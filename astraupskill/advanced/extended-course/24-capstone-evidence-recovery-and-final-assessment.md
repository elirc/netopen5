# 24. Capstone: evidence, recovery, and a final engineering assessment

The final capstone asks you to investigate a latest-media behavior and propose a recovery contract without overstating the evidence. Choose a count-correspondence incident or a canceled-request workload incident. Both tracks use the real [controller](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), [view manager](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs), [DTO service](../../../jellyfin/Emby.Server.Implementations/Dto/DtoService.cs), and [exception middleware](../../../jellyfin/Jellyfin.Api/Middleware/ExceptionMiddleware.cs). The course supplies the assignment and rubric; it does not implement a server change.

By the end, your packet should let another engineer distinguish current source behavior, an executed bounded reproduction, a proposed improvement, and unverified host or production assumptions. The quality of that distinction matters more than the size of the packet or the number of unrelated tests listed.

## Track A: a count appears on the wrong representative

Begin with a report that a container's collected count appears beside another item's metadata. Do not assume the controller or mapper is defective. Build a synthetic fixture with distinct representative IDs and deliberately different positive counts. Record the candidate list, groups, selected representatives, count vector, mapper input IDs, mapper output IDs, and final DTO fields.

The current controller restores by index, and the selected real mapper path preserves index correspondence. A collaborator that reorders DTOs violates that boundary contract. Your first task is to determine whether the reported mismatch occurs before selection, during mapping, during restoration, or in client presentation. A direct fixture can isolate some of those stages while leaving real serialization and UI behavior unexecuted.

Propose either stronger contract assertions, an identity-keyed restoration design, or a narrower diagnostic improvement. If choosing identity-keyed restoration, define duplicate IDs, missing DTOs, and extra outputs explicitly. Do not assume a dictionary solves every correspondence problem. The proposal must preserve the meaning of zero recorded counts and singleton albums.

## Track B: a canceled request continues expensive work

Begin with a client that stops waiting while server-side enrichment appears to continue. The current action has no request token parameter, and selected lower branches use synchronous waiting or CancellationToken.None. These source facts motivate a proposed cancellation path but do not quantify production cost or prove every dependency ignores cancellation.

Design a controlled gate-based fixture that cancels after selection and before a chosen enrichment stage. Record work started, work completed, cancellation observed, and response boundary separately. A canceled client task alone is insufficient evidence that the server cooperated or failed to cooperate. Hosted disconnect behavior is another experiment beyond direct collaborator tests.

Propose a token-aware path with explicit interface changes and observation points. Include noncanceled success controls and a policy for response-started failures. Do not catch every exception and return an empty list, because that would confuse a successful empty latest result with failure. Keep timeout policy, caller abandonment, and invalid input as different categories.

## Deliver a five-column claim ledger

Each row contains a claim, source anchor, experiment, observation, and limitation. For track A, one row can state that the controller uses positional count restoration, another that a specific mapper fixture reorders outputs, and another that a hosted response has a particular serialized mismatch. Those rows require different observations and should not borrow evidence from one another.

For track B, separate the client's cancellation signal, the server's observed token state, the collaborator's started count, its completed count, and the final response. A single log message saying canceled cannot establish all five. The ledger should make it easy to see which claims are source-derived and which were actually executed.

Use synthetic identities and stage labels. Do not include live access tokens, personal media names, complete user playback histories, or unnecessary filesystem paths. A minimal reproduction should preserve algorithmic shape while removing irrelevant real-world details. This improves both reviewability and the ability to share the packet safely.

## Build an independent oracle

For track A, write the expected ordered identity sequence and count vector before invoking the code. Seed zero-count positions with nonzero mapper values so preservation is visible. Capture the mapper input and output independently rather than comparing two references to the same mutable list after modification. Include a correct mapper control and an intentionally reordered mapper case.

For track B, use explicit gates and counters rather than fixed sleeps. Specify which stage should never start after cancellation and which earlier work is allowed to have completed. A test that merely observes an exception without checking stage work can pass while expensive work continues unnecessarily. A test that expects no work at all after a late signal asks for an impossible reversal of completed stages.

The oracle must express the proposed contract, not mirror the implementation's exact condition in another helper. Use tables, expected IDs, and explicit stage outcomes. If a proposed implementation changes the contract, update the specification through review rather than silently changing expected values until tests pass.

## Add a mutation that defeats a weak test

For track A, use a mutation that preserves response length but swaps mapper order, or one that overwrites zero count positions. A length-only assertion passes while correspondence or preservation fails. The stronger oracle should identify the wrong ID/count pairing or lost mapper value.

For track B, use a collaborator that records cancellation but still starts a later expensive stage. An exception-only assertion can pass while the work contract fails. The stronger oracle checks started and completed counters at the named gates. Keep this mutation confined to an owned test fixture or generated copy, not a real external service.

