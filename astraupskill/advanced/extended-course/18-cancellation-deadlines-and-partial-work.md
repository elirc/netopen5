# 18. Cancellation, deadlines, and work that has already happened

The latest-media action is synchronous in the inspected source. It calls synchronous user, view, and DTO interfaces, while some lower branches synchronously wait for asynchronous operations. Read [the controller](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), [the channel branch in UserViewManager](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs), and [live-TV enrichment in DtoService](../../../jellyfin/Emby.Server.Implementations/Dto/DtoService.cs). This chapter treats cancellation support as a proposed engineering change, not a capability inferred from the fact that the server handles HTTP requests.

The objective is to distinguish a caller losing interest, a deadline expiring, an operation observing cancellation, and all work stopping. Those events can happen at different times. A precise proposal names the token path, the observation points, and the response behavior without claiming that cancellation reverses completed reads or external work.

## Trace the current synchronous boundary

GetLatestMedia has no CancellationToken parameter. Its current calls to GetLatestItems and GetBaseItemDtos do not pass a request-aborted token. In the channel-parent branch, UserViewManager calls an asynchronous channel method with CancellationToken.None and waits through GetAwaiter().GetResult(). In the selected DTO service path, live-TV program enrichment also synchronously waits for an asynchronous method.

These statements identify specific propagation gaps in this path. They do not prove that no lower component has its own timeout or cancellation mechanism. Such mechanisms would need separate source inspection. Equally, the presence of asynchronous work lower down does not make the action itself cooperatively cancellable through the HTTP request token.

Avoid turning a source review into an unmeasured performance verdict. Synchronous waiting can be a design concern, but its operational impact depends on workload, implementation, and scheduling. A proposed improvement should preserve correctness and measure the relevant path rather than assuming that adding async to a method name makes all work cheaper or interruptible.

## Define cancellation ownership

A request-aborted token represents the connection or caller's request lifetime. A service timeout represents a component's own budget. A user-interface cancel button may only stop displaying a result unless it is wired through the client and server. These are related but distinct signals. A proposal should say which one governs each operation and whether tokens are linked.

Suppose the client disconnects after candidate retrieval but before DTO enrichment. The server may already have performed user lookup, library reads, grouping, and allocation. Canceling later enrichment cannot undo those completed costs. The useful goal may be to avoid additional expensive work, not to promise that the abandoned request consumed nothing.

For a read endpoint, cancellation generally concerns resource use and response completion rather than rolling back domain writes in the selected action. Nevertheless, lower collaborators may have caches, lazy initialization, or external calls. Do not assume every read is effect-free internally without inspection. State the scope of the proposed guarantee narrowly enough to verify.

## Separate deadlines from input limits

The existing integer guard prevents invalid or overflow-risk limits, and the grouping threshold bounds output groups. Neither is a time budget. A request within the arithmetic range can still be expensive because of candidate retrieval, image metadata, user data, or live-TV enrichment. Conversely, a small request can exceed a deadline if a dependency is slow.

A proposed deadline policy must define what happens on expiry: reject with a specific error, return a documented partial result, or abandon the response. Partial results create additional contract questions about ordering, count meaning, and whether omitted DTOs preserve correspondence. Do not silently truncate a mapped array and continue positional count restoration without reviewing its assumptions.

A lower operational maximum and a deadline can complement one another, but they solve different problems. The capstone later asks for a compatibility review when proposing such policies. This chapter focuses on making the cancellation path testable before making a public promise about latency or maximum work.

## Design an end-to-end token path on paper

A coherent proposal might make the action asynchronous, accept a request token, add token-aware asynchronous view and DTO interfaces where needed, and pass the token into actual I/O calls. Each interface change has callers beyond this endpoint, so inventory them before implementation. A signature change alone is incomplete if a collaborator still uses CancellationToken.None or blocks on an operation that ignores the signal.

Define observation points around candidate retrieval, grouping, DTO batch work, and enrichment. CPU-only grouping may need an occasional cancellation check if its input can be large, but check frequency is a design tradeoff rather than a magic guarantee. Tests should verify that the intended stage stops starting new work after cancellation and that already completed stages are reported honestly.

