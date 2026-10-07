# Follow the latest-media request

UserLibraryController exposes Items/Latest and the older Users/{userId}/Items/Latest compatibility route. The main method receives the optional user and parent identifiers, requested DTO fields, item kinds, played-state filter, image options, user-data option, integer limit, and grouping flag. The compatibility method forwards the same values into the main method.

After validation, RequestHelpers resolves the authorized user identifier and IUserManager loads the user. Missing users retain the existing not-found behavior. If the caller did not specify isPlayed, the user's HidePlayedInLatest preference can supply the filter. DtoOptions combines the field and image settings before the query.

IUserViewManager.GetLatestItems receives LatestItemsQuery. The controller then resolves grouped items, asks IDtoService for DTOs, restores child counts, and returns an OK result. The new guard is deliberately before these operations: an invalid limit should not trigger authorization-dependent library lookup, candidate allocation, or DTO work.

The focused test class sits beside existing API controller tests and uses the same Moq and xUnit conventions. Strict user, view, and DTO mocks make unexpected invalid-path calls fail. Normal-path tests configure only the expected query and empty result conversion. Follow those collaborator boundaries when determining whether a future failure belongs to input validation, user resolution, library selection, or DTO presentation.

## Line map (checked 2026-10-06)

The full method is printed in the [course README](README.md#source-excerpt). Use this table to jump around the real files instead.

| Step | Where |
|---|---|
| Current route `GET Items/Latest`, with 200 and 400 metadata | `jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs:521-523` |
| The guard | `jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs:538-541` |
| User resolution and the not-found branch | `jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs:543-548` |
| `HidePlayedInLatest` can supply `isPlayed` | `jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs:550-556` |
| `LatestItemsQuery` built and sent to the view manager | `jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs:563-573` |
| Grouping tuples resolved, DTOs fetched, child counts restored, `Ok(...)` | `jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs:575-603` |
| Legacy route `GET Users/{userId}/Items/Latest`, `[Obsolete]`, delegates with `=> GetLatestMedia(...)` | `jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs:622-638` |
| Where the limit is read (`request.Limit ?? 10`) and **doubled** (`Limit = limit * 2`) | `jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs:242` and `:365` |
| The focused tests: strict mocks (21-23), invalid theory (25-40), legacy (42-53), valid theory (55-78), default (80 onward) | `jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs` |

## Course navigation

[README](README.md) / [01-CODEBASE-MAP](01-CODEBASE-MAP.md) / [02-CONCEPTS](02-CONCEPTS.md) / [03-WORKED-CHANGE](03-WORKED-CHANGE.md) / [04-TESTING-AND-DEBUGGING](04-TESTING-AND-DEBUGGING.md) / [05-PRACTICE](05-PRACTICE.md) / [06-SOLUTIONS-AND-REVIEW](06-SOLUTIONS-AND-REVIEW.md) / [07-TRACE-LAB](07-TRACE-LAB.md) / [VERIFICATION](VERIFICATION.md)
