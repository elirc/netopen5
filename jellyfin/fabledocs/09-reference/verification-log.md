# Verification Log

Running log of what was inspected, run, and left unverified while authoring this curriculum. Date of authoring pass: **2026-07-16**. Git state at start: branch `master`, clean tree, HEAD `f8771b52ec`.

## Commands run (verified)

| Command | Result |
| --- | --- |
| `dotnet --list-sdks` | `10.0.302` installed — satisfies [global.json](../../global.json) (`10.0.0`, rollForward latestMinor) |
| Directory listings of all top-level projects, `Jellyfin.Api/Controllers` (59 controllers), `tests/` (16 test projects), `.github/workflows` (15 workflows), EF migrations dir (101 files incl. Designer files) | Used for system map and counts |

**Not run:** `dotnet build`, `dotnet test`, `dotnet run` (multi-minute operations on this solution; all build/test/run commands in these docs are marked __inferred__ and were derived from [README.md](../../README.md#L120-L176) and [ci-tests.yml](../../.github/workflows/ci-tests.yml#L29-L35)).

## Files read in full or in large part (line anchors written against these reads)

- `Jellyfin.Server/Program.cs` (entire file, 377 lines)
- `Jellyfin.Server/Startup.cs` (entire file, 259 lines)
- `Jellyfin.Api/Auth/CustomAuthenticationHandler.cs` (entire, 90 lines)
- `Jellyfin.Server.Implementations/Security/AuthorizationContext.cs` (entire, 319 lines)
- `Jellyfin.Api/Auth/DefaultAuthorizationPolicy/DefaultAuthorizationHandler.cs` (entire, 96 lines)
- `Jellyfin.Api/Controllers/UserController.cs` (L1–260)
- `Emby.Server.Implementations/Session/SessionManager.cs` (L1600–1780)
- `Jellyfin.Server.Implementations/Users/UserManager.cs` (L470–760)
- `Jellyfin.Server.Implementations/Users/DefaultAuthenticationProvider.cs` (entire, 111 lines)
- `Jellyfin.Api/Helpers/RequestHelpers.cs` (entire, 188 lines)
- `Jellyfin.Api/Controllers/ItemsController.cs` (L1–120, L255–454)
- `Jellyfin.Server.Implementations/Item/BaseItemRepository.cs` (L1–130)
- `Jellyfin.Server.Implementations/Item/BaseItemRepository.Querying.cs` (L1–160)
- `Emby.Server.Implementations/ScheduledTasks/TaskManager.cs` (L1–120)
- `Emby.Server.Implementations/ScheduledTasks/Tasks/RefreshMediaLibraryTask.cs` (entire, 65 lines)
- `Emby.Server.Implementations/Library/LibraryManager.cs` (L1360–1500)
- `Emby.Server.Implementations/Library/UserDataManager.cs` (L40–180)
- `Jellyfin.Api/Controllers/PlaystateController.cs` (L1–120)
- `Emby.Server.Implementations/QuickConnect/QuickConnectManager.cs` (entire, 231 lines)
- `Emby.Server.Implementations/HttpServer/WebSocketManager.cs` (entire, 103 lines)
- `Jellyfin.Api/Middleware/ExceptionMiddleware.cs` (entire, 150 lines)
- `Jellyfin.Api/Middleware/IpBasedAccessValidationMiddleware.cs` (entire, 63 lines)
- `src/Jellyfin.Database/Jellyfin.Database.Implementations/JellyfinDbContext.cs` (L1–120 + grep of L261–332)
- `src/Jellyfin.Database/Jellyfin.Database.Implementations/Entities/User.cs` (L1–120)
- `src/Jellyfin.Database/Jellyfin.Database.Implementations/Entities/BaseItemEntity.cs` (L1–100)
- `tests/Jellyfin.Server.Integration.Tests/Controllers/UserControllerTests.cs` (L1–140)
- `tests/Jellyfin.Server.Integration.Tests/AuthHelper.cs` (entire, 85 lines)
- `.github/workflows/ci-tests.yml`, `Directory.Build.props`, `global.json`, `README.md` (entire)
- `Jellyfin.Server/Extensions/ApiServiceCollectionExtensions.cs` (grep of policy registrations, L63–86, L267–269)
- `Emby.Server.Implementations/Library/UserDataManager.cs` cache/ctor (L40–44)

Additional files were greped or partially read during later modules; entries are appended below as authoring proceeds.

## Uncertainties and areas not covered

- **Transcoding/HLS internals** (`Jellyfin.Api/Controllers/DynamicHlsController.cs`, `MediaBrowser.MediaEncoding`) — treated at map level only; no line-level behavioral claims made.
- **LiveTV, SyncPlay, plugin system internals** — mapped, not traced.
- **Runtime behavior** (actual server boot, endpoint responses) — not exercised; all behavioral claims come from reading code and tests.
- `AuthorizationContext.GetParts` header parsing was read carefully but its edge cases (escaped quotes) were not executed — flagged "investigate" where relevant.
- EF-generated SQL was not captured; N+1/perf claims are reasoned from the LINQ shape and labeled as such.

## Append log

- 2026-07-16: Initial exploration pass complete; README.md and 00-fast-track.md written; anchors re-checked against reads from the same session.
