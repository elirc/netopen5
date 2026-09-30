# Review 04: consistency, bounded execution, and independent capstones

This guide supplies hints and full reasoning for the twenty-four exercises in chapters 17-24. Attempt each exercise before reading its answer. The complete course contains seventy-two chapter exercises, with the earlier forty-eight reviewed in guides 01-03. The two capstones have separate sixty-point rubrics; their assessment points do not turn the preparation exercises into additional capstones.

## Hints before full answers

For chapter 17, separate selected identity from metadata freshness and write the meaning of each count. A shared options reference does not create a transactionally frozen library snapshot. A representative can be a parent even when retrieval operates on children.

For chapter 18, draw every token argument actually present and mark completed work before the signal. A synchronous wrapper around asynchronous work is not automatically request-cancellable. Client cancellation and server cooperation require different observations.

For chapter 19, turn a vague symptom into an ordered identity and count mismatch. Seed mapper values deliberately and use a stage ledger with units. A grouped child represented by its parent is not absent in the same sense as a candidate never retrieved.

For chapter 20, identify extracted code and stand-ins separately. The lab executes real grouping, representative selection, and restoration statements, but not retrieval, identity resolution, DTO service internals, or a web host. Build success must precede interpretation of semantic failures.

For chapter 21, challenge properties with three-item counterexamples. Idempotence can hold for a wrong overwrite algorithm, so pair it with independent preservation assertions. Keep the generator's valid input domain explicit.

For chapter 22, make the intentional compatibility change visible. Rejecting, clamping, and partial output are different policies. A smaller operational cap is not the same thing as the arithmetic guard, and keeping a status code does not preserve every body contract.

For chapters 23-24, declare design-only or implementation scope at the start. Protect existing selection semantics while changing one contract. A complete packet tells a reviewer what ran, what was only designed, and which next experiment would resolve the remaining uncertainty.

## JF-17A: selection and decoration interleaving

With A1, A2, B1 collected into two groups, the controller selects container A and child B1 for ordinary nonalbum behavior. The recorded count vector is two and zero. Adding A3 after selection does not change that already recorded group count in the controller. DTO mapping may observe metadata at its own read boundary, but the positive override still writes two onto A's DTO and leaves B1's mapper count untouched.

The supported count meaning is collected children in the selected group, not complete current library children. This is a source-derived local trace. It does not prove how a real concurrent update is synchronized or which metadata version a database-backed mapper reads. A strong answer names both boundaries and proposes a controlled integration experiment only if a stronger freshness claim is required.

The key review criterion is whether the answer can preserve useful local guarantees without calling the response a global snapshot. Shared user and options objects align request context; they do not freeze every underlying data source.

## JF-17B: correspondence contract

A minimum local contract can require stable representative identity and order from selection into mapping, equal output cardinality, and count restoration at corresponding positions. It can separately document that metadata freshness follows the collaborators' normal reads. Positional restoration is valid under that mapper contract and is supported by the inspected skip-visibility path's indexed output array.

An identity-keyed proposal can tolerate some reordering, but must define duplicate representative IDs, missing DTOs, and extra outputs. A dictionary that silently keeps one duplicate changes the contract. The design should specify whether such cases reject, preserve original mapper values, or use a richer occurrence identity.

A good test includes a faithful ordered mapper control and an explicitly invalid reordered mapper. Do not report the latter as evidence that the real mapper currently reorders. The exercise evaluates interface assumptions and proposed resilience, not an unexecuted production defect.

## JF-17C: retries and cursors

A read retry can return different latest media because time, library contents, user data, or preferences changed. Read-only does not mean repeatable bytes across requests. The response limit is not a snapshot token. A representative ID may identify a container rather than the child candidate that determined ordering, so it is not automatically a valid cursor into candidate retrieval.

A proposed continuation protocol needs candidate ordering keys, tie handling, grouping rules across pages, treatment of new arrivals, and a freshness or snapshot policy. It also needs to define whether a container already represented on one page can appear again when later children are encountered.

Credit belongs to a concrete design question list and a small counterexample, not a generic instruction to use cursor pagination. The current course does not implement that feature or claim a stable continuation contract exists.

## JF-18A: current token path

The current action has no cancellation-token parameter, and its view and DTO calls do not receive a request-aborted token. The channel branch explicitly passes CancellationToken.None and synchronously waits for its asynchronous call. Selected live-TV DTO enrichment also uses synchronous waiting. Those are exact source observations about this path.

They do not prove that every lower dependency lacks its own timeout or that every request necessarily experiences operational harm. A proposed change must inspect actual available asynchronous APIs and propagate a signal through them. Merely renaming the action async or wrapping synchronous work in Task.Run does not establish cooperative cancellation.

