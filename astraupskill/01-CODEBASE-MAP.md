# Follow the latest-media request

UserLibraryController exposes Items/Latest and the older Users/{userId}/Items/Latest compatibility route. The main method receives the optional user and parent identifiers, requested DTO fields, item kinds, played-state filter, image options, user-data option, integer limit, and grouping flag. The compatibility method forwards the same values into the main method.

After validation, RequestHelpers resolves the authorized user identifier and IUserManager loads the user. Missing users retain the existing not-found behavior. If the caller did not specify isPlayed, the user's HidePlayedInLatest preference can supply the filter. DtoOptions combines the field and image settings before the query.

IUserViewManager.GetLatestItems receives LatestItemsQuery. The controller then resolves grouped items, asks IDtoService for DTOs, restores child counts, and returns an OK result. The new guard is deliberately before these operations: an invalid limit should not trigger authorization-dependent library lookup, candidate allocation, or DTO work.

The focused test class sits beside existing API controller tests and uses the same Moq and xUnit conventions. Strict user, view, and DTO mocks make unexpected invalid-path calls fail. Normal-path tests configure only the expected query and empty result conversion. Follow those collaborator boundaries when determining whether a future failure belongs to input validation, user resolution, library selection, or DTO presentation.

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
```

## Course navigation

[README](README.md) / [01-CODEBASE-MAP](01-CODEBASE-MAP.md) / [02-CONCEPTS](02-CONCEPTS.md) / [03-WORKED-CHANGE](03-WORKED-CHANGE.md) / [04-TESTING-AND-DEBUGGING](04-TESTING-AND-DEBUGGING.md) / [05-PRACTICE](05-PRACTICE.md) / [06-SOLUTIONS-AND-REVIEW](06-SOLUTIONS-AND-REVIEW.md) / [07-TRACE-LAB](07-TRACE-LAB.md) / [VERIFICATION](VERIFICATION.md)
