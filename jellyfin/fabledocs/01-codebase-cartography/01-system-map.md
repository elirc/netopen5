# System Map

## What kind of repo is this?

A **single-application, multi-project .NET solution** ([Jellyfin.sln](../../Jellyfin.sln)) — not a monorepo of independent services. Every project compiles into one server process. The split into ~20 projects is about **layering and ownership**, not deployment: `Jellyfin.Api` cannot reach into `Jellyfin.Server`'s internals, and `MediaBrowser.Model` cannot depend on anything above it. Project references are the boundary-enforcement mechanism C# gives you for free (in a Node monorepo the equivalent is package boundaries + lint rules; the transferable idea is *make illegal dependencies unrepresentable*).

## The map

```
                        ┌──────────────────────────────┐
   process entry ─────▶ │ Jellyfin.Server              │  Program/Startup, DI wiring,
                        │  (composition root)          │  middleware, server migrations
                        └───────┬──────────────────────┘
                                │ hosts
        ┌───────────────────────┼─────────────────────────┐
        ▼                       ▼                         ▼
┌────────────────┐   ┌─────────────────────┐   ┌───────────────────────┐
│ Jellyfin.Api   │   │ Emby.Server.        │   │ Jellyfin.Server.      │
│ HTTP surface:  │   │ Implementations     │   │ Implementations       │
│ 59 controllers,│   │ legacy core: library│   │ modern core: users,   │
│ auth handlers, │   │ scan, sessions,     │   │ security, EF item     │
│ middleware     │   │ scheduled tasks     │   │ repository, events    │
└───────┬────────┘   └─────────┬───────────┘   └──────────┬────────────┘
        │      depend on interfaces in                    │
        ▼                       ▼                         ▼
┌─────────────────────────────────────────────┐  ┌─────────────────────┐
│ MediaBrowser.Controller / .Common           │  │ src/Jellyfin.       │
│ (interface layer: ILibraryManager,          │  │ Database (EF Core   │
│  ISessionManager, IUserManager, BaseItem…)  │  │ entities, DbContext,│
└──────────────────────┬──────────────────────┘  │ SQLite migrations)  │
                       ▼                         └─────────────────────┘
        ┌──────────────────────────────┐
        │ MediaBrowser.Model           │  DTOs & enums shared with clients
        └──────────────────────────────┘
```

## Ownership map

