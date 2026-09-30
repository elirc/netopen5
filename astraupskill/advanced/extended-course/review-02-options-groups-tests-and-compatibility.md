# Review: options, groups, tests and compatibility

Use this guide after chapters 06–10. These exercises move beyond the integer guard into the values that a successful request carries through the system. The recurring challenge is preserving associations: options with their intended defaults, a group with its representative, a DTO with its saved count, and a legacy parameter with its primary-action counterpart.

## JF-06A: trace assignments in order

Begin with the DtoOptions constructor, then apply the action's Fields initializer, then the extension and finally PreferEpisodeParentPoster. Constructor defaults are starting values, not necessarily final endpoint values. In particular, the request's fields array replaces the constructor's field list. An empty request array therefore remains an empty Fields collection at this controller boundary rather than silently restoring all default fields.

EnableImages becomes the explicit request value or true when omitted. EnableUserData retains its constructor value when omitted and takes the supplied value when present. ImageTypeLimit retains the constructor's int.MaxValue when absent and takes the provided integer when supplied. A nonempty image-type list replaces existing types; an empty list leaves them unchanged. The poster preference is set true after the extension.

With images disabled and a nonempty type list, the list is still assigned, but GetImageLimit returns zero because EnableImages is false. This illustrates why inspecting a single property is insufficient to predict behavior that depends on several options. Conversely, enabled images with a type absent from ImageTypes also yield zero for that type. The meaning is a conjunction, not a field in isolation.

Do not infer that imageTypeLimit has been range-validated by this extension. It assigns a supplied value. If the exercise investigates negative or unusual values, trace validation elsewhere and distinguish assignment behavior from accepted public requests. The latest-media integer guard protects limit, not every numeric option in the signature.

## JF-06B: the same option object crosses two boundaries

The action creates one DtoOptions instance and passes it to the view manager and later the DTO service. A captured-argument fixture can compare reference identity and inspect its final properties. Use nondefault values, such as disabled user data and a small image limit, so an omitted extension call becomes observable.

The existing focused tests use broad DtoOptions matchers. They establish other forwarding behavior but do not certify every property. A new option-focused case should name that additional contract explicitly. Avoid a fixture whose expected options are constructed by invoking the same extension under test, because a bug in that extension could affect both actual and expected objects identically.

If a collaborator were to mutate the shared option object, later behavior could change. The current controller does not clone options between calls. That is an ownership assumption worth noting, but a hypothetical mutation should not be described as a production bug without evidence that a real collaborator performs it. A controlled mock mutation is an assumption probe and should be labeled as such.

## JF-06C: measure work at the right layer

The inspected DTO service performs option-dependent batch retrieval, including user-data work and some folder-count work. A test counting service invocations can establish that a branch is taken or batching occurs. It does not measure database latency, disk behavior or serialization cost. A benchmark using the real dependency chain answers a different question and needs representative data and environment records.

Keep selected item count fixed while changing one option category. Then vary item types separately. A folder can trigger work that an ordinary item does not, so comparing unrelated fixtures confounds option cost with item-shape cost. Record both the input population and requested fields alongside the observation.

A practical budget proposal should account for the largest relevant response and work shapes, not just the default empty result used in arithmetic tests. That does not require loading a real user's library for a lesson. Synthetic controlled fixtures can expose branch behavior while preserving privacy and reproducibility.

## JF-07A: the group threshold stops scanning

With candidates A1, B1, A2, C1 and a group limit of three, A1 creates group A, B1 creates group B, A2 appends to A and C1 creates a third uncontained group. The returned order is A, B, C1, and A's collected child list contains A1 and A2. The dictionary maps container IDs to list indexes; the list preserves first appearance.

With a group limit of two, the loop stops immediately after B1 creates the second group. A2 and C1 are not processed by this grouping loop. A's collected list contains only A1. This is why the saved group child count cannot automatically be described as the total number of children in the library or even every matching child among a larger unprocessed candidate set.

If grouping is disabled, candidates do not use their index containers in this loop. Each candidate becomes an uncontained one-child tuple until the group-count threshold is reached. Folders also avoid an index container under the inspected condition. These are source-level grouping rules; actual candidate ordering and retrieval remain responsibilities of the earlier query path.

The exercise should state that it supplies the candidate sequence directly as a model of the loop. Unless it invokes the actual service with its required dependencies, it is not a full retrieval test. An independently written trace can still clarify the algorithm without pretending to establish database behavior.

## JF-07B: representative selection has an album exception

