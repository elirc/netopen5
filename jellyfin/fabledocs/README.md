# Jellyfin as a Training Lab: Codebase-to-Curriculum

A complete learning suite that turns the Jellyfin server codebase into a structured path from **junior CRUD developer** to **mid-level fullstack engineer with senior judgment** — and into a portfolio of concrete, evidence-backed interview answers.

## Who this is for

A junior fullstack engineer (C#/.NET, React/Node/TS, or similar CRUD web background) who wants to:

1. Learn how a large, real production codebase is shaped and why.
2. Build transferable judgment — the ability to recognize the same patterns in *any* repo.
3. Pass interviews for mid-level fullstack roles using this repo as a portfolio of talking points.

Every module teaches two things at once: **where things live in Jellyfin** and **why the pattern exists anywhere**. Interview readiness is a first-class goal — most pages end with an "Interview angle."

## What Jellyfin is (the repo's identity in 7 sentences)

Jellyfin is a free, self-hosted media server — the open-source alternative to Plex/Emby — and this repository is its **backend server** only (the web client lives in the separate [jellyfin-web](https://github.com/jellyfin/jellyfin-web) repo). It is a .NET 10 / ASP.NET Core application ([README.md](../README.md#L79)) exposing a large REST API (59 controllers in [Jellyfin.Api/Controllers](../Jellyfin.Api/Controllers)), WebSocket real-time messaging, and HLS video streaming backed by ffmpeg transcoding. Media metadata is stored in SQLite through EF Core ([src/Jellyfin.Database](../src/Jellyfin.Database)), with a hybrid model: relational columns for queryable fields plus a serialized JSON blob per item. It descends from Emby 3.5.2, so it carries visible **legacy seams** — project names like `Emby.Server.Implementations`, a custom token auth scheme bridged into ASP.NET Core, and two parallel migration systems. Background work (library scans, transcodes, cleanup) runs through a custom scheduled-task engine with triggers and progress reporting. It is multi-user with per-user permissions, parental controls, and network-based access rules — a real authorization surface, not a toy one. That mix of modern ASP.NET Core idioms and battle-scarred legacy makes it an unusually honest teaching codebase: you see both what good looks like and what technical debt looks like when it's managed responsibly.

## The learning tracks

| Track | Folder | What you get |
| --- | --- | --- |
| Cartography | [01-codebase-cartography](01-codebase-cartography/README.md) | System map, reading order, glossary, 8 traced key flows |
| Stack mastery | [02-stack-and-language-mastery](02-stack-and-language-mastery/README.md) | C#/.NET async model, ASP.NET Core mental models, type-system contracts, build tooling |
| Architecture | [03-architecture-and-patterns](03-architecture-and-patterns/README.md) | Layer boundaries, data model, auth mapping, async reliability, 14 pattern cards, critique |
| Reading gym | [04-code-reading-gym](04-code-reading-gym/README.md) | Annotation drills, trace tables, fake-code contrasts, review katas |
| Quality | [05-quality-engineering](05-quality-engineering/README.md) | Testing strategy, test recipes, debugging method, performance, security, observability |
| Contribution | [06-contribution-practice](06-contribution-practice/README.md) | Junior tickets, mid-level features, senior projects, refactor katas |
| Career | [07-career-and-collaboration](07-career-and-collaboration/README.md) | Review mindset, PR/RFC writing, maintainer communication |
| **Interview prep** | [08-interview-prep](08-interview-prep/README.md) | 45+ question cards anchored to this repo, system-design walkthrough, STAR stories, 2-week cram plan |
| Reference | [09-reference](09-reference/) | Command cheatsheet, risk register, rubrics, verification log |

## Recommended paths

- **One weekend** → [00-fast-track.md](00-fast-track.md). Run it, trace two flows, make one safe change.
- **Two weeks** → Fast track, then 01 (all), 03/01–03, 04/01–02, 05/03, and skim 08.
- **Eight weeks** → All tracks in order; do every drill; ship one ticket from 06 per week from week 3.
- **Ongoing contributor** → 06 + 07 as your main loop; 05 as your pre-PR checklist.
- **Brand-new junior** → 00 → 01 → 02 → 04 (drills before architecture theory).
- **Junior who knows .NET** → 00 → 01/05-key-flows → 03 → 04 → 05.
- **Mid-level, new to this repo** → 01/01, 01/05, 03/05-pattern-catalog, 03/06-critique, 06/02.
- **Senior doing architecture review** → 03/06-architecture-critique + 09-reference/risk-register.md.
- **Interview in two weeks** → [08-interview-prep/07-two-week-cram-plan.md](08-interview-prep/07-two-week-cram-plan.md), fed by 01/05-key-flows and 03/05-pattern-catalog.

## Conventions used throughout

- **File anchors**: every claim about this codebase links to a real file and line range, e.g. [RequestHelpers.cs#L67-L85](../Jellyfin.Api/Helpers/RequestHelpers.cs#L67-L85). Line numbers were verified against the working tree at writing time (July 2026); if the code has moved since, search for the symbol named in the text.
- **Fake code is labeled**: any snippet not from this repo starts with `// Illustrative fake code: not from this repo`. Everything else is real.
- **Verification labels**: commands are marked __verified__ (run during authoring) or __inferred__ (read from config/scripts but not executed). Uncertain behavioral claims say "investigate" or "possible risk" — they are hypotheses, not bug reports. See [09-reference/verification-log.md](09-reference/verification-log.md).
- **Drills and self-grading**: exercises come with Basic / Solid / Strong rubrics. Grade yourself honestly; "Strong" is the mid-level interview bar.
- **Senior vocabulary** (also interview vocabulary): *invariant, boundary, contract, ownership, idempotency, isolation, authorization, consistency, latency, observability, migration, rollback, blast radius*. Each is defined in context the first time a module uses it seriously.

## The mindset ladder

- **Junior asks:** "How do I make it work?"
- **Mid-level asks:** "Is this the right pattern? What does it cost? What breaks it?"
- **Senior asks:** "What does this commit us to, who pays that cost over time, and how do we reduce the risk?"

Mid-level interviews test exactly the second and third questions. When an interviewer says "tell me about pagination," they are not asking for a definition — they want to hear you say something like: *"Jellyfin's `/Items` endpoint takes `startIndex`/`limit` and makes the expensive total count opt-out via `enableTotalRecordCount` — offset pagination is fine there because a personal media library is small, but I'd reach for cursor pagination on an unbounded multi-tenant feed."* That sentence contains a concrete example, a tradeoff, and a scaling limit. This curriculum exists to fill your head with fifty sentences like it.
