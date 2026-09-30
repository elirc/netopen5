# Review: binding, query branches, evidence and errors

Attempt chapters 11–16 before reading these worked reviews. The exercises extend the source map outward: raw query syntax enters through a binder, parent context selects retrieval branches, mapping depends on prior visibility work, build configuration defines executable evidence and middleware can translate exceptions. A useful review follows those boundaries without pretending that one direct test executes all of them.

## JF-11A: input representation chooses preprocessing

An omitted collection parameter produces an empty typed array in the binder. A single nonnull value is split on commas with empty pieces removed. Multiple supplied values are passed as a list to conversion without an additional explicit split in that branch. Each conversion input is trimmed before the type converter is called. Keep these stages separate in the syntax matrix.

For ordinary repeated enum values such as two separate recognized names, the existing binder tests provide an example. For a repeated value that itself contains a comma, the binder's preprocessing is clear but the converter's interpretation must still be investigated for the actual enum type. Some converters can interpret combinations; others can reject text. Do not replace that investigation with a general statement that commas always flatten into more array elements.

The helper catches FormatException and drops the corresponding unsuccessful conversion entry. It does not contain a catch for every exception. A test demonstrating one invalid enum string is omitted cannot establish that every malformed input of every supported element type is harmless. The exact converter and exception matter.

The single-value double-comma case removes empty entries during splitting. Whitespace-only pieces are not necessarily identical to empty pieces before trimming and conversion. If that distinction matters to a proposed contract, create a focused binder case with an explicit expected result. The point is to follow each transformation in its actual order.

## JF-11B: empty arrays have consumer-specific meaning

An empty includeItemTypes array invites downstream inference from selected parents and collection categories. It does not simply mean no items or all item types with no other rules. An empty fields array is assigned to DtoOptions.Fields. An empty image-type array leaves the option object's existing ImageTypes unchanged in the extension. Those are three different meanings after the same general binding mechanism.

An invalid-only collection input that becomes an empty array can therefore converge with omission at the downstream boundary. Whether that is an acceptable API policy requires a deliberate decision. A proposal to reject invalid tokens would change behavior for clients that currently rely on valid-subset parsing, so it should include mixed-input cases and migration considerations.

A reviewable proposal states whether one bad token rejects the whole parameter or whether valid values survive. It also specifies error location and machine-readable information if clients need to identify the bad parameter. The course does not implement such a change. Its learning outcome is a before-and-after contract that can be evaluated against current behavior.

## JF-11C: three layers answer three questions

A binder-unit test can establish how a chosen value-provider representation becomes a typed array. A controller test can establish how that array is forwarded or used to construct options. A hosted test can establish that an actual URL reaches the intended binder and action under the application's configuration. None is automatically redundant with the others.

Use an empty controlled view result in the hosted fixture so parsing evidence is not entangled with a large library. Capture the typed argument or downstream query when possible. A final empty response alone cannot reveal whether the binder discarded a value, the service inferred another type or the library simply contained no matching items.

The test report should preserve raw input and the observed typed representation using synthetic values. Avoid logging an entire production query or principal merely to diagnose a small binding behavior. Focused artifacts make failures easier to understand and share.

## JF-12A: fallback is a real branch

A nonempty parent ID is looked up. Channel takes its specialized branch and returns candidates from the channel manager. Folder is added to the selected parents. If no parent has been selected, the service uses the user's root children, keeps folders and applies latest-item exclusions. If that produces no parents, it returns an empty candidate collection.

Thus a missing or unrecognized explicit parent can reach fallback in this method. The controller does not independently return not found for parentId the way it does for a missing loaded user. A learner who inferred uniform not-found handling from another action would need to revise the source map here.

The parent decision tree should show the early channel return before ordinary inference and query construction. Applying later music or grouped-collection rules to a path that has already returned is a control-flow error. This is why reading only matching variable assignments without their surrounding branches can produce an inaccurate explanation.

## JF-12B: final query properties depend on the branch

Explicit included item types bypass empty-type inference. Empty types can become Movie or Episode for homogeneous relevant UserViews, or remain empty while media types are derived from collection folders. The default excluded-type set is used only when both included types and derived media types are empty. Write those conditions explicitly instead of describing one universal default filter.

The ordinary query contains descending DateCreated, SortName and ProductionYear ordering. This gives more structure than newest timestamp alone, but it does not establish a unique order for complete ties across all those fields. If stable paging across ties becomes a requirement, investigate the underlying query's additional ordering or propose an explicit tie breaker with compatibility evidence.

