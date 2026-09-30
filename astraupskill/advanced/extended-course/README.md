# Jellyfin latest-media engineering course

The completed twenty-four-chapter course follows the actual latest-media request from input boundaries through identity, retrieval, grouping, DTO mapping, errors, diagnostics, and change design. It includes seventy-two independent exercises, four separate review guides, one runnable extracted-source lab, and two capstones with separate sixty-point rubrics. Application source and existing learner work remain unchanged.

## Complete route

Read chapters in order and record predictions before opening the reviews. Chapters 01-10 establish the endpoint contract and focused-test evidence. Chapters 11-16 deepen binding, retrieval branches, visibility assumptions, build context, work budgets, and errors. Chapters 17-24 develop consistency, cancellation proposals, diagnostics, bounded source execution, independent properties, compatibility, and assessed capstones.

- [01. Follow the latest-media request](01-follow-the-latest-media-request.md)
- [02. Derive the integer boundary](02-derive-the-integer-boundary.md)
- [03. Validation order and observable work](03-validation-order-and-observable-work.md)
- [04. Resolve user identity and context](04-resolve-user-identity-and-context.md)
- [05. Nullable filters and user preferences](05-nullable-filters-and-user-preferences.md)
- [06. DTO options and requested cost](06-dto-options-and-requested-cost.md)
- [07. Group candidates and choose representatives](07-group-candidates-and-choose-representatives.md)
- [08. Preserve position through DTO mapping](08-preserve-position-through-dto-mapping.md)
- [09. Read and strengthen the focused tests](09-read-and-strengthen-the-focused-tests.md)
- [10. Legacy routes and contract equivalence](10-legacy-routes-and-contract-equivalence.md)
- [11. Bind collections without assuming syntax](11-bind-collections-without-assuming-syntax.md)
- [12. Trace parent and library query branches](12-trace-parent-and-library-query-branches.md)
- [13. Review visibility as a chain of assumptions](13-review-visibility-as-a-chain-of-assumptions.md)
- [14. Build context and reproducible test evidence](14-build-context-and-reproducible-test-evidence.md)
- [15. Budget query, grouping and mapping work](15-budget-query-grouping-and-mapping-work.md)
- [16. Classify errors across the request pipeline](16-classify-errors-across-the-request-pipeline.md)
- [17. Reason about consistency between retrieval and representation](17-reason-about-consistency-between-stages.md)
- [18. Cancellation, deadlines, and work that has already happened](18-cancellation-deadlines-and-partial-work.md)
- [19. Diagnostic ledgers and minimal reproductions](19-diagnostic-ledgers-and-minimal-reproductions.md)
- [20. Execute a bounded source-selection lab](20-execute-a-bounded-source-selection-lab.md)
- [21. Properties, counterexamples, and independent test oracles](21-properties-counterexamples-and-test-oracles.md)
- [22. Design a compatible operational policy](22-design-a-compatible-operational-policy.md)
- [23. Capstone: preserve selection while changing an operational contract](23-capstone-preserve-selection-under-change.md)
- [24. Capstone: evidence, recovery, and a final engineering assessment](24-capstone-evidence-recovery-and-final-assessment.md)

## Separate reviews and runnable lab

- [Review 01: boundaries, identity, and preferences](review-01-boundaries-identity-and-preferences.md)
- [Review 02: options, groups, tests, and compatibility](review-02-options-groups-tests-and-compatibility.md)
- [Review 03: binding, query evidence, and errors](review-03-binding-query-evidence-and-errors.md)
- [Review 04: consistency, labs, properties, and capstones](review-04-consistency-labs-properties-and-capstones.md)
- [Lab evidence guide](lab-evidence-selection-and-mutations.md)
- [Executable extracted-source selection lab](labs/latest_selection_lab.py)

The baseline lab passed twenty-two assertions. Three deliberate generated-source mutations compiled and failed at their predicted semantic assertions. Both selected original source hashes remained unchanged after every invocation. The lab extracts real grouping, representative-selection, and count-restoration statements, while media types and candidate retrieval are explicit stand-ins. It uses an owned temporary .NET 10 SDK project with no third-party package references and cleared package sources.

This is algorithm execution, not a full Jellyfin build, controller integration run, or hosted HTTP test. The existing focused tests and broader source paths were reviewed; no full server test suite, real media library, authentication flow, or network request was executed for this course. Large arithmetic limits belong in mocked or isolated fixtures, never enormous real-library requests merely for a lesson.

## Assessment and optional further work

Chapter exercises have separate answer coverage in the four review guides. Chapters 23 and 24 each provide a complete sixty-point capstone rubric; their design-only and implementation routes have explicit evidence requirements. A proposed operational cap, cancellation path, cursor, cache, or response-format change remains a learner proposal, not shipped behavior added by the course.

The instructional route is complete. Optional further work includes implementing a capstone, running the focused full-project suite in an owned prepared environment, adding hosted binding and middleware tests, and measuring controlled operational workloads. No required chapter remains planned-only. Keep source observations, executed experiments, and proposed work distinct in every final packet.

[Earlier advanced course](../README.md) | [Original course](../../README.md)