A null container with one child selects that child and saves count zero. A nonalbum container with one child also selects the child and saves zero. A nonalbum container with two children selects the container and saves two. A MusicAlbum container with one child selects the album and saves one. Distinct IDs make these four outcomes observable in mapper inputs.

The action reads the first child before checking the container condition. An empty child list therefore fails at that access in the current direct path. The real view-manager loop creates groups with an initial child, so the malformed tuple violates the collaborator shape established by that construction. A robustness proposal can add validation, but it should begin by identifying the violated assumption rather than claiming ordinary service output is currently empty.

For a hypothetical null-container tuple with several children, the condition requiring a nonnull container fails and the first child remains selected. Such a fixture is useful only if its purpose is explicit. Ordinary fixtures should model valid service output; adversarial fixtures should be labeled as contract probes so their findings are interpreted correctly.

## JF-07C: complete counts need a defined population

A total library child count might include children outside the latest candidate window, children excluded by played filters or children invisible to the subject. A useful proposal says exactly which of those populations it intends to count. Reusing the current collected-child count under a broader label would mislead clients even if the integer itself is accurate for its original population.

One design could expose both collectedLatestCount and visibleTotalCount with explicit semantics. Another could retrieve a total only when requested because it has additional cost. These are proposals, not fields added by this course. Their review should consider visibility, query consistency and whether the two values were observed at the same logical point.

Use the early-break fixture as a counterexample: A has a later candidate A2 that is never processed when the second group triggers termination. The collected count is one even though another relevant child exists in the supplied candidate sequence. That small example makes the distinction clearer than a large realistic library snapshot.

## JF-08A: counts follow positions under the current contract

For representatives A, B and C with saved counts two, zero and one, mapping must preserve the intended positional association. The action sets A's DTO ChildCount to two, leaves B's mapper-provided ChildCount unchanged and sets C's to one. Initialize B's DTO count to a distinctive value such as seven so the no-overwrite behavior is visible.

If every mock DTO starts with zero, a mistaken implementation that writes zero to ungrouped slots can pass unnoticed. Similarly, using identical IDs or counts for every row hides ordering and association errors. Good fixtures use just enough distinct data to reject the plausible defect without becoming difficult to read.

The action iterates the DTO count when applying saved values. It relies on the DTO service returning compatible cardinality and order. The inspected skip-visibility path maps the supplied selected list by index into an equally sized array, supporting that assumption in the current implementation. A mock that returns extra DTOs can violate the assumption and cause indexing failure, but that should be reported as a collaborator-contract probe.

## JF-08B: skipping one check transfers responsibility

The controller comment attributes prior visibility handling to GetLatestItems. The query includes the resolved user, and the downstream service uses that context in library queries and parent selection. Those observations explain the intended trust relationship. They do not by themselves constitute an exhaustive proof for every category, item type and representative container.

A visibility investigation should use controlled libraries with known accessible and inaccessible items and exercise relevant grouped and ungrouped paths. Check the representative as well as its children: selecting a container changes which object is mapped. Record whether a test exercises the actual view manager, actual DTO service and hosted authorization or only one of those boundaries.

Removing skipVisibilityCheck without considering positional count restoration could introduce filtering that shifts associations. Keeping it while bypassing the earlier visibility-aware retrieval could remove a protection. A refactor must review both sides of the relationship together rather than treating the boolean as an isolated performance switch.

## JF-08C: an identity join changes the assumptions

An identity-indexed count map can tolerate mapper reordering if each selected identity has one unambiguous saved count and every DTO reports the corresponding identity. It needs a policy for duplicate selected IDs: first count, last count, combined count or rejection. It also needs behavior for missing and unexpected DTO IDs. Those decisions do not disappear simply because a dictionary is used.

The current positional design is straightforward when the mapper guarantees one result per input in the same order. An identity design can improve robustness against a different mapper contract but may add ambiguity or storage. A decision note should compare actual risks instead of assuming dictionaries are universally safer than parallel arrays.

Retain both a reorder example and a duplicate-ID example. The former shows where identity association can help; the latter shows why it needs additional policy. Good design exercises teach where assumptions move when representation changes.

## JF-09A: coverage is a relation between tests and defects

The five invalid rows cover lower and upper rejection examples, including integer extremes. The three valid rows protect a small accepted value, the default-sized explicit value and the final accepted upper edge. The omitted-limit case protects default twenty and grouping true. The legacy invalid case protects shared guard behavior through delegation. Together they form ten cases under theory expansion.

