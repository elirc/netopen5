using System;
using System.Collections.Generic;
using System.Security.Claims;
using Jellyfin.Api.Controllers;
using Jellyfin.Database.Implementations.Entities;
using MediaBrowser.Controller.Dto;
using MediaBrowser.Controller.Entities;
using MediaBrowser.Controller.Library;
using MediaBrowser.Model.Dto;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.Querying;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Moq;
using Xunit;

namespace Jellyfin.Api.Tests.Controllers;

public class UserLibraryLatestMediaTests
{
    private readonly Mock<IUserManager> _users = new(MockBehavior.Strict);
    private readonly Mock<IUserViewManager> _views = new(MockBehavior.Strict);
    private readonly Mock<IDtoService> _dtos = new(MockBehavior.Strict);

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
    [InlineData(20)]
    [InlineData(int.MaxValue / 2)]
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
        _dtos.Setup(x => x.GetBaseItemDtos(It.IsAny<IReadOnlyList<BaseItem>>(), It.IsAny<DtoOptions>(), user, null, true))
            .Returns(Array.Empty<BaseItemDto>());

        var result = controller.GetLatestMedia(user.Id, null, [], [], null, null, null, [], null);

        var ok = Assert.IsAssignableFrom<OkObjectResult>(result.Result);
        Assert.Equal(StatusCodes.Status200OK, ok.StatusCode);
        _views.VerifyAll();
    }

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
