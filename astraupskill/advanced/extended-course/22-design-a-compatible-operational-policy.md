# 22. Design a compatible operational policy

The current limit guard protects a specific arithmetic boundary. A product team might later want a much smaller operational maximum, a response-cost budget, or clearer error metadata. This chapter develops that proposal without implementing it. Read [GetLatestMedia and its legacy delegate](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), [the view-manager branches](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs), and [ExceptionMiddleware](../../../jellyfin/Jellyfin.Api/Middleware/ExceptionMiddleware.cs). The existing behavior remains the baseline against which compatibility is assessed.

The objective is to write a change that reviewers and clients can reason about. A resource policy is not just a new constant. It changes which previously representable requests succeed, how clients recover, and potentially which response counts or fields they receive. Treat those consequences as part of the contract.

## Separate three policy goals

Arithmetic safety ensures that a calculation remains within its intended integer range. An operational item maximum constrains requested work more aggressively. A response-cost budget accounts for options, item types, or enrichment that can make equal item counts have different costs. These goals can coexist, but one does not automatically satisfy the others.

The current guard accepts positive limits through half the maximum signed integer because a retrieval path initially doubles the value. That arithmetic ceiling is not evidence that a request near it is operationally reasonable. Conversely, lowering the ceiling does not automatically bound image metadata, user-data batch work, or serialized bytes for every item.

A proposal should identify the measured problem before choosing a mechanism. If the dominant cost is expensive DTO fields, a uniform item cap may help only partially. If the problem is oversized candidate retrieval, an output-only truncation after mapping is too late. Place the policy at the earliest boundary that can evaluate it accurately without changing identity or error precedence unintentionally.

## Choose rejection, normalization, or partial output explicitly

One policy rejects limits above a documented maximum. Another clamps them to that maximum. A third accepts the requested limit but returns fewer results under a budget. These are different client contracts. Silent clamping can make a request appear successful while hiding that its requested bound was changed. Partial output can be indistinguishable from a naturally short latest list unless metadata explains the reason.

For a rejected request, specify status, body shape, and whether the rejection happens before identity resolution and service calls. Preserving the current guard's early-work behavior may be desirable, but a new policy that depends on user tier or library type cannot necessarily be evaluated at the same point. State the tradeoff rather than assuming every guard can remain first.

For normalization, specify the effective limit returned or observable to clients. For partial output, define ordering, group membership, and count semantics at the truncation boundary. Truncating DTOs after positional restoration differs from stopping grouping earlier. The proposal must say which stage owns the budget and what the final counts mean.

## Preserve defaults and omission semantics

The action's default limit is twenty and default grouping is true. Nullable played intent can be filled from the selected user's preference, while an explicit value remains explicit. Optional DTO flags also have their own defaulting logic. A policy change should not accidentally convert omission into an explicit false or replace a subject user's preference with the authenticated caller's preference.

A compatibility matrix should include omitted parameters, explicit defaults, ordinary nondefault values, the new proposed boundary, and values between the new boundary and the old arithmetic ceiling. These last requests are where the new policy intentionally changes acceptance. Record that behavior change instead of calling it fully backward compatible.

Do not infer real client usage from the existence of a parameter. If deployment data is needed to estimate impact, collect an appropriately scoped aggregate measurement through an authorized operational process. This course does not access production traffic or logs. The design can identify the evidence needed without inventing usage percentages.

## Include both route shapes

The legacy latest-media route delegates to the current action with the same arguments. A shared policy in the current action can therefore affect both routes. That is useful for consistency, but it also means clients using the old path experience the new acceptance rules. Hiding the legacy route from API discovery does not remove its compatibility responsibility.

A proposed test suite should compare both entry points for the new boundary, defaults, and representative output. Direct delegate tests establish shared action behavior, while hosted route tests establish binding and public response equivalence. Keep those evidence levels separate. The course's existing direct fixtures do not automatically prove every route-level serialization detail.

If the policy must differ by API version, do not smuggle that difference into a legacy wrapper without documentation. Define version negotiation, deprecation behavior, and migration guidance. A simple shared implementation is often preferable, but the choice should follow the stated compatibility requirement rather than convenience alone.

## Design an error contract clients can use