Do not use Task.Run merely to hide synchronous blocking without analyzing resource ownership and the underlying I/O API. Moving work to another thread does not make an uncancellable dependency honor the request token. It can also change scheduling and exception behavior. A source-grounded proposal should identify the actual asynchronous methods available and their contracts.

## Build a controlled cancellation fixture

Use collaborator gates rather than arbitrary sleeps. A candidate provider can signal that it has started and wait on an explicit test-controlled completion source. The test cancels the token at a known point and then releases or observes the dependency according to the proposed contract. This makes ordering reproducible and gives the failure a precise stage.

Track calls that started and calls that completed separately. If user lookup completed before cancellation, its completed count remains one. If DTO mapping never starts, its start count should remain zero. If enrichment starts and observes cancellation, record that outcome separately from normal completion. A single total-call counter cannot explain these distinctions.

The current synchronous action cannot be assumed to satisfy this proposed fixture without interface changes. Keep the test plan labeled as future behavior. The existing direct-action tests remain characterization evidence for current guards and forwarding, not proof of an unimplemented cancellation feature.

## Reason about response-started behavior

ExceptionMiddleware has a branch that rethrows when the response has already started rather than replacing it with its ordinary error response. A cancellation-related failure late in serialization or streaming therefore cannot always become a clean new status and body. A proposal that promises a structured cancellation response must identify whether headers or bytes have already been sent.

The latest action returns an enumerable view of the DTO list after mapping; actual result execution and serialization happen later in the framework. A direct action test observes the returned result object, not the timing of bytes sent to a client. Hosted tests are needed to study response-started behavior and client disconnects at that boundary.

Do not interpret a canceled client task as proof that the server stopped. The client can stop waiting while server-side work continues. Conversely, server cancellation can occur after useful work completed but before a response was delivered. A diagnostic receipt should identify which side observed the signal and which artifacts were collected.

## Preserve exception meaning

A cancellation proposal should decide how expected cancellation is logged and surfaced without conflating it with invalid input, missing users, or security failures. Catching every exception and returning an empty list would hide both legitimate failures and implementation defects. An empty latest list has a meaningful successful interpretation and should not become a generic failure sentinel without an explicit contract change.

Similarly, converting every timeout into a retryable result can create load amplification if clients retry immediately. Define retry guidance and backoff at the appropriate client or protocol boundary. The course does not prescribe a universal policy; it asks for a concrete one whose deterministic failures are not retried unchanged and whose transient failures have bounded recovery behavior.

Keep logs free of live tokens and unnecessary user details. A synthetic request correlation ID, stage name, elapsed duration, and cancellation origin can be enough for a bounded experiment. Diagnostic precision comes from stage separation, not from dumping every request header or exception object into a shared report.

## Compare three failure timelines

Timeline one cancels before candidate retrieval starts. Under a proposed token-aware contract, later query and DTO work should not start. Timeline two cancels after groups are selected but before DTO enrichment; selection costs already occurred, while later work may be avoided. Timeline three cancels after a normal result object is returned but during response execution; direct-controller evidence is insufficient to predict the client's final body.

For each timeline, record signal source, first observer, started stages, completed stages, result or exception, and evidence boundary. This table prevents the phrase canceled successfully from hiding whether the server, a mock, or only the client stopped. It also exposes which parts of the current implementation would need changes before the proposed behavior could be verified.

## Independent exercises

Exercise JF-18A asks you to draw the current token path and mark where no request token is passed. Explain the channel branch's CancellationToken.None and the difference between synchronous waiting and asynchronous propagation. State which lower timeout behavior remains uninspected.

Exercise JF-18B asks you to design a gate-based fixture for cancellation between selection and DTO work. Include started and completed counters, a positive noncanceled control, and an assertion that distinguishes caller abandonment from server cooperation. Keep it explicitly proposed behavior.

Exercise JF-18C asks you to specify a deadline response policy and analyze the three timelines above. Include the response-started limitation, retry consequences, and the difference between output limits and time budgets. Use the final reviews only after writing your own causal trace.

## Review checkpoint

A complete answer can say exactly which work cancellation is intended to prevent and which work may already have happened. It does not claim universal cancellation from a token-bearing signature, does not treat empty results as generic errors, and gives a reproducible experiment for every proposed propagation change.


[Separate hints and full review](review-04-consistency-labs-properties-and-capstones.md) | [Complete course route](README.md)
