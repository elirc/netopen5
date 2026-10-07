# Exercises at both ends of the range

Write each prediction before you check it. Every **Check** uses the focused command from the `jellyfin` folder, `dotnet test tests/Jellyfin.Api.Tests/Jellyfin.Api.Tests.csproj --filter "FullyQualifiedName~UserLibraryLatestMediaTests"`, and a disposable edit you undo with `git checkout -- jellyfin`.

## Exercise 1 - The exact upper bound

**Goal.** Calculate the largest integer that can be doubled without overflowing a signed 32-bit result. Write down the accepted value and the next value, which is rejected. Explain why testing only `int.MaxValue` would miss an off-by-one guard that rejects *too many* values.

**Check.** Change `>` to `>=` in the guard (`jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs:538`). Predict which `InlineData` row fails (and in which theory) before you run the command.

## Exercise 2 - Reject *before* the work

**Goal.** Imagine an implementation that returns `BadRequest` only after `GetLatestItems` runs. Predict which test fails and why. What is the observable difference between "returns the right status" and "does no invalid downstream work"?

**Check.** Move the `if` block below the `_userManager.GetUserById` call and run the command. Read the failure. Is it an assertion about the result type, or a strict-mock exception?

## Exercise 3 - One guard, two routes

**Goal.** Suppose the predicate were copied into `GetLatestMediaLegacy` and removed from the main method. Which route becomes unprotected? Why is delegation to a single validated method easier to maintain than two guards?

**Check.** `LegacyRoute_UsesTheSameLimitGuard` covers the legacy route and `InvalidLimit_*` covers the main one. Confirm by reading lines 622-638 that the legacy method has no body of its own, only `=> GetLatestMedia(...)`.

## Exercise 4 - Defaults are a contract

**Goal.** Compare a test that passes `20` explicitly with one that omits `limit`. Change the default to `21` in your head and predict which test notices. Do the same for `groupItems = true`.

**Check.** Edit the default in the signature (`jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs:534`) and run the command. Only one test should fail. Then restore it and flip the `groupItems` default instead.

## Exercise 5 - Forwarding versus selection

**Goal.** Design a normal request with a parent id, a played-state filter and grouping disabled. List the `LatestItemsQuery` fields that must arrive unchanged. Then separate that forwarding contract from two claims the controller test cannot make: which media are actually selected, and how HTTP binds `?limit=abc`.

**Check.** Compare your list with the `It.Is<LatestItemsQuery>(...)` predicate in `ValidLimit_ForwardsFiltersAndReturnsEmptyResults` (test file line 66). Find the one forwarded field that the predicate does *not* check, and decide whether that is a gap.

## Source excerpt

From [jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs](../jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs).

```cs
    [Fact]
    public void OmittedLimit_PreservesTwentyItemDefault()
    {
        var user = new User("latest-default", "authentication", "reset");
        var controller = CreateController(user);
        _users.Setup(x => x.GetUserById(user.Id)).Returns(user);
        _views.Setup(x => x.GetLatestItems(It.Is<LatestItemsQuery>(q => q.Limit == 20 && q.GroupItems), It.IsAny<DtoOptions>()))
            .Returns(new List<Tuple<BaseItem, List<BaseItem>>>());
        _dtos.Setup(x => x.GetBaseItemDtos(It.IsAny<IReadOnlyList<BaseItem>>(), It.IsAny<DtoOptions>(), user, null, true))
            .Returns(Array.Empty<BaseItemDto>());

        var result = controller.GetLatestMedia(user.Id, null, [], [], null, null, null, [], null);

        var ok = Assert.IsAssignableFrom<OkObjectResult>(result.Result);
        Assert.Equal(StatusCodes.Status200OK, ok.StatusCode);
        _views.VerifyAll();
    }

    private UserLibraryController CreateController(User? user = null)
    {
```

## Course navigation

[README](README.md) / [01-CODEBASE-MAP](01-CODEBASE-MAP.md) / [02-CONCEPTS](02-CONCEPTS.md) / [03-WORKED-CHANGE](03-WORKED-CHANGE.md) / [04-TESTING-AND-DEBUGGING](04-TESTING-AND-DEBUGGING.md) / [05-PRACTICE](05-PRACTICE.md) / [06-SOLUTIONS-AND-REVIEW](06-SOLUTIONS-AND-REVIEW.md) / [07-TRACE-LAB](07-TRACE-LAB.md) / [VERIFICATION](VERIFICATION.md)
