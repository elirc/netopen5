# Choose the evidence layer before writing the test

## Placement questions

What is the largest positive signed 32-bit integer that can be doubled without overflow? Why does returning 400 after querying the library fail the “reject before work” requirement? How does a C# call that omits an optional argument differ from a call explicitly passing its current default? Which part of query-string binding does either call test?

If any answer is unclear, complete the boundary trace first. These questions separate the contract from the convenience of a familiar testing tool.

## Read the narrow source path

The [UserLibraryController](../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs) declares `[Authorize]`, the current `Items/Latest` route and a compatibility route under `Users/{userId}/Items/Latest`. Find `GetLatestMedia`, its initial limit guard, user lookup, filter handling, `LatestItemsQuery`, DTO conversion and legacy delegation.

The downstream [UserViewManager](../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs) contains `Limit = limit * 2` in candidate querying. The [base controller](../../jellyfin/Jellyfin.Api/BaseJellyfinApiController.cs) supplies API-controller behavior and a typed result subclass. The [focused tests](../../jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs) use strict collaborators and invoke the real controller method.

## Reproduce focused controller checks

From the outer `netopen5` folder, use PowerShell:

```powershell
Push-Location jellyfin
try {
    dotnet --version
    dotnet test tests/Jellyfin.Api.Tests/Jellyfin.Api.Tests.csproj `
      --filter FullyQualifiedName~UserLibraryLatestMediaTests `
      --nologo --verbosity minimal /m:1 --logger trx
} finally {
    Pop-Location
}
```

Inspect [global.json](../../jellyfin/global.json) if SDK selection fails. This command may restore and build; `--no-restore` is appropriate only after successful restoration. A build failure is not a failed controller assertion. Retain the actual discovered test summary and distinguish parameterized cases from repeated runs of the same case.

This is a learner reproduction command, not a claim that the documentation expansion reran the .NET suite. Earlier results are recorded in [verification](../VERIFICATION.md).

## Evidence ladder

| Layer | What it can establish | What it does not establish by itself |
|---|---|---|
| Arithmetic worksheet | Correct threshold and expected branches | Actual C# implementation or server behavior |
| Direct controller test | Guard, forwarded query, collaborator calls, action result | Route selection, query parsing, authentication middleware |
| Owned HTTP test host | Configured routes/binding/middleware and serialized response | Real media selection or deployment capacity |
| Controlled integration environment | Its configured library and services | Every production workload or permission configuration |

Choose the smallest layer that can establish the claim you are making. Higher layers complement lower ones; they do not make a small precise unit assertion unnecessary. Your session plan should state which layer each deliverable uses and what remains outside it.