A strong answer marks uninspected lower timeout behavior as unknown and distinguishes current characterization from the proposed token-aware contract. It does not claim server cooperation based on a client task being canceled.

## JF-18B: gate-based fixture

Use a selection collaborator that signals completion and a later enrichment collaborator that waits on an explicit test-controlled gate. Cancel after the first signal and before releasing the later stage. Record started and completed counters separately, then assert the proposed contract for whether enrichment may start or should observe cancellation before additional work.

Include a noncanceled control that completes normally with the expected representatives. Also include a client-abandonment observation separate from server token observation so the test cannot pass merely because the caller stopped awaiting. Avoid arbitrary sleeps as the only ordering mechanism.

This is a future-behavior fixture because the current action does not expose the proposed token path. A complete answer states the interface changes needed and does not present the design as an already passing regression test. Earlier selection work may legitimately remain completed after a later cancellation signal.

## JF-18C: deadline policy

A coherent policy specifies whether deadline expiry returns an error, abandons the response, or produces documented partial output. It names the signal source and the earliest observer. Before retrieval, later work can be avoided; after selection, selection costs already occurred; during response execution, headers or bytes may already have started and a clean replacement response may be unavailable.

The middleware's response-started branch rethrows rather than writing its ordinary replacement body. A hosted experiment is needed to establish actual disconnect and serialization behavior. An output-group limit is not a time budget, and a small request can still encounter a slow dependency.

Retry guidance should distinguish deterministic rejection from transient failure and avoid immediate load amplification. The answer should not promise rollback of completed reads or use an empty list as an unexplained cancellation sentinel.

## JF-19A: minimal count fixture

Use a multi-child nonalbum container A with children A1 and A2, a singleton nonalbum B with child B1, and a singleton album C with song C1. Expected representatives are A, B1, and C. The recorded counts are two, zero, and one. Seed mapper DTO counts with ninety-nine, eighty-eight, and seventy-seven; final counts should be two, eighty-eight, and one.

The nonzero singleton seed exposes accidental zero overwrite. Distinct representative IDs expose parent/child confusion and ordering errors. A length-only assertion or all-zero DTO initialization would miss important defects. Add candidate-order context if the fixture is produced through grouping rather than supplied directly.

The report should identify whether it executes extracted statements, a direct controller with collaborators, or the real mapper. Those are different boundaries even when the expected identity/count table is the same.

## JF-19B: competing hypotheses

For a missing item, compare retrieval exclusion with grouped representation. Capture the candidate list and group membership; an item inside a group but represented by its parent differs from one absent before grouping. A third useful hypothesis is early threshold exit, distinguished by candidate order and the first point group count reaches the limit.

For slowness, compare excessive candidates with expensive DTO enrichment. Record candidate/group counts separately from option-dependent batch calls and elapsed stage durations. One top-level mapper invocation does not mean one lower data operation, while a mock mapper's near-zero time does not represent production mapping cost.

A strong hypothesis table includes a falsifying observation for each claim. Changing user, grouping, fields, and limit simultaneously creates an ambiguous experiment. Keep comparison variables controlled and preserve correctness assertions alongside timing.

## JF-19C: smaller evidence receipt

Replace full user identifiers, media paths, and DTO dumps with synthetic labels, branch, option profile, requested and observed counts, ordered representative IDs in the fixture, and stage outcomes. Include source hashes or a known revision, the exact command, successful build status, semantic result, and unexecuted boundaries.

The smaller receipt should still answer the original question. If a field does not distinguish a hypothesis or reproduce the mismatch, it probably does not belong in the packet. Logging overhead can itself distort performance, so a proposed production instrumentation change needs a cost review rather than assuming more data is free.

A complete answer distinguishes direct action, extracted-source, and hosted evidence. It does not call any nonzero process exit a reproduced endpoint bug, and it does not expose live authentication material to make a synthetic reproduction look realistic.

## JF-20A: extracted boundary

The lab copies the real grouping method while replacing its candidate provider, and extracts representative selection plus child-count restoration from the controller. It executes dictionary grouping, early break, parent/child choice, the album exception, and positive-only overwrite. The stand-ins supply only the domain properties those statements need.

It does not execute the action's limit guard, identity helper, user lookup, private retrieval branches, real DTO service, model binder, middleware, or server. Real-source extraction is stronger than a handwritten imitation for those statements because their actual conditions compile and run, but the generated environment is narrower than application integration.

The extractor is a reviewed bounded fixture, not a general C# parser. If signatures or source block shape change, stop and review. A strong answer can describe the experiment accurately without either dismissing its useful evidence or overstating its scope.

## JF-20B: baseline and mutation predictions

The four representative shapes produce A, B1, album, and plain child with counts two, zero, one, zero. Seeded mapper counts remain at zero-recorded positions and are replaced at positive ones. Different container objects sharing a Guid merge while visited, retaining the first container object.

