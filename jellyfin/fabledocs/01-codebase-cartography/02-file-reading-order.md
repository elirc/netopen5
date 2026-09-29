# File Reading Order

30 files, ordered so each one makes the next legible. Per file: why it matters, what to look for, what to skip. Times are honest estimates for active reading (taking notes), not skimming.

## Junior path (files 1–12): "can I follow a request?"

| # | File | Why / look for | Ignore |
| --- | --- | --- | --- |
| 1 | [README.md](../../README.md) | How to build/run; the repo hosts server only | Badge wall |
| 2 | [Jellyfin.sln](../../Jellyfin.sln) + root folder listing | Project inventory; match against the [system map](01-system-map.md) | GUIDs |
| 3 | [Jellyfin.Server/Program.cs](../../Jellyfin.Server/Program.cs#L71-L157) | Config layering (defaults → json → env `JELLYFIN_` → CLI, [L348-L368](../../Jellyfin.Server/Program.cs#L348-L368)); the restart `do/while` [L144-L154](../../Jellyfin.Server/Program.cs#L144-L154) | VAAPI env vars |
| 4 | [Jellyfin.Server/Startup.cs](../../Jellyfin.Server/Startup.cs#L166-L257) | Middleware order. Write the list down by hand — it is asked about in interviews | HttpClient header setup |
| 5 | [Jellyfin.Api/Controllers/UserController.cs](../../Jellyfin.Api/Controllers/UserController.cs#L84-L260) | Attribute routing, `[Authorize(Policy=...)]` per action, DI via constructor | The 8-arg constructor boilerplate |
| 6 | [Jellyfin.Api/Auth/CustomAuthenticationHandler.cs](../../Jellyfin.Api/Auth/CustomAuthenticationHandler.cs#L43-L88) | Token → claims. Note `NoResult()` vs `Fail()` — different downstream behavior | — |
| 7 | [Jellyfin.Api/Helpers/RequestHelpers.cs](../../Jellyfin.Api/Helpers/RequestHelpers.cs#L67-L112) | The IDOR guard; the "admin may act as another user" rule | GetOrderBy |
| 8 | [Jellyfin.Api/Middleware/ExceptionMiddleware.cs](../../Jellyfin.Api/Middleware/ExceptionMiddleware.cs#L51-L136) | Exception→status mapping; prod hides messages [L96-L98](../../Jellyfin.Api/Middleware/ExceptionMiddleware.cs#L96-L98) | — |
| 9 | [src/Jellyfin.Database/.../JellyfinDbContext.cs](../../src/Jellyfin.Database/Jellyfin.Database.Implementations/JellyfinDbContext.cs#L24-L119) | Table inventory. Note `Users`, `BaseItems`, `UserData`, `ApiKeys`, `Devices` | Locking plumbing |
| 10 | [src/Jellyfin.Database/.../Entities/User.cs](../../src/Jellyfin.Database/Jellyfin.Database.Implementations/Entities/User.cs#L14-L120) | Entity with invariants in the constructor (normalized username, defaults) | Preference plumbing |
| 11 | [tests/.../AuthHelper.cs](../../tests/Jellyfin.Server.Integration.Tests/AuthHelper.cs#L22-L76) | The test-side view of login; the legacy auth header format | — |
| 12 | [tests/.../Controllers/UserControllerTests.cs](../../tests/Jellyfin.Server.Integration.Tests/Controllers/UserControllerTests.cs#L37-L132) | Integration test anatomy: factory fixture, ordered tests (and why ordering is a smell) | — |

## Mid path (files 13–22): "can I follow the data?"

| # | File | Why / look for |
| --- | --- | --- |
| 13 | [Jellyfin.Api/Controllers/ItemsController.cs](../../Jellyfin.Api/Controllers/ItemsController.cs#L262-L460) | A 100+-parameter query endpoint; visibility gate at [L344-L352](../../Jellyfin.Api/Controllers/ItemsController.cs#L344-L352) |
| 14 | [Jellyfin.Server.Implementations/Item/BaseItemRepository.Querying.cs](../../Jellyfin.Server.Implementations/Item/BaseItemRepository.Querying.cs#L31-L102) | Count-then-page; random-sort escape hatch; `AsNoTracking` everywhere |
| 15 | [Jellyfin.Server.Implementations/Item/BaseItemRepository.cs](../../Jellyfin.Server.Implementations/Item/BaseItemRepository.cs#L20-L120) | Partial-class split of a 4-file repository; the null-forgiving warning comment [L20-L24](../../Jellyfin.Server.Implementations/Item/BaseItemRepository.cs#L20-L24) |
| 16 | [src/Jellyfin.Database/.../Entities/BaseItemEntity.cs](../../src/Jellyfin.Database/Jellyfin.Database.Implementations/Entities/BaseItemEntity.cs#L9-L100) | Hybrid storage: queryable columns + `Data` JSON blob [L15](../../src/Jellyfin.Database/Jellyfin.Database.Implementations/Entities/BaseItemEntity.cs#L15) |
| 17 | [Emby.Server.Implementations/Library/UserDataManager.cs](../../Emby.Server.Implementations/Library/UserDataManager.cs#L40-L140) | Transaction + LRU cache + event in one method — a full write-path pattern |
| 18 | [Jellyfin.Server.Implementations/Users/UserManager.cs](../../Jellyfin.Server.Implementations/Users/UserManager.cs#L491-L657) | Login: per-user lock, `ExecuteUpdateAsync`, lockout counter |
| 19 | [Jellyfin.Server.Implementations/Security/AuthorizationContext.cs](../../Jellyfin.Server.Implementations/Security/AuthorizationContext.cs#L43-L222) | Per-request caching in `HttpContext.Items`; token fallback chain; API-key branch |
| 20 | [Emby.Server.Implementations/ScheduledTasks/TaskManager.cs](../../Emby.Server.Implementations/ScheduledTasks/TaskManager.cs#L16-L120) | The background-work engine: queue semantics, cancel-and-requeue |
| 21 | [Emby.Server.Implementations/Library/LibraryManager.cs](../../Emby.Server.Implementations/Library/LibraryManager.cs#L1368-L1459) | The scan: stop monitor → validate → post-scan tasks → restart monitor (invariant repair in `finally`) |
| 22 | [Jellyfin.Server/Extensions/ApiServiceCollectionExtensions.cs](../../Jellyfin.Server/Extensions/ApiServiceCollectionExtensions.cs#L63-L100) | All authorization policies declared in one place |
| 23 | [Emby.Server.Implementations/QuickConnect/QuickConnectManager.cs](../../Emby.Server.Implementations/QuickConnect/QuickConnectManager.cs#L72-L229) | In-memory state machine with expiry; crypto RNG for codes |

## Senior path (files 24–30): "what does this commit us to?"

| # | File | Why / look for |
| --- | --- | --- |
| 24 | [Jellyfin.Server/Migrations/JellyfinMigrationService.cs](../../Jellyfin.Server/Migrations/JellyfinMigrationService.cs) | The *second* migration system (staged code routines) living beside EF migrations — why? |
| 25 | [Jellyfin.Server/Migrations/Routines/20250420200000_MigrateLibraryDb.cs](../../Jellyfin.Server/Migrations/Routines/20250420200000_MigrateLibraryDb.cs) | A real large data migration; note backup attributes on routines in this folder |
| 26 | [Emby.Server.Implementations/HttpServer/WebSocketManager.cs](../../Emby.Server.Implementations/HttpServer/WebSocketManager.cs#L38-L101) | Real-time fan-out to listeners; auth before accept |
| 27 | [Jellyfin.Server.Implementations/Events/EventManager.cs](../../Jellyfin.Server.Implementations/Events/EventManager.cs) | Pub/sub decoupling; consumers in [Events/Consumers](../../Jellyfin.Server.Implementations/Events/Consumers) |
| 28 | [Jellyfin.Api/Middleware/IpBasedAccessValidationMiddleware.cs](../../Jellyfin.Api/Middleware/IpBasedAccessValidationMiddleware.cs#L36-L62) | Network-level authorization; note it runs *after* UseAuthorization in [Startup.cs#L234-L236](../../Jellyfin.Server/Startup.cs#L234-L236) — think about why, and what it would break if moved |
| 29 | [Directory.Build.props](../../Directory.Build.props) + [BannedSymbols.txt](../../BannedSymbols.txt) | Warnings-as-errors, custom analyzers: how a 20-project repo keeps style coherent |
| 30 | [.github/workflows/openapi-generate.yml](../../.github/workflows/openapi-generate.yml) | Contract testing via generated-spec diff — the API's regression net |

## How to read (transferable method)

For every file: (1) read the type's public members first, ignore bodies; (2) pick the one method the file exists for and read it line by line; (3) write one sentence: "this file owns X and must never do Y." If you can't fill in Y, you haven't found the boundary yet — a *boundary* is the line where responsibility changes hands, and most bugs live on one.
