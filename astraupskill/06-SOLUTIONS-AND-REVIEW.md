# Answers and compatibility review

The arithmetic answer is 1,073,741,823. Doubling it yields 2,147,483,646. The next value would exceed int.MaxValue when doubled. A correct predicate rejects values greater than that half-maximum, not values greater than or equal to it. Zero and every negative value are independently invalid.

Moving validation after the library query violates the strict invalid-path tests. The expected bad-request response alone is insufficient: the collaborator calls are part of the regression contract. Invalid input must not reach user resolution, candidate grouping, or DTO conversion.

The compatibility route should retain delegation into the guarded method. Protecting only the legacy route leaves Items/Latest exposed, while maintaining separate predicates risks inconsistent behavior. The obsolete-warning suppression in the test acknowledges that the route is retained for compatibility; it does not declare that new clients should prefer it.

The omitted-parameter test catches a changed signature default that an explicit-twenty test would miss. Normal forwarding must preserve the supplied parent, played state, grouping flag, limit, and user. The empty-list fixture verifies response shape without requiring a media database.

## Check answers (derived by reading the code and tests, 2026-10-06)

| Exercise edit | Expected failures | Why |
|---|---|---|
| 1: `>` becomes `>=` | `ValidLimit_ForwardsFiltersAndReturnsEmptyResults(1073741823)` only | The highest valid value is now rejected. The invalid theory still passes because every one of its values is still rejected. A suite holding only `int.MaxValue` would never notice. |
| 2: guard moved below `GetUserById` | all five `InvalidLimit_*` cases with a Moq strict-mock exception, plus `LegacyRoute_UsesTheSameLimitGuard` with a `SecurityException` | In the invalid tests `userId` is null, so `RequestHelpers.GetUserId` (`jellyfin/Jellyfin.Api/Helpers/RequestHelpers.cs:67-85`) returns the empty claim id and the un-setup strict `GetUserById` throws. The legacy test passes a random `userId` for a non-admin principal, so line 81 throws `SecurityException("Forbidden")` before any user lookup. |
| 4: default `limit = 21` | `OmittedLimit_PreservesTwentyItemDefault` only (its predicate requires `q.Limit == 20`) | The valid theory passes `limit` explicitly. |
| 4: default `groupItems = false` | `OmittedLimit_PreservesTwentyItemDefault` only (`&& q.GroupItems`) | The valid theory passes `false` explicitly. |
| 5: the unchecked field | `IncludeItemTypes` is forwarded (`UserLibraryController.cs:567`) but not asserted | It is a real, small gap. Swapping `includeItemTypes` for an empty array in the controller would pass every test. |

The second row hides a design point. Because validation runs first, an unauthorized caller asking for another user's feed with `limit=0` gets **400**, not **403**. Validating before authorizing is acceptable here because the 400 reveals nothing about the other user. Still, it is a deliberate ordering, and a reviewer should name it.

**What HTTP adds that these tests cannot see.** `UserLibraryController` inherits `[ApiController]` from `BaseJellyfinApiController` (`jellyfin/Jellyfin.Api/BaseJellyfinApiController.cs:12`). So a query value that cannot bind to `int` at all (`?limit=abc`, or `?limit=3000000000`, which is out of `int` range) is answered with ASP.NET Core's automatic 400 `ValidationProblemDetails` *before* the action runs. Only values that bind successfully reach this guard, whose 400 body is a plain string. Same status, two different bodies. Only an HTTP-level test (for example with `WebApplicationFactory`) can pin both.

During review, avoid overstating the bound. It prevents the known overflow and nonpositive inputs. It does not implement rate limiting, cap total resource use, or prove server-wide authorization behavior. Those would be separate changes with separate acceptance criteria. Keep the focused regression evidence and those operational limits visible together.

## Source excerpt

From [jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs](../jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs).

```cs
    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(int.MinValue)]
    [InlineData((int.MaxValue / 2) + 1)]
    [InlineData(int.MaxValue)]
    public void InvalidLimit_ReturnsBadRequestBeforeLibraryAccess(int limit)
    {
        var controller = CreateController();
        var result = controller.GetLatestMedia(null, null, [], [], null, null, null, [], null, limit);

        Assert.IsType<BadRequestObjectResult>(result.Result);
        _users.VerifyNoOtherCalls();
        _views.VerifyNoOtherCalls();
        _dtos.VerifyNoOtherCalls();
    }

    [Fact]
    public void LegacyRoute_UsesTheSameLimitGuard()
    {
        var controller = CreateController();
#pragma warning disable CS0618 // Exercise the supported compatibility route.
        var result = controller.GetLatestMediaLegacy(Guid.NewGuid(), null, [], [], null, null, null, [], null, 0);
#pragma warning restore CS0618

        Assert.IsType<BadRequestObjectResult>(result.Result);
        _views.VerifyNoOtherCalls();
        _users.VerifyNoOtherCalls();
    }

    [Theory]
    [InlineData(1)]
```

## Course navigation

[README](README.md) / [01-CODEBASE-MAP](01-CODEBASE-MAP.md) / [02-CONCEPTS](02-CONCEPTS.md) / [03-WORKED-CHANGE](03-WORKED-CHANGE.md) / [04-TESTING-AND-DEBUGGING](04-TESTING-AND-DEBUGGING.md) / [05-PRACTICE](05-PRACTICE.md) / [06-SOLUTIONS-AND-REVIEW](06-SOLUTIONS-AND-REVIEW.md) / [07-TRACE-LAB](07-TRACE-LAB.md) / [VERIFICATION](VERIFICATION.md)