The early-break mutation fails later sibling excluded after threshold. The album mutation fails representative identities. The zero-restoration mutation fails zero leaves mapper value. In the delivered validation, each mode compiled successfully and failed at that expected semantic assertion, while the baseline passed twenty-two assertions and both original hashes remained unchanged.

Those observed results apply to the extracted algorithm and stand-ins. They do not mean the full API project or focused controller suite ran. A correct review preserves that distinction even when summarizing the result in one sentence.

## JF-20C: additional mutation

One useful proposed mutation groups by container object reference rather than Guid identity. A fixture with two distinct container objects sharing one ID, a limit that allows both candidates to be visited, and an expected single group detects it. Another changes the first-child choice to the last child for a singleton-independent fixture, provided the expected representative contract is stated correctly.

Keep the mutation signature-compatible and confined to generated code. Check extraction signature uniqueness and exact replacement count before compilation. Then require a successful build and a named failing semantic assertion. A compiler failure or changed source signature is an experiment maintenance issue, not proof that the behavior test caught a defect.

Preserve hashes of the selected originals before and after, and report that limited preservation scope rather than claiming a whole-repository audit.

## JF-21A: ungrouped prefix property

With a fixed candidate list, positive finite limit, and grouping disabled, each visited candidate creates one group containing that candidate. The expected sequence is the first minimum of list length and limit candidates. Test empty, shorter-than-limit, equal, and longer-than-limit lists. A folder with grouping enabled bypasses container grouping for that item and supplies a separate branch case.

The independent oracle can use an expected prefix of labels rather than reproducing the grouping conditionals. This property does not verify private query limits, library filters, or HTTP guard behavior because the extracted candidate provider is controlled.

A generator should use modest lists and preserve the stated valid domain. A negative direct method input is not an endpoint-valid request, and a half-maximum allocation adds cost without improving this small structural property.

## JF-21B: false monotonicity

For A1, A2, B1 with a nonalbum A container, limit one stops after A1 and selects A1. Limit two allows A2 to join A before B creates the second group, so the first representative becomes A. The larger response is therefore not necessarily the smaller response plus an appended item with an unchanged prefix.

A client relying on stable positional identity under limit changes needs a different documented contract or reconciliation strategy. For identity grouping, use two different A container objects sharing an ID and a limit above the first group count so both candidates are visited. Otherwise the test cannot distinguish merge behavior because early exit hides the second candidate.

A strong answer uses the counterexample to refine the property, not to label the existing algorithm wrong under an unstated new requirement.

## JF-21C: restoration properties

Applying the same positive-only count vector twice is locally idempotent, but a loop that overwrites zero is also idempotent. Add independent zero-preservation and positive-overwrite assertions with nonzero seeds to kill that mutation. Repeatability alone is too weak an oracle.

A same-length reordered mapper can attach counts to wrong identities, while extra outputs can exceed the count array and fewer outputs can leave counts unused. These are distinct contract violations. An identity-keyed redesign needs explicit duplicate, missing, and extra-output policies rather than assuming a dictionary removes every ambiguity.

The answer should distinguish current mapper correspondence from intentionally invalid test doubles and should not claim the real mapper exhibits the injected violation.

## JF-22A: operational policy

A defensible proposal chooses a modest maximum for a stated experiment and labels it provisional until workload evidence justifies deployment. Arithmetic safety, item count, and option cost remain separate concerns. Rejection communicates that the requested bound is unsupported; clamping silently changes the effective request unless exposed; partial output needs metadata and count semantics.

The exercise permits different chosen values, but requires exact acceptance and early-work behavior. If rejection can be decided solely from the limit, it can preserve the current early guard style. A user-tier policy needs identity information and therefore a different precedence discussion.

Do not award a proposal full compatibility credit when it calls requests between the new cap and old ceiling unchanged. Their acceptance intentionally changes and must be documented.

## JF-22B: compatibility matrix

Include omitted defaults, explicit defaults, one, the proposed maximum, one above it, zero, the old arithmetic maximum, and explicit played intent differing from preference. Compare current and legacy routes, and identify ordinary versus specialized retrieval branches for accepted cases. The current legacy action delegates, so a shared policy affects both route shapes.

Mocked action tests can cover huge numeric inputs and no-downstream-work assertions without allocating a library. Hosted tests add binding, content type, and serialized response evidence. Option profiles and representative correctness belong in bounded operational experiments, not in a single enormous stress request.

A strong matrix states old behavior, proposed behavior, service-call expectations, and evidence layer for every row. Empty cells should not conceal unknown or unexecuted behavior.

## JF-22C: errors and rollout

Proposed stable fields can identify parameter, supported range, and error code, but they are not current features. Keeping status 400 while replacing a string body with an object can still break clients. Versioning or migration guidance must address body shape and content type, not only status.