The valid cases' empty view lists mean they do not exercise representative choice or positive child-count restoration. Broad DTO option matching leaves detailed option construction unverified by those cases. These are specific gaps that motivate focused additions. They do not imply the existing suite should be replaced by a single broad integration test.

Map each proposed new case to a distinct mutation. A nullable-filter case rejects null-to-false collapse. A nonempty album case rejects removal of the MusicAlbum exception. An option case rejects lost image or user-data forwarding. A compatibility case rejects a dropped legacy parameter. This approach grows coverage by meaning rather than by raw case count.

## JF-09B: a small nonempty fixture can be powerful

Use one nonalbum container with two children and one uncontained child. The expected mapper inputs are the container followed by the uncontained child. Return two DTOs with those identities and distinct initial ChildCount values. The first should receive two; the second should retain its mapper value because its saved count is zero.

Capture the resolved User and DtoOptions alongside the selected item list. Assert status and payload association independently. The fixture can expose wrong representative selection, wrong order, indiscriminate count overwrites and context substitution while remaining small enough to reason through by hand.

Do not make the expected-value callback reproduce the controller's selection loop. A callback can record what the controller supplied and project obvious IDs, but the expected representative list should be written independently. Oracle independence is about avoiding shared mistakes, not about forbidding every reusable test helper.

## JF-09C: execution reports need outcomes and limits

A valid run report names the test project and filter, the selected SDK, the command exit status and actual test counts. If restore or compilation fails before discovery, say so rather than reporting zero passing tests as a behavior result. If a test is skipped, preserve that category. A historical run from the earlier course is not a new execution of this expansion.

The local global.json requests the repository's SDK policy, and the test project references the real API and server implementation projects. Running from the nested repository helps make SDK and build context explicit. Do not install packages or change application build settings merely to make a documentation report appear complete; an accurately scoped inspection can remain useful when execution is not performed.

A later author verification record may include bounded actual-source labs or focused suite runs. Those should be reported separately from the independent capstone exercises, which remain learner work until implemented and executed. The instructional course can be complete without pretending that every proposed feature has shipped.

## JF-10A: compatibility includes every forwarded option

The legacy method forwards all eleven parameters to the primary action: user, parent, fields, included types, played filter, image enablement, image limit, image types, user-data enablement, item limit and grouping. Both signatures retain twenty and true defaults for the last two values. The user binding source differs: required route value on the legacy method and optional query value on the primary method.

Use distinct nondefault values for adjacent parameters of related types. Explicit false for images, true for user data and a small image limit make positional mistakes easier to detect. Arrays should contain recognizable members rather than all being empty when the purpose is to verify array forwarding. The captured options and query reveal different parts of the transfer.

The existing legacy guard case verifies one important rejection path, but an invalid limit exits before most forwarded options are used. It cannot prove their successful-path preservation. A paired successful fixture is needed for that broader equivalence claim.

## JF-10B: compare equivalent inputs at a defined boundary

Create fresh controller fixtures for primary and legacy calls so mock histories and mutable captured objects cannot leak across the comparison. Supply the same principal, subject and nondefault options. Compare the resulting query values, option properties, selected item associations and final status. This establishes equivalence after argument binding.

Use separate hosted tests to compare route binding. A malformed route Guid and a malformed optional query value can fail through different binding surfaces. Shared delegation does not make those surfaces identical. A compatibility report should preserve the distinction rather than promising byte-for-byte equivalence for every invalid URL.

Keep obsolete-warning suppression local to the legacy invocation. The test intentionally exercises supported compatibility code, so the narrow suppression documents that purpose. It does not justify disabling warnings across the project or treating obsolete as removed.

## JF-10C: a migration note should avoid invented promises

A useful note shows the old route with a synthetic subject ID and the primary route with that ID supplied as a query parameter. It carries through selected filters and explains that omitting the primary user parameter asks the helper to use the authenticated context. An administrator explicitly choosing another subject remains governed by the same helper rule.

Do not state a removal date, release timeline or support guarantee not found in the source or an authoritative policy supplied to the task. The source establishes obsolete and hidden-from-exploration metadata alongside a still-implemented delegating action. That is enough to explain the mechanical migration without inventing product commitments.

Finish with a compatibility evidence table: direct delegation, captured query, captured options, representative output, hosted route binding and serialized response. Mark each row inspected, executed or proposed. The table gives the next learner a concrete route from local reasoning to a broader integration claim.
