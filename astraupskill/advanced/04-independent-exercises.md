# Six assignments from arithmetic to HTTP recovery

## JF-01 — complete the boundary matrix

Add a prediction for each row in the boundary table: accepted guard, expected user lookups, expected library-view calls and whether DTO conversion should run. Assume a valid user for accepted cases and empty service results. Verify invalid boundaries with strict mocks. Keep huge valid values in mocked tests so the lesson does not trigger a real enormous query.

## JF-02 — preserve forwarding choices

Design cases for explicit `isPlayed=true`, explicit false, omission with `HidePlayedInLatest=true`, and omission with that preference false. Add grouping on/off and missing/present parent IDs. Inspect the actual query object in the mock predicate. Merely returning 200 does not prove that the requested filter reached the service.

## JF-03 — compatibility without duplicated validation

Compare the current and legacy controller methods for invalid input, ordinary input and omitted defaults. Require both to reach the same validation policy. Then write a review of a proposed patch that copies the predicate into the legacy action. Explain the maintenance risk and which test would detect divergence later.

## JF-04 — build an owned HTTP test fixture

Create a separate test fixture that uses the real controller and routing with a controlled test authentication setup and fake library collaborators. The existing [test project](../../jellyfin/tests/Jellyfin.Api.Tests/Jellyfin.Api.Tests.csproj) already references ASP.NET MVC testing support, but that dependency alone does not mean a suitable application host is implemented for this lesson.

Specify how the fixture starts, which services it replaces, how it supplies a fictional identity and how it stops. Send requests to the current and compatibility paths. Include an omitted limit, an ordinary positive limit, zero, malformed text, an out-of-range integer representation and an unauthenticated case. Predict the first relevant layer for each; then verify actual statuses and response shapes from the configured host.

Label assertions honestly: test authentication establishes the test-host behavior, not the production identity provider. A fake library returning no items establishes forwarding and serialization, not real media selection.

## JF-05 — operational limit proposal

Suppose product requirements now call for a smaller maximum page size. Write a proposal explaining the new bound, compatibility impact, defaults and error contract. Separate this policy from the existing arithmetic invariant. A number like 100 may be reasonable for a particular product, but it must come from requirements/measurement rather than being smuggled in as the only mathematically safe value.

## JF-06 — review a misleading claim

Review: “All boundary tests pass, so requests up to 1,073,741,823 items are safe in production.” Explain exactly what the tests establish and what they do not. Rewrite the statement to retain the arithmetic result while identifying capacity, allocation, latency and service behavior as separate concerns requiring appropriate evidence.

Submit one minimal counterexample and one precise assertion with every review. The [solution guide](05-solutions-and-review.md) supplies reasoning after your independent attempt.
