# 21. Properties, counterexamples, and independent test oracles

Example-based tests make individual branches concrete. Property-oriented reasoning asks which relationships hold across many valid inputs and which attractive relationships are false. Use [UserViewManager.GetLatestItems](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs), [the controller's selection and restoration](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), and [the bounded lab](labs/latest_selection_lab.py) as anchors. This chapter specifies additional learner experiments; it does not claim a property-testing framework was installed or a generated suite was executed.

The objective is to derive properties from the actual algorithm and then challenge them with small counterexamples. A property is useful only when its preconditions, observation boundary, and oracle are explicit. A slogan such as larger limits return more of the same items can be false once grouping changes representative identity.

## Begin with a valid input domain

For the controller's representative loop, every tuple must have a nonempty child list. The real grouping method constructs groups by adding a candidate, so its normal output satisfies that shape. A hand-built collaborator result can violate it. Keep malformed tuples in a separate robustness or contract-violation category instead of mixing them with normal property inputs.

For the extracted grouping lab, use positive finite limits, stable container identities, and deterministic candidate lists. The HTTP action's arithmetic guard is outside that lab, so its input domain must be stated by the harness. Testing a negative limit directly against the extracted method does not reproduce the endpoint's validated path.

The stand-in media types model only folder status, identity, and container relationships. Properties involving actual visibility, inheritance behavior, or metadata retrieval require the real types and dependencies. Do not allow a generator to imply a broader domain than the stand-ins represent.

## Derive a simple ungrouped prefix property

When grouping is disabled and the candidate provider returns a fixed list, each visited candidate creates its own null-container group. The loop stops when group count reaches the positive limit. Therefore, the group children correspond to the first minimum of candidate count and limit candidates, preserving order. This property is about the controlled candidate list, not the private retrieval query's own limit or filters.

A useful generated experiment can create short candidate arrays with unique labels, choose modest positive limits, and compare the flattened one-child groups with an independently sliced expected prefix. Include empty candidates, fewer candidates than limit, exact equality, and more candidates than limit. This tests a clear relationship without duplicating the grouping implementation in the oracle.

If a candidate is a folder while grouping is enabled, it similarly bypasses container grouping for that candidate. A mixed fixture can verify that folder treatment does not accidentally merge it with other media sharing a container property. The precondition and expected observation must remain explicit.

## Challenge monotonic representative identity

Suppose candidates are A1, A2, B1, where A1 and A2 share a nonalbum container A. With group limit one, the loop stops after A1, producing a singleton group whose controller representative is A1. With group limit two, A2 is collected before B1 creates the second group, so the controller represents the first group with A instead.

The larger limit did not merely append another representative to an unchanged response prefix. It changed the first representative identity from child to parent. This is a compact counterexample to naive prefix-monotonicity of final DTO identities. It follows from the combination of early grouping termination and representative selection, not from unstable database ordering.

A client caching results by position or assuming that increasing the limit only adds rows could mishandle this behavior. A proposed API change promising stable prefixes would need a different grouping or representation contract. Do not write a property test for that promise and then call the current source broken without first acknowledging the new requirement.

## Distinguish group identity from object identity

Container grouping uses a dictionary keyed by Guid. Two container objects with the same identity merge into one group before the threshold ends scanning, while the first object's reference is retained in the tuple. A property can state that object-reference substitution with the same container identity does not create an additional group, under a fixture that still visits both candidates.

The visit precondition matters. If the first candidate already reaches a limit of one, the second is never examined, so the test cannot distinguish identity-based merging from any other behavior. Choose a limit and candidate order that keep the loop running through the relevant pair. Reachability is part of property design, just as earlier guard isolation was part of example-based tests.

Do not infer item deduplication from container grouping. Repeating the same child candidate can append it again to a group's child list in the inspected algorithm. A proposed deduplication property would be a behavior change unless another boundary guarantees unique candidates. State whether uniqueness is a provider precondition or an algorithm responsibility before writing expected counts.

## Use restoration idempotence carefully

For a fixed count vector and a fixed ordered DTO list, applying the positive-only restoration loop twice produces the same ChildCount values as applying it once. Positive positions are assigned the same number again, while zero positions remain as supplied. This is a local idempotence property of the loop, not an idempotence guarantee for the whole endpoint across changing library data.

A generated test can seed arbitrary small mapper counts, use a count vector containing zeros and positives, apply restoration once, snapshot values, apply it again, and compare. It should also assert that zero positions preserve their original seed. Otherwise a mutated loop that overwrites zero could still be idempotent and pass the repeat-only property.

This illustrates why one elegant property rarely replaces examples. The mutated all-position assignment is idempotent too, but violates the intended preservation rule. Pair algebraic relationships with concrete boundary expectations so a broad property does not certify the wrong behavior.

## Separate cardinality from correspondence

The selected real DTO service allocates an output array for accessible items and fills it by index. With skipVisibilityCheck true, it uses the input items as the accessible list. This supports the controller's positional restoration contract. A property of the controller-plus-mapper boundary can require equal cardinality and corresponding identities, but a fake mapper must implement or deliberately violate that contract explicitly.

A mapper returning fewer rows may leave some recorded counts unused; one returning more can make the count-array indexing invalid. A mapper returning the same number in a different order can silently attach counts to the wrong items. These are different counterexamples and should not be collapsed into mapper failed.

If proposing identity-keyed restoration, generate duplicate representative IDs and missing outputs as design cases. A dictionary that silently overwrites duplicates can introduce a new ambiguity. The current positional method's simplicity depends on a real collaborator contract; a replacement should be evaluated against its own complete assumptions.

## Design generators for meaning, not volume

Use a small vocabulary of candidate shapes: standalone item, folder, singleton nonalbum container, repeated nonalbum container, and singleton album. Generate short sequences and modest limits that reach each branch. Record a seed if the generator is randomized, and retain the minimized failing case as a deterministic regression example.

Do not use the half-maximum integer as a real candidate-list size. The arithmetic guard belongs in a mocked boundary test; grouping properties can be explored with a handful of items. Large allocations add cost without improving the logical discrimination of a two- or three-candidate counterexample.

A shrinking strategy should preserve the failure's preconditions. Removing a candidate that kept the loop below its threshold can make an identity-merging failure disappear for the wrong reason. A good minimized case still reaches the branch under investigation and explains why every remaining element is necessary.

## Review an independent oracle

An oracle that calls the same method twice and compares outputs mainly tests repeatability under that fixture, not correctness. An oracle that reproduces every source conditional in a second function risks copying the same defect. Prefer independent tables, simple mathematical relations with stated preconditions, or explicitly written expected IDs for minimal cases.

For grouping, the ungrouped prefix is a simple independent relation. For representative selection, the four-shape table is clearer than a second conditional implementation. For restoration, zero-preservation and positive-overwrite assertions directly express the contract. For limit monotonicity, a counterexample is more useful than forcing an invalid universal property.

Mutation testing can evaluate these oracles. Change the album exception, the early-break comparison, or the zero-restoration condition in a generated copy and identify which property or example fails. If a mutation survives, explain whether the property is too weak, the inputs never reach the branch, or the change is equivalent under the stated domain.

## Independent exercises

Exercise JF-21A asks you to specify the ungrouped prefix property with exact preconditions and an independent oracle. Include four candidate-count/limit relationships and one folder-bypass case. State why this does not verify private retrieval limits or HTTP validation.

Exercise JF-21B asks you to reproduce the limit-one versus limit-two representative counterexample and critique a client that assumes stable response prefixes. Add a repeated-container-identity fixture whose limit ensures both candidates are visited.

Exercise JF-21C asks you to design a restoration property suite that kills the zero-overwrite mutation even though that mutation remains idempotent. Include one mapper cardinality or ordering violation and explain how a future identity-keyed design would need different assumptions. Review the separate answers after writing the properties.

## Review checkpoint

You have completed the chapter when you can reject an appealing but false property with a minimal counterexample, state a true property's input domain, and explain why your oracle is independent. The goal is discriminating evidence, not the largest generated test count.


[Separate hints and full review](review-04-consistency-labs-properties-and-capstones.md) | [Complete course route](README.md)
