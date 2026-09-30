# 13. Review visibility as a chain of assumptions

The latest-media path resolves a subject user, retrieves candidates in that context, selects representatives and maps them with skipVisibilityCheck true. Visibility is therefore distributed across a chain of responsibilities. The goal of this chapter is to construct an evidence-based review of that chain, not to declare it safe or unsafe from one flag.

## Separate three questions

First, may the actor request this subject user's context? RequestHelpers answers a local version of that question through same-user and administrator rules. Second, which candidates are available to that subject in the selected library path? UserViewManager and its library or channel dependencies participate there. Third, what associated information is included when selected representatives are mapped? DtoService uses the supplied user and options.

These questions can fail independently. Correct actor-to-subject authorization does not prove every candidate query respects the subject. Correct candidate filtering does not prove mapper user-data fields use the same subject. Correct DTO fields do not prove that a representative container was selected under the intended visibility assumptions. A review matrix should keep these claims separate.

The controller explicitly passes the loaded User to both LatestItemsQuery and DTO mapping. That is good source evidence for context continuity at this layer. The view manager constructs InternalItemsQuery with the user on ordinary and channel paths. Broader conclusions require following those collaborators or executing controlled integration fixtures. Stop the claim where the inspected evidence stops.

## Inspect representative changes

Grouping can replace a child with a container. A test that verifies only child candidate visibility may therefore leave a gap around the object ultimately mapped. The album exception means even a one-child group can display a container. Include representative identity in a visibility investigation so the observed DTO can be traced back to the selected source object.

The mapper's skipped visibility filter also preserves the positional association used for child-count restoration. Re-enabling filtering as a speculative repair could change cardinality or order assumptions. A correct change would need to preserve both access behavior and count association. Security-sensitive refactors still need ordinary data-contract reasoning; one concern does not make the other disappear.

Do not use real private library data to demonstrate the concept. A synthetic fixture with two users, two parents and clearly marked accessible and inaccessible items is easier to reason about and avoids unnecessary exposure. The important artifact is the access matrix and actual returned identities, not realistic personal media names.

## Exercise JF-13A: build a trust ledger

Create rows for actor-to-subject resolution, root-parent selection, explicit-parent retrieval, channel retrieval, grouped representative choice and DTO user-data mapping. For each row, name the component responsible, the context supplied and the evidence currently available.

Add a column for what would invalidate the assumption. Examples include substituting an unfiltered candidate provider, loading DTO user data under the actor instead of the subject or returning reordered DTOs after filtering. These are review scenarios, not assertions that the current implementation contains those defects.

## Exercise JF-13B: specify an access fixture

Use two synthetic users and a small library with one shared parent and one restricted parent. Define expected items for self access, permitted administrator subject access and denied nonadministrator cross-user access. Include an album representative and an ungrouped item.

State which tests can use direct mocks and which must execute the real query or host pipeline. A mock that simply returns the expected accessible list cannot prove the real query enforces that access matrix. It can only verify how the controller handles a list already filtered by the mock.

## Exercise JF-13C: review a service substitution

A proposed cache returns latest groups without calling the original view manager. List the user, parent, filter, grouping and option dimensions that could affect cache identity or mapped output. Explain which visibility and freshness assumptions must be preserved before the controller can continue skipping its mapper filter.

Do not design a full production cache in this exercise. Produce a review checklist grounded in the actual request fields and representative behavior. Mark unknown dependencies for investigation rather than guessing a complete cache key from the endpoint name alone.

## Review standard

A complete ledger avoids both complacency and unsupported alarm. It shows where context flows, where authority is checked and where broader evidence is required. The proposed fixtures make access mistakes observable without treating a mock's prepared result as proof of real authorization or visibility.
