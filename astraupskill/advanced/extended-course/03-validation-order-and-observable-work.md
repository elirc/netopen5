# 03. Validation order and observable work

A guard's location can matter as much as its boolean expression. In [GetLatestMedia](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), the limit check precedes RequestHelpers.GetUserId, user lookup, view retrieval and DTO mapping. This gives invalid-limit requests a narrow direct-call behavior: return a bad-request result without beginning those later stages.

## Model the failure frontier

Draw a line after each stage and ask what has happened before a failure there. Before the guard passes, no user/view/DTO collaborator call is required. After identity resolution, a security exception may have occurred without user lookup. After user lookup, a missing user produces not found. After view retrieval, representative selection and mapping become possible. Each location has a different observable trace.

This is useful even for a read endpoint. Reads can consume resources, invoke expensive services or expose different error behavior. Preventing unnecessary work on invalid input is a concrete contract that can be checked with mocks. Avoid the vague phrase no side effects unless you define the boundary: a direct controller test can show no calls to specified collaborators, not that no logging or framework activity occurred anywhere in a hosted request.

The focused regression creates strict mocks for user, view and DTO services. Invalid cases do not configure successful downstream behavior. If the action begins an unexpected call, the strict mock can fail the test. Explicit VerifyNoOtherCalls assertions make the intended absence visible to a reader rather than leaving it implicit in mock setup.

## Competing invalid conditions

Suppose a direct call has both an invalid limit and a requested user that the supplied principal may not access. The source checks limit first. That observation does not imply that an unauthenticated HTTP request bypasses authorization middleware and receives the same bad-request result. The hosted pipeline can reject a request before the action runs. Keep action-level validation precedence distinct from pipeline-level precedence.

Similarly, an invalid integer string in a URL is not an int argument passed to the method. Model binding must first interpret it. A direct test using int.MaxValue examines a representable but rejected integer; it does not examine text outside the integer range. Those are separate input classes and belong in separate tests.

Validation order is a compatibility concern when clients depend on stable error categories. Moving user lookup before the guard could change which error is returned for multiply invalid direct inputs and increase downstream work. A refactor should state whether such changes are intentional. The final success result may remain identical while the rejection contract changes.

## Exercise JF-03A: write a call ledger

Create rows for invalid limit, valid limit with inaccessible requested user, valid limit with missing user, valid limit with empty view result and valid limit with nonempty groups. Record which stages are reached and which are excluded. Use source inspection for the first ledger; mark execution separately when you run a fixture.

For each row, write one negative-call assertion that would catch an accidental reorder. Invalid limit should not call user lookup. Missing user should not call the view manager. A view failure should not yield a successful DTO mapping result. Be precise about which collaborators your test fixture actually controls.

## Exercise JF-03B: move the guard in a disposable experiment

In a disposable copy, move the guard below user lookup without changing its expression. Predict which existing invalid-limit tests fail and why. If the test principal lacks a usable user identifier, identity resolution may fail even before a strict service mock is reached. Describe that causal chain rather than reporting only that the test turned red.

Restore the original ordering in the experimental copy and verify the chosen case again. Keep the actual application file unchanged. The experiment teaches that an apparently harmless code-motion refactor can alter observable behavior even when the predicate itself is correct.

## Exercise JF-03C: design hosted precedence tests

Specify a small HTTP matrix containing authenticated valid input, authenticated invalid limit, unauthenticated invalid limit and malformed integer text. Identify the expected boundary for each assertion: route selection, authentication result, model-binding rejection or action guard. Do not fill in exact response shapes without checking the host's actual configuration.

Use a disposable integration fixture with controlled services and authentication. The purpose is not to make a large live media query. A good hosted test can establish pipeline behavior while keeping downstream retrieval empty and cheap. Record how the fixture differs from a real server before drawing deployment conclusions.

## Review standard

The finished call ledger should explain both what runs and what cannot run on each path. A strong answer distinguishes invalid argument values from unparseable HTTP text and avoids promoting direct-action validation order into a claim about middleware that the test never executed.
