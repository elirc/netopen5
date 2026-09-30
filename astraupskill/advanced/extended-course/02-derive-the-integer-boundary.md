# 02. Derive the integer boundary

The limit guard rejects values at or below zero and values above int.MaxValue divided by two. Its purpose is tied to downstream arithmetic, not to an arbitrary round number. In [UserViewManager](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs), the ordinary internal query is initially assigned limit multiplied by two. To understand the guard, derive the largest positive integer whose doubled value fits in the signed integer range.

## Work from the operation backward

A signed 32-bit integer has a maximum value of 2,147,483,647. Integer division by two yields 1,073,741,823. Doubling that value produces 2,147,483,646, which is representable. Increasing the accepted limit by one would make the mathematical doubled value 2,147,483,648, outside that range. The guard therefore accepts the half-maximum boundary and rejects the next integer.

Write the inequalities before the condition. The desired arithmetic requirement is positive limit and twice limit no greater than the integer maximum. Rearranging for integer inputs gives limit at least one and at most the floored half maximum. This derivation makes the comparison operators reviewable. Using greater-than-or-equal at the upper guard would incorrectly reject the last safe boundary.

The lower boundary expresses more than overflow prevention. Zero and negative limits do not represent a positive requested item count under this endpoint's current contract. Testing only very large values would miss a guard that prevented overflow while accepting nonsensical nonpositive requests. The two sides of the condition address distinct classes of input.

## Distinguish arithmetic safety from feasible work

An accepted upper boundary near one billion does not imply that processing such a request is operationally sensible. The guard prevents a particular integer-doubling overflow. It does not prove bounded memory, acceptable latency, database capacity or network response size. Operational limits require separate evidence and a deliberate API policy.

Keep the huge accepted boundary in a controller test with mocked dependencies returning an empty result. The test can verify that the integer is forwarded unchanged without allocating that many media objects or querying a real server. This is an example of choosing a test boundary that makes a dangerous-to-scale input cheap and deterministic to examine.

A proposed practical maximum should be documented as a new contract, with compatibility and workload reasoning. Do not quietly replace the arithmetic limit with a smaller number in a learning exercise and call it a behavior-preserving fix. Existing accepted inputs would change, even if most clients never request them.

## Read the downstream branches carefully

The internal query is initialized with the doubled limit on the ordinary path. Some grouped collection branches then replace query.Limit with the original limit before calling GetLatestItemList. A channel parent follows another path that forwards request.Limit directly. These details prevent the overstatement that every request ultimately retrieves exactly twice its requested count.

The guard still protects the arithmetic expression that is evaluated when the ordinary query is constructed. A later reassignment cannot make an earlier overflowing calculation safe. Conversely, a branch that returns before constructing that query may not evaluate the doubling at all. The endpoint uses a uniform input rule rather than exposing a branch-dependent public maximum.

## Exercise JF-02A: build the boundary table

Include int.MinValue, negative one, zero, one, twenty, the half maximum, the half maximum plus one and int.MaxValue. For each value, record accepted or rejected, which comparison decides it and whether downstream user/view/DTO work should occur in a direct action test.

For accepted values, calculate the mathematical doubled value in a representation that cannot itself overflow during your prediction. A worksheet using wider arithmetic can serve as an independent oracle. Do not compute the expected result with the same narrow unchecked multiplication whose safety you are trying to establish.

## Exercise JF-02B: reject plausible mutations

Consider four proposed guards: limit less than zero; limit less than or equal to zero; limit at least one with no upper check; and the current lower check combined with upper greater-than-or-equal. Identify the smallest useful input that distinguishes each incorrect version from the intended contract.

Explain why a single default-value test cannot detect any of those boundary mistakes. Then choose a compact regression set that covers each distinct requirement without pretending that many ordinary positive values provide the same information as exact edges.

## Exercise JF-02C: design a practical-limit proposal

Write a separate proposal for a realistic service budget. Identify the measurements needed: candidate count, grouping ratio, mapping cost, selected DTO fields and serialized size. Explain how a smaller maximum would affect current clients and legacy routes. Include a compatibility plan and a way to communicate rejection.

Do not choose a final production number solely to complete the exercise. A complete answer can state the decision process and the evidence still required. The important skill is separating a proven arithmetic bound from an operational policy that remains to be designed.

## Review standard

A strong answer derives the exact accepted range, names the operation that motivates it and recognizes branch-specific downstream behavior. It never equates a passing mocked upper-boundary test with proof that a live server can process that request economically.