The query is initially assigned twice limit. Grouped television, music and movie branches can replace that value with the original limit before using GetLatestItemList. The arithmetic expression was still evaluated in construction, so the upper guard remains relevant. The channel branch instead forwards request.Limit through its own earlier query.

LatestItemsQuery also has StartIndex, but this controller does not expose or set it. A shared model can support other callers without expanding every endpoint's public surface. Do not invent a latest-media paging parameter simply because a property exists on the downstream request type.

## JF-12C: changing fallback changes the contract

A proposal to reject an explicitly missing parent needs a way to distinguish explicit invalid context from omitted context while preserving channel handling. It should specify the error type or result, its translation at the API boundary and tests for recognized Folder, Channel, missing item and another item type. It should also state what happens when fallback roots are legitimately empty.

Compatibility review should ask whether clients use stale parent IDs and currently receive root results. Replacing that behavior with an error may be desirable, but it is observable. The proposal should not be described as a harmless internal cleanup. A before-and-after table gives reviewers enough information to decide whether the change fits product expectations.

The exercise is complete with a source-grounded design and tests to implement later. It does not require altering the application during a documentation expansion or inventing deployment telemetry that has not been collected.

## JF-13A: assign each trust claim to evidence

The actor-to-subject row points to RequestHelpers and the principal's roles and identifier. Parent selection points to UserViewManager and the loaded subject's root children and exclusion preferences. Channel retrieval points to a user-scoped InternalItemsQuery. Representative selection points to the controller's tuple logic. DTO user-data mapping points to the same User object supplied to DtoService.

For each row, distinguish observed context flow from a broader access guarantee. The source shows a user is passed; verifying every underlying query's enforcement requires following or exercising that query. A mock returning a prefiltered collection proves the controller handles that collection, not that the real filtering is correct.

Potential invalidators include a cache that ignores subject identity, a service substitution that bypasses visibility-aware retrieval and a mapper change that filters or reorders without preserving saved-count association. These are review scenarios. Their purpose is to expose assumptions before a refactor, not to accuse the current implementation of unobserved defects.

## JF-13B: synthetic access fixtures should include representatives

Two users and two parent scopes can establish a clear expected access matrix. Use invented item IDs and simple ownership or visibility rules in a disposable integration fixture. Include self access, administrator subject access and denied cross-user access at the appropriate layers. Keep actor and subject distinct in the administrator case.

An album with one child is useful because the controller can map the album representative even though the candidate began as a child. Verify the identity of the final mapped object as well as candidate identities. This closes a conceptual gap that a candidate-only assertion might leave.

A real query integration fixture is needed to establish actual candidate access. A direct controller fixture can still verify that the resolved subject reaches both query and mapper. Treat these as complementary observations. A well-designed evidence plan can use inexpensive direct cases broadly and reserve hosted or database cases for the boundaries they uniquely establish.

## JF-13C: cache identity must follow semantics

A selected-group cache may depend on subject user, parent, included types, resolved played filter, grouping and library state. A fully mapped DTO cache additionally depends on fields, images, user-data options and potentially other mapping context. Storing one user's mapped DTOs under a key that ignores subject identity risks mixing context even when selected item IDs overlap.

Preferences complicate omitted options. A request that omits isPlayed can resolve differently after HidePlayedInLatest changes. A key based only on the raw absence marker may need invalidation or resolution-aware identity. The proposal should state whether it caches before or after preference resolution and how updates invalidate entries.

Do not claim the listed dimensions form an exhaustive production key without inspecting the entire retrieval and mapping path. A review checklist can identify known dependencies and unresolved ones. That is a useful bounded output, and it is safer than presenting an incomplete key as a finished implementation.

## JF-14A: record inherited build context

The test project targets net10.0 through test-directory properties that import the parent properties. Root settings include nullable analysis, warnings-as-errors behavior and analyzers. Package versions are centrally managed. The API test project references the actual API and server implementation projects, so its build involves more than one controller file.

The global SDK policy requests 10.0.0 with latestMinor roll-forward. The actual selected SDK is an observation from the execution environment. Do not conflate requested policy, target framework and installed SDK version; they are related but distinct. A run manifest should record all relevant values with their evidence source.

Only include environment information needed to reproduce the result. Full environment-variable dumps can expose unrelated personal or secret configuration and usually add little value. The project path, SDK selection, command and dependency state are sufficient for many focused run reports.

## JF-14B: classify failures before fixing them

Missing restored assets prevents the build from resolving its dependencies. A warning promoted to an error stops compilation under the repository's policy. A half-maximum assertion failure occurs after tests execute and directly challenges the behavior expectation or fixture. These require different next steps and should not share a vague failed tests label.

