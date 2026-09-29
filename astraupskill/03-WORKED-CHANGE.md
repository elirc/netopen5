# Place one guard before all collaborators

The production change is small enough to review directly. At the beginning of GetLatestMedia, reject limit <= 0 or limit > int.MaxValue / 2 and return BadRequest with the accepted range. The endpoint metadata also documents a 400 response. Everything after that guard retains the existing user lookup, filter construction, grouping, and DTO behavior.

The legacy method already delegates to GetLatestMedia, so it needs no duplicate validation implementation. Duplicating the predicate there would create two places that could drift during later maintenance. Its regression test invokes the compatibility method and checks the same bad-request result without downstream calls.

Valid-limit tests supply an authenticated test principal and a known user. The view mock expects the exact limit, parent, grouping flag, played-state filter, and user object. An empty view result flows through the existing DTO conversion and returns an empty collection in an OK response. This verifies that the guard has not accidentally changed normal delegation.

The omitted-limit case calls the method without the optional arguments and expects twenty with grouping enabled. That is distinct from passing twenty explicitly: it protects the signature's default contract. None of these tests creates or modifies a real media library, and the invalid tests need no user fixture because the guard must exit before user resolution.

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

```

## Course navigation

[README](README.md) / [01-CODEBASE-MAP](01-CODEBASE-MAP.md) / [02-CONCEPTS](02-CONCEPTS.md) / [03-WORKED-CHANGE](03-WORKED-CHANGE.md) / [04-TESTING-AND-DEBUGGING](04-TESTING-AND-DEBUGGING.md) / [05-PRACTICE](05-PRACTICE.md) / [06-SOLUTIONS-AND-REVIEW](06-SOLUTIONS-AND-REVIEW.md) / [07-TRACE-LAB](07-TRACE-LAB.md) / [VERIFICATION](VERIFICATION.md)
