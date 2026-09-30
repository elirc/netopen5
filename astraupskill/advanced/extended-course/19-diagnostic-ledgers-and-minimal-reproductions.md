# 19. Diagnostic ledgers and minimal reproductions

A latest-media bug report often begins with an imprecise observation: a count looks wrong, an item disappeared, or a request is slow. This chapter turns those observations into bounded investigations using the actual [controller](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), [grouping implementation](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs), and [DTO mapper](../../../jellyfin/Emby.Server.Implementations/Dto/DtoService.cs). It does not add production logging or change the server. The instrumentation discussed here is a proposed test or diagnostic design.

The objective is to produce a reproduction another engineer can challenge without access to a real user's library. Use synthetic identities and a compact stage ledger. Preserve enough detail to distinguish selection, grouping, representation, and serialization while avoiding unnecessary sensitive data or a transcript of every internal call.

## Start with an observable mismatch

Replace the statement wrong latest items with an exact expected and actual identity sequence. Replace wrong count with the field name, representative identity, expected count meaning, and observed value. Replace slow with the measured boundary, fixture size, options, and elapsed distribution. A useful report can be small because each field has a purpose.

For example, expected representative IDs A and B1 but observed A1 and B1 points toward container selection or group membership. Expected ChildCount two on A but observed seven points toward count restoration or correspondence. Expected one group but observed two may involve grouping disabled, a folder bypassing grouping, or different container IDs. Those hypotheses follow the source's actual branches.

Do not begin by copying an entire media database into a test. Identify the minimum synthetic shape that makes the branch decision different. Two children in one nonalbum container distinguish parent selection from single-child selection. A singleton music album distinguishes the explicit album exception. A folder with a container distinguishes the IsFolder bypass. Each is a focused reproduction with a clear oracle.

## Use a stage ledger with units

Record requested limit, effective played intent, selected subject identity label, parent label, grouping flag, included item types, and DTO option profile. Then record candidate count, group count, representative IDs, collected child counts, DTO IDs, and final count fields. Keep requested bounds separate from observed counts.

The ledger should also identify the query branch: channel parent, specialized grouped collection, or ordinary retrieval. The initial doubled query limit does not describe every branch. A report that compares two requests without their branch can attribute a count difference to the wrong mechanism. Branch identity is often more useful than a large unstructured debug dump.

Use synthetic labels such as SubjectA, ContainerA, and ChildA1 in the explanatory packet, with deterministic fixture GUIDs only where code requires them. A real user's names, file paths, access token, and playback history are not necessary to explain the algorithm. If a real incident motivates the fixture, transform it into the smallest equivalent shape before sharing.

## Diagnose a count mismatch in causal order

First ask whether the selected group actually contains the expected number of collected children. The early-break rule can stop before later siblings are processed. Next ask whether the controller chose the container or first child. A singleton nonalbum group yields the child and leaves the restoration count zero; a singleton album selects the album and records one.

Then inspect the mapper's output cardinality and order. The controller restores counts by index and only when the recorded value is positive. A mapper-provided value on an ungrouped representative remains untouched. Finally inspect the serialized field and client interpretation. A client may be showing a different count or treating a missing value differently from zero.

This order prevents a proposed fix from overwriting every DTO ChildCount with zero just to make one screenshot match. Such a change would alter the deliberate positive-only preservation behavior. A regression test should seed nonzero mapper counts on rows that should remain unchanged so this mistake becomes visible.

## Diagnose a missing item without assuming visibility failure

A candidate may be absent because retrieval filters excluded it, grouping represented its container instead, the group threshold stopped scanning before it, or a later layer behaved differently. Visibility is one possible boundary, not the only explanation. The controller requests skipVisibilityCheck in DTO mapping because it relies on selection's visibility handling; that trust assumption should be examined at the correct stage.

A minimal fixture can distinguish hidden candidate from grouped child by recording the candidate list returned to grouping and the representative list passed to mapping. If the child is present in a group's members but the parent is selected, it is not missing in the same sense as an item never returned by retrieval. The diagnostic vocabulary should reflect that difference.

For a real library investigation, avoid weakening visibility checks to make an item appear. Instead, reproduce the relevant user, parent, and filter context with synthetic data and trace the earliest exclusion. A security-sensitive symptom requires precise evidence, not a broad claim that a missing item proves access-control failure.

## Distinguish repeated calls from duplicated effects