A rollout plan can request aggregate rejection counts by limit band and controlled work measurements, without inventing production usage percentages or collecting unnecessary media content. Deterministic invalid requests should be corrected rather than retried unchanged; transient failures need a bounded recovery policy.

Rollback can restore an acceptance range but may not undo client adaptations to a new error schema. Separate the cap and response-format changes when possible so their effects remain reviewable. A draft plan is not a deployed safeguard.

## JF-23A: policy inventory

The inventory should preserve default limit and grouping, nullable intent, subject identity, parent and type forwarding, DTO options, folder bypass, Guid-based grouping, early break, first-child selection, multi-child parent selection, singleton albums, and positive-only count restoration. The new policy intentionally rejects some limits previously within the arithmetic range.

Specify both routes and whether rejected input performs identity or service work. Do not accidentally change omitted played intent while adding the guard. Distinct synthetic identities and option values make mapping assertions meaningful.

A complete answer leads with the changed acceptance contract and then names preserved behavior. It does not bundle unrelated cache, pagination, and asynchronous rewrites into the same capstone merely because they concern performance.

## JF-23B: representative fixture

Use multi-child A, singleton nonalbum B, singleton album C, a folder, and an ungrouped item. Write the exact ordered representatives and seed mapper counts independently. Include A1, B1, A2 versus A1, A2, B1 at limit two, and A1, A2, B1 at limits one and two to expose collected-count and representative changes.

Zero-seeded DTOs cannot reveal zero overwrite. Unordered ID assertions cannot reveal positional count misassignment. Response length cannot reveal choosing a child instead of its parent. Each expected field should therefore have a specific discriminating purpose.

The lab can calibrate algorithm expectations, but the new guard requires action-level evidence on the implementation route. A strong fixture plan keeps those boundaries complementary rather than interchangeable.

## JF-23C: review missing guard evidence

Passing extracted-source cases supports the grouping, representative, and restoration statements executed by that lab. It does not execute the action's limit guard, so it cannot prove the new maximum or rejection precedence. Accept the algorithm evidence and require focused action tests for proposed maximum, one above, invalid zero, and no downstream work as specified.

A mutation that accepts one above the proposed maximum exposes the missing policy coverage; moving the guard after user lookup exposes missing early-work coverage. Hosted response-format claims require their own observation if the patch changes that contract.

The design-only route can be complete with a concrete test plan. Implementation completion cannot be claimed from a detailed plan plus unrelated green algorithm cases.

## JF-24A: claim ledger

For count correspondence, separate source indexing, captured representative input, captured mapper output order, final DTO pairing, and hosted serialized result. Correct the overclaim wrong count proves mapper defect to a narrower observation plus the stage capture needed to locate the mismatch. For cancellation, separate caller signal, server observation, started work, completed work, and response outcome.

Each row needs the appropriate experiment and limitation. A direct fixture cannot borrow host evidence, and a client cancellation cannot stand in for server cooperation. Synthetic labels and exact expected values make the ledger reviewable without exposing real library content.

A strong answer identifies the next observation that would falsify its current hypothesis, not merely another broad test to run.

## JF-24B: oracle and mutation

Count-track oracles need ordered identities, count vectors, nonzero mapper seeds, and faithful versus deliberately reordered controls. A length-preserving swap defeats a weak cardinality test. Cancellation-track oracles need gates and separate start/completion counts; a collaborator that reports cancellation but starts later work defeats an exception-only test.

Compiler failure means the semantic experiment did not run. Fixture timeout before the intended gate means setup did not establish the scenario. Assertion failure after a successful build can provide the intended mutation evidence. Hosted response observations remain a separate boundary.

The oracle must be specified before observing the result. Changing expectations until a test passes without explaining the causal difference destroys the independence the capstone is meant to assess.

## JF-24C: reviewer decisions

A complete design-only packet can be accepted as a source-grounded contract and experiment plan while explicitly remaining unimplemented at its proposed boundaries. An implementation packet missing required hosted evidence can be accepted for its demonstrated component behavior, but not represented as a fully verified public response contract.

Name the exact missing check: route binding and serialization, response-started cancellation behavior, or a real mapper integration fixture depending on the claim. Do not require a host run for a claim that is intentionally limited to extracted algorithm behavior, and do not award host credit to that limited run.

The final decision should state what is complete, what remains unverified, and why the next check matters. Honest scope is part of engineering correctness, not a disclaimer added after an inflated conclusion.

## Final review standard

The completed route should leave the learner able to preserve current behavior, propose deliberate changes, and assemble evidence without confusing layers. Strong answers use minimal counterexamples, independent oracles, and precise source anchors. They can explain a surprising behavior without silently repairing it in the description, and can mark a useful experiment as limited without dismissing what it actually proves.
