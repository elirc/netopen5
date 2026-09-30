# Review: boundaries, identity and preferences

Attempt chapters 01–05 first. Keep your original predictions and annotate corrections rather than replacing them silently. The most useful outcome is an explanation of why a prediction changed: an overlooked branch, a confused evidence level or a mistaken meaning of an omitted value. Those explanations help you transfer the lesson to a different endpoint.

## JF-01A: the map should preserve authority

The guard owns the accepted integer range at the action boundary. RequestHelpers owns the resolution of actor and requested subject under its current helper policy. IUserManager supplies the loaded subject User. That user's preference supplies an omitted played-filter default. The view manager owns candidate retrieval and group assembly. The controller owns representative selection and saved child-count application. The DTO service owns mapping selected items into response models.

These ownership statements are more useful than a diagram whose arrows all say data. They let you ask where a proposed change belongs. A practical maximum belongs in an input-policy discussion, while a wrong album representative belongs in group-resolution behavior. A user preference being applied to the wrong subject is different from a database query ignoring a correctly forwarded filter.

The action's empty paths must remain distinct. Invalid limit exits before identity resolution and services. Missing user exits after an allowed identity has been resolved and looked up. An empty view result proceeds to DTO mapping with an empty selected array. A diagram that marks every empty outcome as short circuit would incorrectly predict collaborator calls for the last path.

The view-manager-to-mapper relationship is also important. Mapping skips its own visibility filter because the controller relies on the earlier retrieval path. That does not mean visibility has ceased to matter. It means the responsibility is placed earlier, and a refactor that substitutes candidates must preserve or reestablish that responsibility.

## JF-01B: an empty successful response still does work

With an existing user and an empty tuple list, resolvedItems and childCounts both have length zero. The representative loop performs no iterations. The DTO service is called with the empty selected list, the constructed options, the resolved user and skipVisibilityCheck true. If it returns an empty DTO collection, the controller returns a typed successful result containing that collection.

If the user lookup instead returns null, the action returns not found before constructing the view query and before invoking DTO mapping. The prepared empty-view and mapper setups should not be consumed. Negative-call assertions can make that difference visible. A successful empty library and an unavailable user are different outcomes even though neither produces media items.

The successful result's runtime wrapper derives from OkObjectResult. The existing tests use assignability and verify status two hundred. An exact OkObjectResult assertion would reject the typed subclass used by the local base controller. This is a small example of why test conventions should follow the repository rather than a remembered pattern from another project.

## JF-01C: evidence labels should be specific

A source claim can state that the action sets PreferEpisodeParentPoster true. An existing focused-test claim can state that accepted boundary values are forwarded to the mocked view manager. A proposed test can state that all nullable preference combinations should be covered. A proposed HTTP test can state that malformed integer text should be examined through model binding. These labels describe different work products.

Do not write verified next to a proposed fixture merely because its expected result follows from source inspection. Inspection is valuable evidence and can be labeled honestly. Execution adds a different observation: the compiled code in a defined environment behaved as predicted. A future refactor can invalidate either, so source paths and run records are useful alongside the claims.

The ledger should include limitations that name a missing boundary. Does not exercise real visibility is meaningful. More testing needed is too vague to guide anyone. Good limitations identify the next appropriate experiment without implying that every task must run a full server before any useful conclusion is possible.

## JF-02A: calculate the exact range

The accepted integer interval is one through 1,073,741,823 inclusive. Negative one, zero and int.MinValue fail the lower comparison. The half maximum plus one and int.MaxValue fail the upper comparison. One, twenty and the half maximum pass both comparisons. Accepted values still require an allowed user context and successful downstream work before a successful response can be produced.

The largest accepted doubled value is 2,147,483,646. The next input would mathematically double to 2,147,483,648. Write these values using wider arithmetic in an oracle so the expected calculation does not reproduce the same overflow risk. Testing a guard with an oracle that silently overflows can make an incorrect implementation look correct.

The ordinary query construction evaluates the doubling before some grouped collection branches replace query.Limit with the original value. Therefore a later overwrite does not remove the need to protect that earlier expression. A channel branch returns through another path before ordinary query construction. The public guard remains uniform, so clients do not need to know which internal branch would have been selected to predict the accepted range.

