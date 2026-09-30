# 08. Preserve position through DTO mapping

The latest-media action keeps two parallel arrays: resolvedItems and childCounts. It then maps resolvedItems to DTOs and uses each DTO's index to recover the corresponding saved child count. This is a positional contract. Correct item selection is not enough if mapping changes order or cardinality unexpectedly.

## Trace the arrays together

Suppose three groups select container A with two collected children, child B with no saved group count and album C with one collected child. The arrays are selected items A, B, C and saved counts two, zero, one. After mapping, the action writes two to the first DTO's ChildCount, leaves the second DTO's existing value unchanged and writes one to the third DTO's ChildCount.

The zero case is especially easy to misdescribe. The controller does not set ChildCount to zero for every ungrouped item. It assigns only when the saved count is positive. Any value already produced by the DTO service remains for the zero slot. A test should initialize that value distinctly if it wants to establish the no-overwrite behavior.

The mapping call passes skipVisibilityCheck true. In the inspected [DtoService](../../../jellyfin/Emby.Server.Implementations/Dto/DtoService.cs), that means accessibleItems is the supplied list rather than a visibility-filtered replacement. The service allocates a DTO array of that count and iterates the selected items by index. This source supports the positional relationship in the current path. It still deserves attention during refactors because the controller relies on it.

## Why filtering can break an association

Imagine a hypothetical mapper that removes the middle item but returns A and C. A controller loop that blindly pairs resulting index one with childCounts index one would attach B's saved count to C or fail to apply C's intended count. Reordering can create the same kind of error without changing the count. Testing only response length does not detect those association failures.

The current real service's skip-visibility path avoids that particular filtering step, but a mock can accidentally return a sequence that violates the expected association. Use valid contract fixtures for ordinary tests and label deliberately malformed outputs as assumption probes. Otherwise a test can manufacture an impossible collaborator behavior and present the resulting failure as a current production defect.

A proposed identity-based mapping could store saved counts by selected item ID and apply them to DTO IDs. That might tolerate reordering, but duplicate selected IDs and different count meanings would need a policy. It is not automatically superior to a positional contract whose service guarantees are explicit. Evaluate the actual risks and costs before replacing the design.

## Exercise JF-08A: assert complete associations

Build the three-group fixture described above with distinctive IDs and preexisting DTO ChildCount values. Verify the exact ordered pairs of DTO ID and final ChildCount. Ensure the middle DTO retains its mapper-provided value because its saved count is zero.

The fixture should fail if the mapper output is reversed, if every count is overwritten indiscriminately or if the action uses the first group's count for every DTO. Write those mutations beside the assertions they are intended to trigger. This makes the test's purpose clearer than a broad snapshot with no explanation.

## Exercise JF-08B: inspect the trust boundary

Trace why the action asks DTO mapping to skip visibility checks. Identify the earlier collaborator named in the comment and inspect how its query uses the resolved user. State what additional evidence would be needed to verify real visibility for representative items under different library categories.

Do not conclude that visibility is unnecessary because a flag skips one check. The flag relies on work having been done earlier. A refactor that changes candidate retrieval, substitutes a service or adds a new representative type should reassess that assumption explicitly.

## Exercise JF-08C: compare positional and identity joins

Design a small alternative that associates counts by identity. Specify behavior when two selected positions share an ID, when the mapper returns an unexpected ID and when a DTO is missing. Compare those decisions with the current positional contract.

Provide a decision note rather than changing production code. The note should include one scenario where identity association helps and one where it introduces ambiguity. A useful design review acknowledges that changing representation moves assumptions; it rarely eliminates every assumption.

## Review standard

A strong answer preserves item-to-count associations and recognizes the positive-count-only overwrite. It reads the actual mapping path before accusing it of filtering and treats visibility as an explicit upstream dependency rather than a property established by a unit-test mock.
