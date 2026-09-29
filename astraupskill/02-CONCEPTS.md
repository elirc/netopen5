# The boundary comes from integer arithmetic

A signed 32-bit integer has a maximum of 2,147,483,647. Doubling 1,073,741,823 produces 2,147,483,646, which is representable. Doubling the next integer exceeds the maximum. The accepted upper bound is therefore int.MaxValue / 2. The lower bound is one because this endpoint asks for a positive maximum number of returned items.

This is an input-validity rule, not a performance capacity guarantee. Accepting a large representable value does not promise that a real media library can satisfy it quickly. A separate product decision could impose a smaller operational limit, but that would need its own compatibility review. This change addresses the demonstrated arithmetic defect while preserving ordinary caller behavior.

Validation belongs before downstream work because later consumers should not have to interpret impossible query values. Testing only an annotation would leave uncertainty when the method is invoked directly or through a compatibility delegate. The explicit guard makes the shared behavior visible in both routes.

Boundary tests should include zero, a negative integer, int.MinValue, the first overflowing double, int.MaxValue, and the highest accepted value. Including both sides of the exact upper boundary prevents an off-by-one implementation from passing a collection of only small examples. Default-value testing separately protects clients that omit the parameter.

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
