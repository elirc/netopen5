# 01 — Codebase Cartography

Before you can change a system safely you must know its shape: what owns what, where the public surface is, and which paths carry the load. This module builds that map for Jellyfin and teaches the transferable skill of building the same map for any repo in your first week on a job.

| File | What it gives you |
| --- | --- |
| [01-system-map.md](01-system-map.md) | Project layout, ownership map, public vs private surfaces |
| [02-file-reading-order.md](02-file-reading-order.md) | 30 files in reading order with junior/mid/senior paths |
| [03-domain-glossary.md](03-domain-glossary.md) | Domain nouns (BaseItem, Provider, Session…) with code locations |
| [04-runtime-and-tooling-map.md](04-runtime-and-tooling-map.md) | SDK, build, test, run, config and env-var surfaces |
| [05-key-flows.md](05-key-flows.md) | **The core asset**: 8 end-to-end flows with trace tables and drills |

Interview note: "walk me through a codebase you know" is a standard mid-level screen question. The system map plus any two key flows *is* your answer.
