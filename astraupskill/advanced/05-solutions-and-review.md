# Evaluate the boundary and the claim separately

## Expected answers

JF-L1: the threshold itself is valid. A `>=` upper comparison rejects one valid value. Testing the threshold and threshold+1 distinguishes that mistake. Testing only the largest possible integer does not.

JF-L2: rejected integer input should return before user, view and DTO access. An exact status assertion alone misses unnecessary downstream work. Use the focused test's strict dependency pattern and verify the expected absence of calls.

JF-L3: explicitly passing 20 cannot establish the declared default. Omitting the optional C# argument tests that call-site behavior. An HTTP request omitting the query parameter adds routing/binding evidence and must be exercised through an HTTP pipeline.

JF-L4: Jellyfin's base controller returns a typed subclass. Assignability plus status/value assertions can preserve the intended contract without insisting on an exact base type. This is not permission to accept any result or ignore the response content.

JF-L5: malformed text cannot be supplied to the action's `int` parameter through an ordinary direct C# call. It belongs to a binding-level test. Authentication middleware can reject an HTTP request before action execution. Your recorded status needs the configured fixture and observed call path to support a claim about a particular boundary.

## Forwarding reasoning

For JF-02, explicit played-state values remain explicit. If the value is absent and the user's hide-played preference is true, the action supplies false. If absent and the preference is false, the nullable query value remains absent. Grouping and parent identity are separate dimensions; test a small purposeful matrix rather than every combination without a rationale.

For JF-03, legacy delegation reduces the number of places owning the rule. A shared implementation does not remove the need to test route-specific binding or compatibility behavior. Changes to a route parameter or attribute can break callers even while a direct method delegation test passes.

For JF-04, state which parts of the host are real and which are substitutes. A response from a handwritten fake route is not a test of Jellyfin's controller. A real controller with fake services can establish action integration and serialization without claiming a real media-library result.

## Review rubric

Score each row 0 for absent, 1 for explained, 2 for demonstrated:

| Area | Full-credit requirement |
|---|---|
| Arithmetic | Both accepted and rejected adjacent edges derived correctly |
| Work boundary | Invalid input avoids specified collaborator calls |
| Compatibility | Defaults and legacy delegation covered by distinct meaningful cases |
| HTTP layer | Real routing/binding setup described and actual observations recorded |
| Claim accuracy | Test scope separated from capacity and deployment claims |

For a controller-only submission, mark HTTP work explicitly deferred instead of claiming a full HTTP score. That can be a complete controller exercise, but it is not the full HTTP capstone. Keep distinct outcomes rather than treating every unexecuted test as a failure or silently counting it as passed.

## Practice a useful review comment

“The new test passes 20 explicitly, so changing the optional default to 21 would not fail it. Add a call that omits limit and assert the forwarded query. Keep a separate HTTP omission case for query binding.” This is more actionable than asking for “better coverage” without naming the missing behavior.
