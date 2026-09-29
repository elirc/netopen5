# Exercises at both ends of the range

Calculate the largest integer that can be doubled without overflowing a signed 32-bit result. Write down both the accepted value and the immediately following rejected value. Explain why testing only int.MaxValue would miss an off-by-one error in a guard that rejects too many valid values.

Next, propose an implementation that returns BadRequest only after GetLatestItems runs. Predict which existing test fails and why. Identify the observable difference between returning the correct status and avoiding invalid downstream work.

For the compatibility route, imagine copying the predicate into GetLatestMediaLegacy while removing it from the main method. Which callers become unprotected? Explain why delegation to a single validated method is easier to maintain than independent guards.

For defaults, compare a test that explicitly passes twenty with one that omits limit. Change the default mentally to twenty-one and predict which test detects it. Repeat for the grouping default.

Finally, design a normal request with a parent identifier, played-state filter, and grouping disabled. List the query fields that must arrive unchanged at the view manager. Separate that forwarding contract from a claim about actual media selection or HTTP model binding, neither of which is established by a controller test with mocked collaborators.

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