| Concern | Owner (project/folder) | Evidence |
| --- | --- | --- |
| HTTP API + auth policies + middleware | [Jellyfin.Api](../../Jellyfin.Api) | [Controllers/](../../Jellyfin.Api/Controllers), [Auth/](../../Jellyfin.Api/Auth), [Middleware/](../../Jellyfin.Api/Middleware) |
| Process lifecycle, DI, pipeline, server-level migrations | [Jellyfin.Server](../../Jellyfin.Server) | [Program.cs](../../Jellyfin.Server/Program.cs#L71-L157), [Startup.cs](../../Jellyfin.Server/Startup.cs#L63-L257), [Migrations/](../../Jellyfin.Server/Migrations) |
| Contracts (interfaces + domain base classes) | [MediaBrowser.Controller](../../MediaBrowser.Controller), [MediaBrowser.Common](../../MediaBrowser.Common) | e.g. `IUserManager`, `ILibraryManager`, `BaseItem` |
| Wire DTOs shared with every client | [MediaBrowser.Model](../../MediaBrowser.Model) | e.g. `UserDto`, `BaseItemDto`, `QueryResult<T>` |
| Legacy service implementations (library, sessions, tasks, collections, playlists) | [Emby.Server.Implementations](../../Emby.Server.Implementations) | [Library/](../../Emby.Server.Implementations/Library), [Session/](../../Emby.Server.Implementations/Session), [ScheduledTasks/](../../Emby.Server.Implementations/ScheduledTasks) |
| Modern service implementations (users, security, events, EF item repo, trickplay, backup) | [Jellyfin.Server.Implementations](../../Jellyfin.Server.Implementations) | [Users/](../../Jellyfin.Server.Implementations/Users), [Security/](../../Jellyfin.Server.Implementations/Security), [Item/](../../Jellyfin.Server.Implementations/Item), [Events/](../../Jellyfin.Server.Implementations/Events) |
| Persistence (entities, DbContext, EF migrations) | [src/Jellyfin.Database](../../src/Jellyfin.Database) | [JellyfinDbContext.cs](../../src/Jellyfin.Database/Jellyfin.Database.Implementations/JellyfinDbContext.cs#L24-L119), [Migrations/](../../src/Jellyfin.Database/Jellyfin.Database.Providers.Sqlite/Migrations) (101 files) |
| Metadata fetching (TMDb, MusicBrainz, local NFO) | [MediaBrowser.Providers](../../MediaBrowser.Providers), [MediaBrowser.LocalMetadata](../../MediaBrowser.LocalMetadata), [MediaBrowser.XbmcMetadata](../../MediaBrowser.XbmcMetadata) | provider classes per source |
| Transcoding / ffmpeg | [MediaBrowser.MediaEncoding](../../MediaBrowser.MediaEncoding), [src/Jellyfin.MediaEncoding.Hls](../../src/Jellyfin.MediaEncoding.Hls) | not traced in depth in this curriculum |
| Filename → media parsing | [Emby.Naming](../../Emby.Naming) | pure functions, heavily unit-tested — good first reading |
| Networking config (LAN detection, HappyEyeballs) | [src/Jellyfin.Networking](../../src/Jellyfin.Networking) | used by every remote-access auth decision |
| Live TV / DVR | [src/Jellyfin.LiveTv](../../src/Jellyfin.LiveTv) | mapped only |
| Tests | [tests/](../../tests) (16 projects) | unit per-project + [Jellyfin.Server.Integration.Tests](../../tests/Jellyfin.Server.Integration.Tests) booting the real host |

## Public interfaces vs private internals

**Public (a change here is a breaking change for someone):**
- REST API routes and DTO shapes — consumed by every Jellyfin client app; the OpenAPI spec is generated and diffed in CI ([openapi-generate.yml](../../.github/workflows/openapi-generate.yml)). This is a **contract**: an agreement other code relies on, enforced socially and by tooling rather than by the compiler.
- Plugin-facing interfaces in `MediaBrowser.Controller`/`MediaBrowser.Common` — third-party plugins compile against these. [BannedSymbols.txt](../../BannedSymbols.txt) and the compat CI job ([ci-compat.yml](../../.github/workflows/ci-compat.yml)) police this surface.
- The SQLite schema — shared with nothing external, but *its own past*: EF migrations mean every past version must upgrade cleanly.

**Private (safe to refactor):** everything inside `*.Implementations` classes that isn't an interface member; controller helper methods; the internals of repositories.

Senior noticing: the *two* implementation projects (`Emby.*` legacy vs `Jellyfin.*` modern) are a **strangler-fig migration** frozen mid-motion — new subsystems land in `Jellyfin.Server.Implementations`, old ones stay put until touched. When you see duplicated concepts in a codebase, ask "which direction is the migration flowing?" before judging it.

## Interview angle

- *"How do you approach a large unfamiliar codebase?"* — describe exactly this process: entry point → DI wiring → middleware order → one endpoint traced to the DB → test layout. Name the artifacts you'd produce (this map).
- *"How do you enforce architectural boundaries?"* — project references as compile-time walls; banned-symbol analyzers; generated-spec diffs in CI as contract tests.

## Drill

Without looking at this page, draw the dependency arrows between `Jellyfin.Api`, `Jellyfin.Server`, `MediaBrowser.Controller`, `Emby.Server.Implementations`, and `MediaBrowser.Model` from memory. Then verify by opening two `.csproj` files and reading their `<ProjectReference>` items.
Self-grade — Basic: got the API→Controller→Model chain. Solid: knew `Jellyfin.Server` is the composition root that references everything. Strong: can explain *why* `MediaBrowser.Model` must sit at the bottom (client-shared DTOs cannot drag server dependencies with them).
