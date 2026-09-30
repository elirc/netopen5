# 17. Reason about consistency between retrieval and representation

The earlier chapters traced one latest-media request. This chapter asks what it means for that request to be consistent when selection and representation read different information at different times. Read [GetLatestMedia](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), [UserViewManager](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs), and [DtoService](../../../jellyfin/Emby.Server.Implementations/Dto/DtoService.cs). The source shows a sequential pipeline with shared user and option objects; it does not show a request-wide snapshot transaction around every collaborator.

The goal is to build a consistency contract that is precise enough to test without inventing guarantees. Current implementation observations appear as source facts. Snapshot isolation, cache policies, and versioned responses discussed below are proposed designs, not features added by this course.

## Name the observations that can differ

The controller loads the selected user, resolves played intent, constructs DTO options, asks for latest groups, chooses representatives, maps them, and restores selected child counts. The view manager's candidate retrieval and the DTO service's associated-data batches are separate calls. A library change between those calls can affect what each stage sees, depending on their implementations and data sources.

This does not automatically make the endpoint incorrect. Many read APIs intentionally provide a useful recent view rather than a transactionally frozen snapshot. The problem arises when a client or test assumes a stronger contract than the source establishes. State whether your proposed requirement concerns stable item identity, stable ordering, internally consistent counts, or a single database version. Those are different guarantees with different costs.

For example, a representative can be selected from a group assembled before a new child arrives. The controller's restored ChildCount is the number of children collected in that group, not necessarily the library's complete current child total. A later DTO batch may compute other fields from newer data. Calling the response a snapshot of the entire library would require evidence beyond this control flow.

## Preserve the distinction between selection and decoration

Selection decides which base items or containers occupy response positions. Decoration builds DTO fields for those chosen items using options and user context. The controller intentionally passes the same options object and loaded user to both stages, which keeps request intent aligned. Object identity alone, however, does not establish that every underlying data read occurs at the same instant.

A test can verify that the same user and options references are forwarded, that the mapper receives the intended representative identities in order, and that counts are restored at the corresponding indices. Those are strong local contracts. They do not prove immutable user preferences or a stable library while collaborators execute. If mutable shared objects become a concern, a proposed request-context snapshot should specify which values are captured and when.

Do not solve a consistency concern by cloning arbitrary objects without a contract. A shallow clone can still share arrays or nested state, and a deep clone can omit behavior or introduce expensive serialization. First list the actual request values and collaborator outputs that need stability. Then choose an explicit immutable request representation if the proposed design warrants it.

## Work a controlled interleaving

Use synthetic items A1 and A2 in container A, plus item B1 in container B. Suppose retrieval returns A1, A2, B1 and grouping produces A with two collected children and B with one. The controller selects container A and child B1 under the normal nonalbum rules. Its count array is two for A and zero for B1.

Now imagine metadata for A changes before DTO mapping, or another child A3 is added. The controller still restores two onto A's DTO because that is the selected-group count it recorded. It leaves B1's mapper-provided ChildCount unchanged because the restoration condition is positive only. These are source-derived local predictions. They do not assert how a real concurrent library update is synchronized internally.

A bounded collaborator fixture can simulate this interleaving by returning a fixed selection and then changing the mapper's supplied metadata. The test should verify the controller's contract rather than pretend the fixture models database concurrency. A separate integration experiment would need controlled update timing and the actual data stores to investigate cross-stage freshness.

## Distinguish count meanings explicitly

Three useful counts are collected children in the selected group, complete visible children in a container, and response representatives. The controller's positive override supplies the first for grouped containers. The DTO service may obtain other child-count information through its batch logic when requested. The response length is the third. None can be substituted for another merely because all are integers.

A client displaying a badge should know which interpretation applies. If a product requires a complete visible child total, it may need a different field or query rather than repurposing the collected count. A proposed change should preserve the old meaning or version the contract deliberately. Replacing a count with a more expensive total can affect both performance and compatibility.