A successful command with zero discovered tests does not establish that the intended class ran. Inspect discovery output and filter syntax before reporting success. Similarly, skipped cases retain their skipped status even if the overall process exits successfully. The evidence report should preserve those distinctions rather than compressing everything into green.

Do not weaken production build policy merely to make a learning report pass. If a bounded isolated lab is used instead, state which actual source it compiles and which project settings it omits. The narrower evidence can be useful when honestly named.

## JF-14C: a pending template is not a completed run

The report template should separate intended command from observed command output. Before execution, counts and exit status remain pending. After execution, fill them from actual results and link a saved artifact where appropriate. Documentation link checks belong in another section because they validate navigation, not runtime behavior.

A source inspection can still support a complete chapter while a proposed integration experiment remains unrun. The distinction is between instructional completion and implementation evidence. A course can deliver a full capstone brief without pretending that the learner's future solution already exists.

## JF-15A: keep requested bounds and observed counts separate

Requested limit is the client's desired maximum under the endpoint contract. Assigned query limit is what a selected service branch asks its retrieval collaborator to return. Candidates returned is an observation. Groups produced is the grouping loop's output count. DTO count and response bytes describe later stages. They can differ substantially in a grouped or option-rich request.

Many candidates sharing a container can reduce group count while still consuming retrieval and grouping work. The loop's early break can also leave later candidates unprocessed once enough groups exist. Record both retrieved and processed candidates if the experiment needs that distinction. A single item count cannot explain the whole path.

## JF-15B: timing without correctness is incomplete

Use fixed synthetic data for each grouping shape and hold options constant when comparing grouping. Then vary option profiles on the same selected population. Assert representative IDs and counts in every run. A candidate optimization that skips correct mapping work may look faster while returning the wrong contract.

Record warm-up state, sample count and relevant variability. Avoid precise performance claims from one noisy run. Large arithmetic boundaries remain in mocks; real retrieval experiments use bounded fixtures selected to expose cost behavior. Any extrapolation should state its model and uncertainty.

## JF-15C: selections and DTOs are different cache products

Caching selected domain groups can avoid some retrieval work while still mapping under current user and option context. Caching full DTOs can avoid more work but preserves more context-sensitive data. The invalidation and key requirements differ. A proposal should say which artifact it stores before discussing hit rates or performance benefits.

Library updates, played-state updates, preference changes and image or metadata changes can affect different layers. A complete review plan identifies those change sources and the intended freshness contract. The exercise does not require a universal cache implementation; it requires an honest inventory of what a cache would have to preserve.

## JF-16A: identify the origin before naming the response

Invalid representable limit returns a bad-request result from the action. Missing loaded user returns not found. Forbidden explicit subject can throw from RequestHelpers. Malformed integer text belongs to binding. Invalid collection tokens follow the custom binder's conversion behavior. View or mapper exceptions propagate from direct action execution unless handled by a broader pipeline.

The inspected ExceptionMiddleware maps a security exception to forbidden when it catches it before the response starts. It writes plain text and varies message detail by environment. That is source-backed middleware behavior, not proof that every possible request reaches that middleware in a particular hosting setup. A hosted test establishes the complete route through it.

## JF-16B: fault placement determines what remains observable

A null user result prevents view retrieval. A view exception prevents representative selection and mapping. A DTO exception occurs after groups have been selected. Separate fixtures isolate those paths. Configuring every collaborator to fail at once only observes the earliest reached failure and says little about later stages.

A middleware fixture whose next delegate throws before response start can assert status and body under a chosen environment. A direct action fixture instead observes the thrown exception. Both can be correct for the same underlying condition because they execute different boundaries. Keep their reports separate and connect them with a clear pipeline diagram.

If the response has already started, the middleware rethrows rather than performing its normal replacement response. Do not promise a clean error envelope for late failures without testing the actual response lifecycle. This limitation is especially relevant when extending patterns to streaming endpoints.

## JF-16C: retry policy should follow error meaning

Correct invalid input before retrying. Resolve missing or forbidden subject context rather than repeatedly sending the same request. A transient server failure may justify a bounded retry for a read, but the client should avoid uncontrolled loops and should preserve enough diagnostic context to distinguish recurring deterministic errors.

Development exception text is not a stable production machine code. The middleware uses a generic message outside development, and returned action results can follow another formatting path. If a client needs structured error categories, propose an explicit contract and compatibility tests rather than parsing incidental prose.

Retain the syntax matrix, parent tree, trust ledger, run manifest, work ledger and error-origin table. Together they form a practical investigation kit: each artifact answers a different question and makes the limits of its evidence visible to the next engineer.