Record build and semantic outcomes separately. If a signature change prevents compilation, the intended behavior was never exercised. If a fixture deadlocks before the cancellation point, the timeout is a setup failure rather than proof of server noncooperation. A useful mutation receipt names the assertion that distinguishes the defect.

## Define recovery without hiding the original failure

A client recovery proposal should distinguish deterministic invalid input, missing subject, forbidden subject, and transient dependency failure. Repeating an unchanged invalid limit or forbidden subject is not a useful recovery strategy. A transient read retry may be appropriate, but its response can differ because latest media changes over time.

For track A, a client should not repair count mismatches by guessing from a displayed list unless that is an explicitly chosen presentation contract. Report the mismatch or use a documented field meaning. For track B, retry budgets and backoff should avoid amplifying an overloaded dependency. The course does not prescribe a universal retry count; it requires a bounded policy tied to the failure category.

Do not rely on development-only exception text as a stable machine-readable signal. ExceptionMiddleware normalizes development messages and uses a generic message otherwise. A structured recovery protocol would be a proposed API change with compatibility tests, not a property of the current plain-text path merely because a client wants it.

## Prepare the reviewer packet

Lead with the observed mismatch or proposed work guarantee. Follow with the minimal fixture, exact source boundary, strongest executed result, and remaining limits. Include the current behavior and desired behavior in concrete terms. Avoid a chronological transcript of every exploratory command; reviewers need the causal argument and reproducible artifacts.

A design-only packet can be complete without application edits when its contract, experiment, and acceptance criteria are concrete. An implementation packet needs executed evidence for the changed interfaces and behavior. If full project assets or a hosted environment are unavailable, state that limitation rather than relabeling an extracted-source lab as a server test.

Preserve original source and learner work during bounded experiments. The delivered lab hashes its two selected originals and generates code only in a uniquely owned temporary directory. A later learner implementation belongs in its own deliberate workflow. The course does not make commits, publish changes, or modify the application as part of this assessment.

## Sixty-point capstone rubric

Award twelve points for a precise chosen incident and proposed contract with accurate source anchors. Award twelve for an independent oracle that separates identity/count correspondence or started/completed work. Award ten for a minimal reproducible fixture with positive controls and explicit observation boundaries.

Award ten points for a discriminating semantic mutation and correct failure-stage interpretation. Award eight for recovery and compatibility reasoning that distinguishes deterministic and transient failures. Award eight for a concise evidence packet with exact executed results, preservation scope, and honest unverified boundaries. The maximum is sixty points, separate from the first capstone's rubric and the chapter preparation exercises.

Do not award hosted-execution credit for direct action invocation, full-project-build credit for an SDK-only extraction, or cancellation-propagation credit for a canceled client task alone. Those are material category errors. A technically limited but accurately described result is more useful than an impressive claim built on the wrong evidence boundary.

## Final course assessment

The complete route now covers input arithmetic, identity, nullable intent, options, retrieval branches, grouping, representation, DTO correspondence, binding, errors, consistency, cancellation design, diagnostics, bounded execution, properties, compatibility, and independent capstones. Each topic is connected to local source or explicitly marked as a proposed extension.

You should be able to explain why a collected child count is not a complete library total, why larger limits can change representative identity, why a read retry can return different media, and why positional restoration depends on mapper correspondence. You should also be able to name the difference between a source prediction, an extracted algorithm run, a direct controller test, and a hosted request.

Optional future work includes implementing a capstone, restoring and running the full project's focused tests in an owned environment, adding hosted binding and middleware tests, and measuring a controlled operational policy. These are extensions beyond the completed instructional route. No required chapter remains a planned placeholder, and no proposed feature is represented as shipped application behavior.

## Independent preparation exercises

Exercise JF-24A asks you to choose a track and write five claim-ledger rows at distinct evidence boundaries. Include one tempting overclaim and replace it with a supported statement plus a concrete next experiment.

Exercise JF-24B asks you to design the independent oracle, a positive control, and a semantic mutation that defeats a weaker test. Explain how you will distinguish compiler failure, fixture timeout, assertion failure, and hosted response evidence.

Exercise JF-24C asks you to write a reviewer decision for a complete design-only packet and an implementation packet missing its hosted evidence. State what is complete, what remains unverified, and which next check would resolve the gap. Use the final review guide after writing your own assessment.

## Review checkpoint

You finish the course when you can make a precise engineering claim, support it at the right boundary, and describe the next useful experiment without exaggerating what already ran. The capstones reward that discipline alongside correct code and concrete tests.


[Separate hints and full review](review-04-consistency-labs-properties-and-capstones.md) | [Complete course route](README.md)