The upper-boundary controller test uses an empty mocked view result. It verifies accepted forwarding without asking the server to allocate or retrieve a billion items. That is a deliberate choice of evidence boundary. The test is meaningful for arithmetic and composition while making no claim about operational feasibility.

## JF-02B: distinguish each mutation

A lower guard using only less-than-zero accepts zero incorrectly; zero is its smallest direct counterexample. A guard that rejects nonpositive values but omits the upper check accepts the half maximum plus one; that is the first positive arithmetic counterexample. An upper comparison using greater-than-or-equal rejects the half maximum incorrectly. An ordinary default limit of twenty does not distinguish any of those mutations.

If a candidate guard accepts all positive ints, testing int.MaxValue detects the missing upper rule, but the immediate next value above the intended boundary is a clearer explanation. Keep both edge clarity and representative extremes where they serve different purposes. A large collection of ordinary positive values adds little information about an off-by-one comparison.

A complete mutation map connects each requirement to a failing fixture. It should not demand that every test kill every mutation. The default test protects default preservation; the upper-edge test protects inclusion of the last safe value; the invalid tests protect rejection and absence of downstream calls. The suite's combined evidence is what matters.

## JF-02C: a practical maximum needs another argument

A sensible operational proposal begins with workloads and budgets. Measure candidate retrieval, grouping, selected item count, mapper batch work and response size under representative options. Determine which resource is constrained and what service-level behavior the product expects. Only then can a smaller maximum be justified as more than a guess.

Compatibility work should include both current and legacy routes because they share the action. Document whether clients currently request values above the proposed bound, how rejection is represented and whether a transition period is needed. This course does not invent such deployment evidence. A learner can produce a complete decision plan while honestly leaving the final production number unresolved.

Keep arithmetic and operational reasoning separate in the proposal. The current guard remains correct for its stated integer-doubling concern even if a practical policy should be stricter. Describing it as safe in every sense is too broad; describing it as useless because it permits large work ignores the specific overflow it prevents.

## JF-03A: validation order defines the direct trace

Invalid limit reaches no user, view or DTO service calls in the direct action path. A valid limit with a forbidden explicit subject can fail in RequestHelpers before user lookup. A permitted but missing subject reaches user lookup and returns not found. An existing user with an empty view result reaches mapping. A nonempty result additionally executes representative selection and count restoration.

For the forbidden-subject row, distinguish source-backed helper behavior from an executed fixture. The existing latest-media regression does not cover every role branch. A fabricated principal can establish the direct helper decision in a unit test, but it does not establish that production authentication would issue that principal. This boundary should remain visible in the ledger.

No downstream service calls is a narrower, more defensible assertion than no side effects anywhere. Framework logging, authentication and response execution are outside a direct invocation. Use names of the controlled collaborators so the reader knows exactly what was excluded by the fixture.

## JF-03B: moving a correct predicate can be incorrect

If the guard is moved below user resolution and lookup, invalid-limit inputs can now trigger identity errors or unexpected mock calls before reaching the same boolean condition. The regression's strict mocks help expose that reordered work. A failure may occur before the result assertion, which is useful evidence about the changed execution path rather than a reason to weaken the mocks.

The disposable experiment should preserve the original application source. Record the copied file hash, the small mutation and the observed failing case. Restore the copy or regenerate it before evaluating another mutation so combined defects do not obscure causality. The purpose is to learn what the guard's position protects, not to modify the user's running server.

A source-motion refactor can preserve successful outputs and still change rejection precedence. Reviewers should therefore examine invalid and multiply invalid inputs, not only the happy path. This principle applies to reads as well as writes because unnecessary service work and error categories are observable behavior.

## JF-03C: hosted precedence needs a hosted fixture

An unauthenticated invalid-limit request can be intercepted before the action. A malformed integer string can fail binding before an int argument exists. An authenticated representable but rejected integer can reach the action guard. These cases need different assertions and cannot be collapsed into one direct-method test.

A useful hosted fixture supplies controlled authentication and an empty view manager so it exercises routing and binding without expensive library work. Record whether it uses the application's actual exception handling and result serialization. If those components are replaced, the fixture proves a narrower pipeline and should be described accordingly.

Avoid predicting exact public error envelopes from the controller's string message alone. Response formatting can involve framework configuration and filters. The learning plan should identify which component turns a result into bytes and then verify that component when serialized behavior is the question.

## JF-04A: actor, request and subject are separate values

