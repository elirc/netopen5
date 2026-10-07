# Focused verification and limits

The recorded checks below define the verified scope. The new tests execute the actual controller class with mocked user, library-view, and DTO services. Invalid-value assertions inspect both the response and the absence of collaborator calls. Valid-value assertions inspect query forwarding, empty result shape, the default limit, and compatibility delegation.

These checks do not start the full Jellyfin server, scan a real media library, or verify HTTP binding and authentication middleware. They also do not establish production capacity for the largest accepted value. The upper bound follows a known integer-doubling requirement; operational page-size policy remains outside this change.

To reproduce, use a .NET SDK 10.0.x (`jellyfin/global.json` pins `10.0.0` with `rollForward: latestMinor`) and run from the `jellyfin` folder: `dotnet test tests/Jellyfin.Api.Tests/Jellyfin.Api.Tests.csproj --filter "FullyQualifiedName~UserLibraryLatestMediaTests"`. The recorded run added `--no-restore`, which works only after an earlier restore. Restore and compilation must finish before a test result counts.

**How the 10 is made up.** It is counted from `UserLibraryLatestMediaTests.cs` and matches the TRX `<Counters total="10" executed="10" passed="10" failed="0">`:

| Test | Kind | Cases |
|---|---|---:|
| `InvalidLimit_ReturnsBadRequestBeforeLibraryAccess` | `[Theory]`: 0, -1, `int.MinValue`, `int.MaxValue / 2 + 1`, `int.MaxValue` | 5 |
| `LegacyRoute_UsesTheSameLimitGuard` | `[Fact]` | 1 |
| `ValidLimit_ForwardsFiltersAndReturnsEmptyResults` | `[Theory]`: 1, 20, `int.MaxValue / 2` | 3 |
| `OmittedLimit_PreservesTwentyItemDefault` | `[Fact]` | 1 |

The build reports an existing NU1903 advisory for SQLitePCLRaw.lib.e_sqlite3 2.1.11. This controller change does not upgrade that dependency. The first compile rejected a Guid equality operator in the new test, which was corrected to Equals. The next run exposed Jellyfin's typed OkResult subclass; valid-response assertions now accept the existing OkObjectResult subclass and explicitly check status 200. Neither correction changes the production response contract.

Original snapshots preserve the changed baseline controller, and the new focused test class is included in the delivery manifest. Existing documentation remains in place. Reviewers can compare the small production guard with the boundary examples and decide whether a future HTTP-level or full-library integration check is warranted. Such additional evidence would complement, rather than be implied by, this controller-level regression suite.

## Source excerpt

From [jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs](../jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs).

```cs
    private UserLibraryController CreateController(User? user = null)
    {
        var controller = new UserLibraryController(_users.Object, Mock.Of<IUserDataManager>(), Mock.Of<ILibraryManager>(), _dtos.Object, _views.Object, Mock.Of<IFileSystem>());
        controller.ControllerContext = new ControllerContext
        {
            HttpContext = new DefaultHttpContext
            {
                User = new ClaimsPrincipal(new ClaimsIdentity(user is null ? Array.Empty<Claim>() : new[] { new Claim("Jellyfin-UserId", user.Id.ToString()) }, "test")),
            },
        };
        return controller;
    }
}
```

## Course navigation

[README](README.md) / [01-CODEBASE-MAP](01-CODEBASE-MAP.md) / [02-CONCEPTS](02-CONCEPTS.md) / [03-WORKED-CHANGE](03-WORKED-CHANGE.md) / [04-TESTING-AND-DEBUGGING](04-TESTING-AND-DEBUGGING.md) / [05-PRACTICE](05-PRACTICE.md) / [06-SOLUTIONS-AND-REVIEW](06-SOLUTIONS-AND-REVIEW.md) / [07-TRACE-LAB](07-TRACE-LAB.md) / [VERIFICATION](VERIFICATION.md)

## Recorded command evidence

The accepted test evidence covers **10 distinct passing tests**. The commands below define the verified scope; repeated targeted runs do not increase the count.

| Check | Recorded command | Exit | Evidence |
|---|---|---:|---|
| `astra-netopen5-latest-tests-r3` | `["dotnet", "test", "tests/Jellyfin.Api.Tests/Jellyfin.Api.Tests.csproj", "--no-restore", "--filter", "FullyQualifiedName~UserLibraryLatestMediaTests", "--nologo", "--verbosity", "minimal", "/m:1", "--logger", "trx"]` | 0 | [record](evidence/astra-netopen5-latest-tests-r3.json); the console log it names was not committed |

[Machine-readable results](evidence/regression.trx). The TRX header still records the original workstation's paths; the counts and test names are the evidence.
