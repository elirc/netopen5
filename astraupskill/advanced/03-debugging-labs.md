# Make incomplete fixes fail for a clear reason

These labs describe deliberate mutations or observations in a disposable practice branch/copy. The current implementation already contains the reviewed guard. Do not introduce the mutations into your regular application merely to follow the prose.

## JF-L1 — the upper edge is off by one

Propose a guard that rejects `limit >= int.MaxValue / 2`. Test the threshold and its immediate successor. Both an over-restrictive guard and the correct guard reject `int.MaxValue`, so that single extreme case cannot distinguish them. Your minimal regression needs a valid edge and the adjacent invalid edge.

Write the doubled mathematical values by hand. Avoid performing an unchecked 32-bit multiplication as the test's own oracle; it could repeat the implementation's overflow mistake. The expected result should come from an independently stated bound.

## JF-L2 — correct status after forbidden work

Move the guard mentally after user or library lookup. The eventual action result is still 400. Which mock verification catches the earlier work? Configure no valid user for the invalid-input case so the guard must be self-contained. Record the specific dependency that should receive zero calls, rather than a vague statement that “nothing happened.”

## JF-L3 — a default changed unnoticed

Compare two tests: one passes `limit: 20`, the other omits limit. Change the declaration's default in your exercise copy. Explain why only one test detects the default regression. Repeat for grouping. For the HTTP contract, design an additional request that omits the query parameter; a direct C# optional-argument test does not exercise query binding.

## JF-L4 — test fixture rejects a valid result

Inspect the base controller's typed `Ok` result. A strict exact-type assertion can fail while status and response value remain correct. Use an assignability assertion plus explicit status and payload assertions when that matches the API contract. Do not weaken an assertion indiscriminately: explain the exact permitted variation and the behavior still required.

## JF-L5 — a query never reaches the action

For the proposed HTTP lab, compare a valid authenticated request with `limit=abc`, a representable nonpositive integer and a request with no authentication. Record whether rejection occurs in binding/validation, middleware or the action. Do not assume a 400/401-looking response proves that the integer guard executed.

Use an owned test host and instrumented fake collaborators. Avoid configuring a real library merely to test malformed input. Capture route, query, configured identity, status and collaborator observations without storing an actual bearer token.

## Debugging note format

For each case, write the trigger, expected first rejecting layer, observed layer, surviving state/work count and one assertion that would catch the regression. If your experiment stops at build or host startup, record that boundary and investigate it before describing any HTTP behavior as verified.
