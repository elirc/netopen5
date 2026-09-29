# Fast Track: Jellyfin in One Weekend

Goal: by Sunday night you can run the server, trace two end-to-end flows, explain them out loud, and have made one safe change with a passing test. This is the minimum viable understanding everything else builds on.

## 1. Install and run (Saturday morning)

Prerequisite: .NET 10 SDK ([global.json](../global.json) pins `10.0.0` with `rollForward: latestMinor`; SDK presence __verified__ on this machine: `10.0.302`).

```bash
# From repo root
dotnet build                                   # __inferred__ from README.md#L134
dotnet run --project Jellyfin.Server -- --nowebclient   # __inferred__ from README.md#L186-L187
```

- `--nowebclient` matters: this repo is the **server only**. Without the flag it looks for the separately-built web client and exits if missing ([Program.cs#L119-L134](../Jellyfin.Server/Program.cs#L119-L134)).
- Server listens on `http://localhost:8096`; interactive API docs at `/api-docs/swagger/index.html` ([README.md#L142-L144](../README.md#L142-L144)).
- Run the test suite: `dotnet test` (__inferred__; this is exactly what CI runs — [ci-tests.yml#L29-L35](../.github/workflows/ci-tests.yml#L29-L35)). Faster: target one project, e.g. `dotnet test tests/Jellyfin.Model.Tests`.

## 2. The first 10 files to open, in order

| # | File | Why |
| --- | --- | --- |
| 1 | [Jellyfin.Server/Program.cs](../Jellyfin.Server/Program.cs#L71-L157) | Entry point: config layering, logging, migrations, the restart loop. The whole lifecycle in one file. |
| 2 | [Jellyfin.Server/Startup.cs](../Jellyfin.Server/Startup.cs#L166-L257) | The HTTP middleware pipeline. Ordering here is a security decision. |
| 3 | [Jellyfin.Api/Controllers/UserController.cs](../Jellyfin.Api/Controllers/UserController.cs#L209-L236) | `AuthenticateByName` — the login endpoint every client calls first. |
| 4 | [Jellyfin.Api/Auth/CustomAuthenticationHandler.cs](../Jellyfin.Api/Auth/CustomAuthenticationHandler.cs#L43-L88) | How a token on a request becomes a `ClaimsPrincipal`. |
| 5 | [Jellyfin.Api/Helpers/RequestHelpers.cs](../Jellyfin.Api/Helpers/RequestHelpers.cs#L67-L85) | 19 lines that stop users reading each other's data. Memorize this shape. |
| 6 | [Jellyfin.Api/Controllers/ItemsController.cs](../Jellyfin.Api/Controllers/ItemsController.cs#L262-L352) | The biggest read endpoint: visibility checks, query building. |
| 7 | [Jellyfin.Server.Implementations/Item/BaseItemRepository.Querying.cs](../Jellyfin.Server.Implementations/Item/BaseItemRepository.Querying.cs#L31-L64) | Where queries hit EF Core: count + page + deserialize. |
| 8 | [src/Jellyfin.Database/Jellyfin.Database.Implementations/JellyfinDbContext.cs](../src/Jellyfin.Database/Jellyfin.Database.Implementations/JellyfinDbContext.cs#L24-L119) | Every table, one property each. The data model's table of contents. |
| 9 | [Jellyfin.Api/Middleware/ExceptionMiddleware.cs](../Jellyfin.Api/Middleware/ExceptionMiddleware.cs#L51-L136) | One place where exceptions become HTTP status codes. |
| 10 | [tests/Jellyfin.Server.Integration.Tests/AuthHelper.cs](../tests/Jellyfin.Server.Integration.Tests/AuthHelper.cs#L22-L47) | How tests boot the real server and log in — proof the flows work end to end. |

## 3. Trace two flows (Saturday afternoon)

Do these with the files open. Full trace tables live in [01-codebase-cartography/05-key-flows.md](01-codebase-cartography/05-key-flows.md).

**Flow A — Login.** `POST /Users/AuthenticateByName` ([UserController.cs#L209-L236](../Jellyfin.Api/Controllers/UserController.cs#L209-L236)) → `SessionManager.AuthenticateNewSessionInternal` validates and creates a device token ([SessionManager.cs#L1640-L1706](../Emby.Server.Implementations/Session/SessionManager.cs#L1640-L1706)) → `UserManager.AuthenticateUser` checks password, lockout, remote-access, parental schedule ([UserManager.cs#L491-L657](../Jellyfin.Server.Implementations/Users/UserManager.cs#L491-L657)) → `DefaultAuthenticationProvider` verifies the PBKDF2 hash and silently upgrades old hashes ([DefaultAuthenticationProvider.cs#L48-L94](../Jellyfin.Server.Implementations/Users/DefaultAuthenticationProvider.cs#L48-L94)).

*Pause and predict:* before opening SessionManager, write down what you think happens when the same device logs in twice. Then check [SessionManager.cs#L1708-L1737](../Emby.Server.Implementations/Session/SessionManager.cs#L1708-L1737) — old sessions for that device are logged out first.

**Flow B — Mark item played.** `POST /UserPlayedItems/{itemId}` ([PlaystateController.cs#L72-L109](../Jellyfin.Api/Controllers/PlaystateController.cs#L72-L109)) → `UserDataManager.SaveUserData` writes inside an explicit transaction, updates an in-memory LRU cache, and raises `UserDataSaved` ([UserDataManager.cs#L50-L93](../Emby.Server.Implementations/Library/UserDataManager.cs#L50-L93)).

*Pause and predict:* the item may have several "user data keys." Why would a transaction matter here? (Answer: multiple rows must move together — an invariant across rows is exactly what transactions are for.)

## 4. One small safe change (Sunday)

Pick a log message improvement or an XML doc fix — changes with near-zero blast radius (the amount of the system your change can break). Example shape: the log line at [ItemsController.cs#L350](../Jellyfin.Api/Controllers/ItemsController.cs#L350) warns when a user can't access a library. Build, run, hit the endpoint, watch the log. Then revert or keep it as your first-PR candidate — real vetted candidates live in [06-contribution-practice/01-good-first-tickets.md](06-contribution-practice/01-good-first-tickets.md).

Run one test file to close the loop:

```bash
dotnet test tests/Jellyfin.Server.Integration.Tests --filter "FullyQualifiedName~UserControllerTests"   # __inferred__
```

## 5. Teach-back (Sunday night)

Explain Flow A out loud in 90 seconds, as if an interviewer asked "walk me through auth in a codebase you know." A strong answer names: the endpoint, the token creation, **where the lockout counter is incremented** ([UserManager.cs#L627-L653](../Jellyfin.Server.Implementations/Users/UserManager.cs#L627-L653)), and one design tradeoff (e.g. tokens are device rows in the DB, not stateless JWTs — revocable, but every request costs a lookup). Record yourself. If you said "and then it just checks the password," you skipped the four authorization gates — do it again.

## What the fast path skips

Streaming/transcoding (the hardest subsystem), the plugin system, LiveTV, SyncPlay, the dual migration systems, and all of the drills. The two flows you traced are load-bearing for everything else; the rest of the curriculum rotates through six more.