The current limit guard returns a bad-request result with a message. ExceptionMiddleware has its own plain-text behavior for exceptions and environment-sensitive details. A proposed structured error format must distinguish direct action rejection from middleware-translated exceptions and decide how both fit the public API.

Machine-readable fields might identify the invalid parameter, supported range, and stable error code. Those are design options, not current fields added by this course. If adopted, tests should assert the stable fields while allowing diagnostic text to evolve. A client should not depend on development-only exception wording as its retry signal.

Compatibility includes content type and body shape, not just status. Replacing a string body with an object can break a client that reads text in a specific way. A migration plan should identify whether the change is versioned, negotiated, or documented as a breaking contract. Do not claim that keeping status 400 makes every response-format change harmless.

## Budget options without guessing their complete cost

DtoService performs option-dependent batches for user data, child counts, and other fields, plus type-dependent enrichment. A proposed option budget can classify known expensive profiles, but a complete cost model requires measurement and continued maintenance. Avoid presenting a hand-assigned weight table as a proven latency predictor.

A bounded experiment can compare a few synthetic profiles while holding candidate shapes constant. Record representative identities and correctness assertions alongside timing and batch counts. If a faster profile omits required fields, it is a different response contract rather than a free optimization. The policy should tell clients which fields are optional and what omission means.

Caching can reduce repeated work but introduces user, preference, parent, type, grouping, and option dimensions. The earlier course identified those key questions. This proposal should also address freshness and invalidation: a budget cache that returns stale selected groups may change consistency behavior. Do not add caching solely to avoid specifying a clear operational maximum.

## Plan rollout as an experiment, not a promise

A reviewable rollout plan defines the intended policy, expected client impact, observable metrics, and a rollback or revision criterion. For example, track rejection counts by requested-limit bands and compare bounded server work before and after in an authorized environment. Use aggregate measurements that answer the policy question without collecting unnecessary media identities or user content.

The course does not deploy such a policy. Its deliverable is the plan and acceptance suite. A later implementation should include exact changed paths, executed tests, and any unverified production assumptions. Avoid claiming that a proposal prevents all expensive requests when it only constrains one dimension.

Rollback also has a contract dimension. Removing a newly introduced cap may restore acceptance but not reverse client adaptations or response-format changes. Keep the policy and error-schema changes separable when possible so reviewers can assess their risks independently. A small coherent patch is easier to validate than a combined cap, cache, async rewrite, and error redesign.

## Build the compatibility acceptance matrix

Use rows for default request, smallest valid request, proposed maximum, one above proposed maximum, old arithmetic maximum, invalid zero, and an explicit played filter differing from preference. Add current and legacy routes, ordinary and specialized retrieval branches, and lean versus richer DTO options as separate dimensions where relevant.

For each row, state old behavior, proposed behavior, expected service-call counts, and evidence layer. Do not actually allocate an enormous library for the arithmetic maximum; use a mock or isolated guard fixture. Operational benchmarks should use modest controlled sizes. The matrix can therefore combine different test boundaries without pretending one fixture executes everything.

A strong proposal also states what remains unchanged: representative selection, positive-only count restoration, subject identity rules, and explicit nullable-filter intent unless the change deliberately revises them. These are regression contracts relevant to the policy, not a generic promise that no other behavior can ever differ.

## Independent exercises

Exercise JF-22A asks you to choose a proposed operational maximum and justify its role separately from arithmetic safety and option cost. Compare rejection, clamping, and partial-output policies, then select one with exact client-visible behavior and an early-work rule.

Exercise JF-22B asks you to build the compatibility matrix for both route shapes, including omitted parameters and values accepted by the old arithmetic range but rejected by your proposal. Identify which tests can remain mocked and which need a hosted response observation.

Exercise JF-22C asks you to design stable error fields and a rollout evidence plan without claiming production measurements you do not have. Explain body-shape compatibility, deterministic versus transient retries, and one rollback limitation. Consult the separate review after committing your proposal.

## Review checkpoint

A complete policy proposal makes its intentional behavior changes visible, uses measurements to justify scope, and preserves unrelated selection contracts through tests. It does not call an operational cap arithmetic validation, silently truncate results, or treat a draft rollout plan as a deployed safeguard.


[Separate hints and full review](review-04-consistency-labs-properties-and-capstones.md) | [Complete course route](README.md)
