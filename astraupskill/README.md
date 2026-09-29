# Jellyfin latest media: validate before library work

This improvement targets one API boundary: the latest-media limit. The existing endpoint defaults to twenty items and forwards a caller-supplied integer into the library query. Zero and negative values do not express a meaningful positive result limit. Extremely large values can also overflow downstream arithmetic that doubles the requested limit when fetching candidate groups.

The controller now rejects limits outside one through int.MaxValue divided by two before resolving a user or querying the library. The bound follows the actual arithmetic constraint. It does not introduce an arbitrary small page-size policy. Existing normal requests, the twenty-item default, filtering options, and the legacy route continue through the existing implementation.

Read the map and concepts chapters first, then inspect the small guard in the worked change. Tests call the real controller with strict mocked collaborators. Invalid inputs must produce a bad-request result without library or user access. Valid inputs must preserve their query values and return the normal result shape. The legacy route delegates into the same guard.

The verification record describes focused API tests, not a complete Jellyfin server deployment or media-library scan. The source-based exercises ask you to reason about the exact arithmetic boundary and distinguish controller behavior from HTTP binding. Existing project documentation is preserved; this course explains the bounded change and its evidence.

## Source excerpt

From [jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs](../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs).

```cs
    public ActionResult<IEnumerable<BaseItemDto>> GetLatestMedia(
        [FromQuery] Guid? userId,
        [FromQuery] Guid? parentId,
        [FromQuery, ModelBinder(typeof(CommaDelimitedCollectionModelBinder))] ItemFields[] fields,
        [FromQuery, ModelBinder(typeof(CommaDelimitedCollectionModelBinder))] BaseItemKind[] includeItemTypes,
        [FromQuery] bool? isPlayed,
        [FromQuery] bool? enableImages,
        [FromQuery] int? imageTypeLimit,
        [FromQuery, ModelBinder(typeof(CommaDelimitedCollectionModelBinder))] ImageType[] enableImageTypes,
        [FromQuery] bool? enableUserData,
        [FromQuery] int limit = 20,
        [FromQuery] bool groupItems = true)
    {
        // The library query doubles this value when fetching candidate groups.
        if (limit <= 0 || limit > int.MaxValue / 2)
        {
            return BadRequest("Limit must be between 1 and 1073741823.");
        }

        var requestUserId = RequestHelpers.GetUserId(User, userId);
        var user = _userManager.GetUserById(requestUserId);
        if (user is null)
        {
            return NotFound();
        }

        if (!isPlayed.HasValue)
        {
            if (user.HidePlayedInLatest)
            {
                isPlayed = false;
            }
        }

        var dtoOptions = new DtoOptions { Fields = fields }
            .AddAdditionalDtoOptions(enableImages, enableUserData, imageTypeLimit, enableImageTypes);

        dtoOptions.PreferEpisodeParentPoster = true;

        var list = _userViewManager.GetLatestItems(
            new LatestItemsQuery
            {
```

## Course navigation

[README](README.md) / [01-CODEBASE-MAP](01-CODEBASE-MAP.md) / [02-CONCEPTS](02-CONCEPTS.md) / [03-WORKED-CHANGE](03-WORKED-CHANGE.md) / [04-TESTING-AND-DEBUGGING](04-TESTING-AND-DEBUGGING.md) / [05-PRACTICE](05-PRACTICE.md) / [06-SOLUTIONS-AND-REVIEW](06-SOLUTIONS-AND-REVIEW.md) / [07-TRACE-LAB](07-TRACE-LAB.md) / [VERIFICATION](VERIFICATION.md)