A direct test can count view-manager and mapper calls, but a call count alone does not measure all underlying database or metadata operations. DtoService performs several option-dependent batches and type-dependent enrichments. One top-level mapper call can still initiate multiple lower calls. Conversely, a mock mapper can return immediately and reveal nothing about production mapping cost.

When investigating repeated work, identify the level being counted. Top-level invocation count, batch count, item-level enrichment count, and serialized output count answer different questions. Do not label a reduction in one as an end-to-end optimization without measuring the relevant lower stages and preserving correctness assertions.

A proposed diagnostic hook should be cheap and bounded. Capturing every full DTO can dominate the workload and expose user-specific fields. Prefer counts, branch labels, selected synthetic IDs in tests, and stage durations. If deeper payload capture is necessary for a controlled experiment, limit it to an owned fixture and state that it is not a production logging recommendation.

## Build a hypothesis table before changing code

For each hypothesis, write a discriminating observation and a falsifying result. Hypothesis: the controller overwrites ungrouped counts. Observation: seed mapper ChildCount with ninety-nine on an ungrouped row. Falsifying result: final count remains ninety-nine. Hypothesis: the grouping loop scans every candidate. Observation: place a later sibling after the threshold-producing group. Falsifying result: that sibling is absent from the collected group.

This method keeps investigation from becoming a sequence of edits until output looks plausible. A failed hypothesis is useful when the experiment cleanly distinguishes it. Record the source branch that explains the result and move to the next boundary. Do not retain a speculative fix merely because it happened to change the symptom.

Use one variable at a time when possible. If you change grouping, item types, subject user, and image options together, an improved response cannot be attributed confidently. A controlled matrix is more informative than a large collection of unrelated request examples.

## Make failure receipts reproducible

A receipt should name the source version through local hashes or a known revision when available, the exact fixture, command, expected result, actual result, and execution boundary. For a disposable extracted-source lab, include which methods were copied and which collaborators were stubs. For a direct action test, state that model binding and middleware were bypassed.

Build failure, test assertion failure, and host startup failure must remain separate outcomes. A failing command is not automatically a reproduced endpoint defect. Preserve a short diagnostic output showing the stage, rather than only an exit code. The source-based lab in chapter 20 uses named assertions and explicit build completion to support this distinction.

Do not repeatedly rerun a broad suite when the failure is already localized to an unbuilt dependency or missing asset file. Continue useful source inspection or a bounded experiment, then report the unavailable boundary. The goal is evidence that explains the behavior, not a ritual list of commands regardless of their ability to execute.

## Review a proposed instrumentation change

Suppose a patch adds logging of every selected user's identifier, every media path, and complete DTO JSON around each stage. Ask what question each field answers, whether synthetic fixtures could answer it instead, and whether the added serialization changes the performance being measured. More data can make a report less interpretable and more intrusive.

A better proposed hook might expose a test-only stage observer with candidate count, group count, representative labels, and elapsed durations. Even that hook should have a clear lifecycle and avoid becoming a new application contract accidentally. The course does not require such a hook; a collaborator fixture or debugger can often collect the needed evidence without modifying production behavior.

The strongest diagnostic artifact is the smallest one that rules out competing explanations. It is specific enough for another engineer to reproduce, modest enough to review, and honest about which layer it did not exercise. That standard applies equally to correctness and performance investigations.

## Independent exercises

Exercise JF-19A asks you to turn a wrong-count report into a minimal three-group fixture. Include a multi-child container, a singleton nonalbum container, and a singleton album. Seed mapper counts so positive-only restoration is observable and write exact expected IDs and counts.

Exercise JF-19B asks you to build a hypothesis table for a missing item and a slow request. Give two competing explanations for each and one observation that distinguishes them. State which counts are top-level calls and which are lower-stage work.

Exercise JF-19C asks you to review the excessive logging proposal and produce a smaller evidence receipt. Include source identity, fixture shape, build/semantic outcome, and explicit unexecuted boundaries. Use the separate review guide after completing your own diagnostic plan.

## Review checkpoint

A complete investigation can explain why its fixture is sufficient, which hypothesis it ruled out, and what the next observation would resolve. It does not expose unnecessary user data, confuse grouped representation with absence, or treat any failing process as proof of the original reported defect.


[Separate hints and full review](review-04-consistency-labs-properties-and-capstones.md) | [Complete course route](README.md)