The grouping loop's early break is central. Once the number of groups reaches the request limit, it stops scanning candidates, even if later candidates belong to an already selected container. Therefore, the collected count can depend on where the threshold is reached. This is not a complete-container census. A consistency test that expects every candidate with container A to be counted after the break would be testing a different algorithm.

## Define stable identity without assuming stable metadata

A useful minimum contract can preserve representative identity and response position while allowing fields such as playback progress or image metadata to reflect their normal read timing. Another contract can require a stable version for selected fields. Write the exact distinction before adding caching, retries, or asynchronous mapping.

For a local controller test, assign unique IDs to every child and container and seed mapper DTOs with corresponding IDs. Assert the ordered identity sequence and the count override independently. If the mapper reorders output, the current positional restoration can attach counts to the wrong DTO. The real selected mapper path preserves array index, but a replacement or test double must honor that contract or intentionally test a violation.

An identity-keyed restoration proposal could tolerate some reordering, but it introduces questions about duplicate IDs, representative collisions, and missing outputs. Do not label it automatically safer without defining those cases. Positional correspondence is simple when cardinality and order are guaranteed; changing the mechanism changes the interface contract that tests must protect.

## Separate retries from snapshots

Retrying a read after a transient failure can produce a different latest list because the library or user data changed. Read-only does not mean deterministic across time. A client that retries should not assume the second response is a byte-for-byte replay of the first attempted response. If stable pagination or continuation is required, the protocol needs a stated ordering and consistency model.

The latest endpoint's limit is an output-group bound, not a snapshot token. A proposed continuation design would need to define how grouping interacts with cursor positions, newly inserted items, and containers already represented. Simply using the last returned DTO ID as a cursor may skip or duplicate candidates because representatives can be parents rather than the queried child items.

This chapter does not add pagination. It uses the current grouping semantics to show why a future feature requires domain-specific design. A good proposal identifies the candidate ordering key, tie handling, representative mapping, and the state carried across requests. Generic cursor advice cannot replace that analysis.

## Build a consistency experiment matrix

Use one baseline with fixed collaborators, one simulated metadata change between retrieval and mapping, one candidate-order variation that reaches the group threshold earlier, and one deliberate mapper-reordering violation. For each, record selected candidate IDs, group membership, representative IDs, count array, mapper output IDs, and final DTO counts.

The baseline establishes the intended local pipeline. The metadata variation distinguishes selection stability from decoration freshness. The order variation demonstrates collected-count semantics. The mapper violation tests the positional contract's dependence rather than claiming the real mapper currently violates it. Label proposed behaviors and intentionally invalid collaborators clearly.

A full concurrent integration test would additionally need controlled library updates and a known observation point. Do not infer such evidence from sleeps inserted into mocks. A sleep can order the mock's own actions but does not reproduce the real library's transaction or synchronization boundaries.

## Independent exercises

Exercise JF-17A asks you to draw the A1, A2, B1 interleaving and list which response values come from selection and which come from mapping. Add A3 after selection and state what the controller's restored count can honestly mean. Your answer should distinguish source prediction from database concurrency evidence.

Exercise JF-17B asks you to specify a minimum consistency contract for representative identity, order, and counts. Compare positional and identity-keyed restoration, including duplicate IDs and missing mapper outputs. Do not change the current implementation in this exercise; produce a reviewable proposed contract and discriminating tests.

Exercise JF-17C asks you to critique a proposed retry-and-cursor feature. Explain why a read retry can return different media and why a representative ID is not automatically a candidate cursor. Identify the ordering, grouping, and freshness questions that must be resolved before implementation. Consult the separate final reviews after writing your own predictions.

## Review checkpoint

You have completed the chapter when you can describe useful local guarantees without calling the whole response a transactionally frozen library snapshot. A strong answer identifies the exact count meaning, protects representative correspondence, and gives a concrete next experiment for any stronger proposed consistency requirement.


[Separate hints and full review](review-04-consistency-labs-properties-and-capstones.md) | [Complete course route](README.md)