With omitted or empty requested userId, RequestHelpers returns the authenticated user's identifier. With an explicit matching identifier, it returns that identifier. With a different identifier and no administrator role, it throws SecurityException. With a different identifier and administrator role, it permits that subject. The subsequent user lookup can still return null, producing the action's not-found path.

The current helper treats Guid.Empty like omission. A shortcut using only the null-coalescing operator would preserve Guid.Empty and therefore change behavior. The difference is easy to miss if tests cover null and ordinary IDs but not the empty Guid. Exact absence semantics matter whenever several representations can mean use the default context.

Do not merge denied subject access with missing subject records in the matrix. One is a decision about the actor's permitted target; the other is a lookup result after an allowed target was chosen. Keeping them distinct supports both security reasoning and accurate client error handling.

## JF-04B: preferences belong to the resolved subject

An administrator requesting another user's latest media passes the subject User into the query and mapping. If the subject hides played items and the request omits isPlayed, the action sends false. The administrator's own preference is irrelevant to that decision in this path. Distinct actor and subject fixtures make this visible.

An explicit true or false request remains explicit even when the subject preference is true. The preference is used only for omission. A test that expects the preference always to force false would encode a different policy from the source. Write the six-row truth table before creating role-based combinations so two independent dimensions do not become confused.

The same-user-object assertion across query and mapper protects context association. It does not establish real database visibility for that user. A later integration test should inspect returned items under controlled libraries if visibility is the requirement being evaluated.

## JF-04C: shortcuts can remove policy

Replacing RequestHelpers with userId or principal fallback loses the administrator check for another explicit user and can mishandle Guid.Empty. A normal self-request still works, so a happy-path test is insufficient. The smallest access-decision fixture uses a nonadministrator principal and a different nonempty requested identifier.

Using the actor's loaded User for mapping after selecting another subject creates a second kind of bug. The query might retrieve under one user while user-data fields are populated under another. Distinct synthetic preferences and user IDs reveal that association problem without requiring real personal data.

The review should identify the removed rule and its observable consequence, rather than merely saying the helper is important. Concrete counterexamples make policy-preserving refactors possible because they state what an alternative implementation must continue to satisfy.

## JF-05A: preserve the nullable truth table

For either preference value, explicit true remains true and explicit false remains false. Omitted isPlayed becomes false only when HidePlayedInLatest is true. Omitted isPlayed remains null when the preference is false. That last distinction separates an unplayed-only filter from no played-state filter at the controller boundary.

Use exact nullable assertions. A predicate that merely checks the value is not true accepts both null and false and cannot protect the omission rule. Similarly, a fixture that initializes every user's preference to true never examines the null-preserving branch. Small combinatorial tables are useful when every combination represents a distinct policy state.

The test can keep all unrelated inputs simple: valid limit one, empty type arrays, existing user and empty view result. This isolates the preference rule and prevents group or mapping fixtures from obscuring a failed nullable assertion.

## JF-05B: forwarded intent can be transformed downstream

For an omitted filter and a subject who hides played items, the controller sends false. In the inspected ordinary downstream path, a recognized music collection parent changes the local filter to null. A channel parent uses a different query path and forwards the request value there. These source facts describe successive layers rather than contradictory results.

A report should say which layer was tested. Controller sends false is established by a captured query. Internal music query uses null requires inspecting or exercising the service branch. Final visible library results require still broader query evidence. The same word filter can otherwise conceal three different claims.

The trace should also note where a branch returns. If a channel path exits before ordinary parent processing, later rules cannot be applied to it merely because they appear lower in the same method. Following control flow is more reliable than searching for every assignment to a similarly named variable.

## JF-05C: a client needs an omission state

Use my preference should omit the isPlayed parameter, while played only sends true and unplayed only sends false. The first and third can produce the same controller value for a user who hides played items, but they express different intent and can diverge if the stored preference changes. Persisting an explicit false when the user chose preference would erase that distinction.

A client contract should avoid promising behavior that the server transforms for a category. Record the music and channel questions for integration and product review. The exercise is complete when it specifies request intent, known server interpretation and unresolved display wording; it need not invent an unsupported universal guarantee.

Retain your source map, boundary table, identity matrix and nullable-filter table as separate artifacts. They address independent dimensions and can be combined later to choose high-value integration cases without exploding into every possible cross-product.
