# Strict mocks expose forbidden work

The invalid-limit theory uses strict mocks for user lookup, latest-item lookup, and DTO conversion. A bad value must return BadRequestObjectResult. VerifyNoOtherCalls then documents that no collaborator was consulted. This is stronger than checking only the returned status: a controller could otherwise reject input after expensive or stateful work had already occurred.

The valid theory includes the largest safe value without allocating that many items. The view manager is a mock that returns an empty list, so the test checks forwarding and arithmetic-boundary acceptance rather than memory capacity. The resulting empty DTO collection is the expected ordinary response.

The legacy test suppresses the obsolete warning only around the compatibility call. It does not remove the production obsolete marker or weaken project-wide warnings. The default test omits the optional limit and grouping parameters and checks their preserved values.

When a test fails, identify the boundary first. A strict mock exception on invalid input means validation occurred too late or not at all. A failed query predicate on valid input means the controller changed a forwarded value. A compilation or restore error is setup evidence, not a failing request assertion. Run the focused class using the recorded SDK and command, then retain the actual terminal result in the verification chapter.

## Source excerpt

From [jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs](../jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs).

```cs
    public void ValidLimit_ForwardsFiltersAndReturnsEmptyResults(int limit)
    {
        var user = new User("latest-test", "authentication", "reset");
        var parentId = Guid.NewGuid();
        var controller = CreateController(user);
        _users.Setup(x => x.GetUserById(user.Id)).Returns(user);
        _views.Setup(x => x.GetLatestItems(
                It.Is<LatestItemsQuery>(q => q.Limit == limit && q.ParentId.Equals(parentId) && q.User == user && !q.GroupItems && q.IsPlayed == true),
                It.IsAny<DtoOptions>()))
            .Returns(new List<Tuple<BaseItem, List<BaseItem>>>());
        _dtos.Setup(x => x.GetBaseItemDtos(It.Is<IReadOnlyList<BaseItem>>(items => items.Count == 0), It.IsAny<DtoOptions>(), user, null, true))
            .Returns(Array.Empty<BaseItemDto>());

        var result = controller.GetLatestMedia(user.Id, parentId, [], [], true, null, null, [], null, limit, false);

        var ok = Assert.IsAssignableFrom<OkObjectResult>(result.Result);
        Assert.Equal(StatusCodes.Status200OK, ok.StatusCode);
        Assert.Empty(Assert.IsAssignableFrom<IEnumerable<BaseItemDto>>(ok.Value));
        _views.VerifyAll();
    }

    [Fact]
    public void OmittedLimit_PreservesTwentyItemDefault()
    {
        var user = new User("latest-default", "authentication", "reset");
        var controller = CreateController(user);
        _users.Setup(x => x.GetUserById(user.Id)).Returns(user);
        _views.Setup(x => x.GetLatestItems(It.Is<LatestItemsQuery>(q => q.Limit == 20 && q.GroupItems), It.IsAny<DtoOptions>()))
            .Returns(new List<Tuple<BaseItem, List<BaseItem>>>());
```

## Course navigation

[README](README.md) / [01-CODEBASE-MAP](01-CODEBASE-MAP.md) / [02-CONCEPTS](02-CONCEPTS.md) / [03-WORKED-CHANGE](03-WORKED-CHANGE.md) / [04-TESTING-AND-DEBUGGING](04-TESTING-AND-DEBUGGING.md) / [05-PRACTICE](05-PRACTICE.md) / [06-SOLUTIONS-AND-REVIEW](06-SOLUTIONS-AND-REVIEW.md) / [07-TRACE-LAB](07-TRACE-LAB.md) / [VERIFICATION](VERIFICATION.md)
