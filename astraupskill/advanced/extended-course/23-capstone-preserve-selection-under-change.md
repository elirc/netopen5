# 23. Capstone: preserve selection while changing an operational contract

This capstone asks you to propose and, optionally, implement a modest operational limit policy while preserving the latest-media selection contract. The course supplies a complete assignment and assessment rubric. It does not change the Jellyfin application, create a deployment, or require a full server environment merely to complete the design route.

Use [UserLibraryController](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), [UserViewManager](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs), [DtoService](../../../jellyfin/Emby.Server.Implementations/Dto/DtoService.cs), and [the extracted-source lab](labs/latest_selection_lab.py). These anchors make the assignment concrete: the change concerns accepted request bounds, while identity, grouping, representative choice, DTO correspondence, and positive-only count restoration remain protected contracts.

## State the requested change precisely

Choose a proposed operational maximum appropriate to a small synthetic benchmark plan. The exact value is a design choice for this exercise, not a recommendation based on production measurement. Reject larger requested limits with a documented bad-request contract rather than silently clamping or returning a partial list. Preserve the current default request and the smallest valid limit.

Keep arithmetic safety explicit even if the proposed maximum is much smaller than the overflow boundary. The new policy is an operational decision layered on the current arithmetic concern. Your specification must say whether rejection occurs before identity resolution and downstream services, and must explain any reason the policy would need subject-specific information instead.

Do not bundle a cache, asynchronous rewrite, new pagination protocol, and structured error migration into the same implementation. You may discuss them as alternatives, but the chosen deliverable should remain reviewable. If you also propose a new error body shape, identify it as a separate compatibility decision and give it its own acceptance cases.

## Deliver a baseline contract inventory

List the current default limit and grouping behavior, the arithmetic acceptance range, nullable played-intent resolution, subject identity rules, parent forwarding, and DTO option construction. Then list group selection rules: folders and disabled grouping bypass containers, repeated container IDs merge while visited, and the loop stops as soon as enough groups exist.

List representative rules separately: first child by default, container for multiple collected children, and container for a singleton MusicAlbum. Record the count vector and the positive-only restoration rule. This inventory prevents an unrelated refactor from changing a subtle contract while tests focus only on the new maximum.

Finally record the mapper boundary: the selected real path with visibility checks skipped preserves input cardinality and index correspondence. Your test doubles must honor that contract for ordinary cases and violate it only in explicitly labeled robustness experiments. A fake mapper returning arbitrary order cannot be treated as a faithful implementation while interpreting positional count failures.

## Build an acceptance matrix before implementation

Include default, one, proposed maximum, one above proposed maximum, zero, and a value beyond the old arithmetic ceiling. Use a mocked action boundary for enormous numeric inputs so no real library allocation occurs. For accepted ordinary values, include a multi-child container, singleton nonalbum, singleton album, folder, and ungrouped item.

For every rejected row, assert the intended result and absence of later service work according to your chosen early-rejection contract. For accepted rows, assert the forwarded effective limit, subject user, played intent, parent, item types, and DTO option identity. Use distinct values and identities to make transpositions visible.

Test both the current action and legacy delegate for shared behavior. Hosted route binding and response serialization are additional implementation-route checks when the environment is available. A direct invocation of both methods does not establish their full HTTP equivalence, but it can protect their argument delegation and result behavior.

## Include a collected-count counterexample

Use candidates A1, B1, A2 with a limit of two and compare them with A1, A2, B1. The first collects one A child before stopping; the second collects two. Your expected representative and count results should reflect that distinction. The new operational cap must not accidentally change the grouping loop to scan all remaining candidates after the threshold.

Also include the limit-one versus limit-two example where a nonalbum representative can change from child A1 to container A. This protects against a test oracle that assumes stable response prefixes under larger limits. Your policy change should preserve current semantics unless the specification explicitly includes a separate representation redesign.

These examples are small enough to understand by hand and strong enough to catch plausible refactor mistakes. A large random media fixture without exact expected identities would provide less useful review evidence for this capstone's narrow contract.

## Require independent count-restoration assertions

Seed mapper DTOs with nonzero ChildCount values on positions whose recorded group count is zero. Verify those values survive. Verify positive group counts replace the mapper values at the corresponding positions. Include the singleton album, whose count one is positive even though its group contains only one child.

A test that initializes every DTO count to zero cannot detect an accidental zero overwrite. A test that checks only response length cannot detect a wrong representative. A test that compares IDs as an unordered set can miss positional count misassignment. Explain how your assertions avoid each weakness.

Use the extracted-source lab as calibration, not as the sole proof of the policy change. Its algorithm blocks exclude the action guard and framework result path. The implementation route needs focused action tests for the new rejection behavior and appropriate broader evidence for any public response-format claim.

## Plan implementation and review boundaries

The design-only route submits the specification, matrix, source inventory, mutation plan, and compatibility analysis. The implementation route additionally changes application code in the learner's own authorized workflow and records exact executed checks. This course authoring does neither application modification nor Git history work on the learner's behalf.

If full test assets are unavailable, report that limitation and retain the concrete test plan. Do not mark a proposed command as executed or treat an SDK-only extracted lab as a substitute for compiling the changed API project. A complete design packet remains useful; implementation completion requires evidence appropriate to the changed code.

For a later patch narrative, lead with the accepted and rejected request behavior, then describe why selection remains unchanged and what tests demonstrate that. Avoid listing every exploratory command. A reviewer should be able to locate the new policy, its compatibility effect, and the protected contracts quickly.

## Use semantic mutations to evaluate the suite

Consider four deliberate changes in an owned experimental copy: accepting one above the new maximum, moving the guard after user lookup, removing the singleton-album exception, and overwriting zero count positions. Each should fail a different assertion. The first tests the policy boundary; the second tests rejected-work behavior; the others protect existing selection semantics.

A compilation failure is not a killed semantic mutation. A missing test dependency is not proof that the guard works. Record successful build and the named assertion that fails. If the suite cannot distinguish one mutation, identify the missing input or weak oracle before adding unrelated tests.

Keep baseline and mutation receipts tied to the same source version. A passing baseline from yesterday and a mutation failure after unrelated source changes are weaker evidence than a paired experiment. Hashes or a known revision can make the relationship reviewable without exposing credentials or machine-specific secrets.

## Sixty-point capstone rubric

Award twelve points for a precise operational policy that distinguishes arithmetic safety, acceptance, and public response behavior. Award twelve for a complete preserved-contract inventory and compatibility matrix across both route shapes. Award twelve for independent representative, ordering, and count assertions with discriminating fixtures.

Award ten points for semantic mutation analysis and rejected-work evidence. Award eight for a realistic bounded performance or cost experiment plan with correctness controls. Award six for an honest review packet separating design, direct tests, extracted-source execution, full-project build, and hosted evidence. The maximum is sixty points; the chapter's three preparation exercises are separate practice items.

A submission cannot claim implementation completion if it only runs the extracted grouping lab, because that lab does not execute the new action guard. It also cannot claim unchanged behavior if it silently clamps limits, changes count meaning, or loses explicit played intent. Those are material contract changes requiring their own specification.

## Independent preparation exercises

Exercise JF-23A asks you to write the policy and baseline inventory, then identify the exact requests whose acceptance intentionally changes. Include defaults, both route shapes, and the service-work contract for rejected input.

Exercise JF-23B asks you to produce the five-shape representative fixture and the two candidate-order counterexamples. Give expected ordered IDs and count fields, and explain why zero-seeded DTOs or unordered ID assertions would be weak.

Exercise JF-23C asks you to assess a submission with passing extracted-source cases but no action-guard test. State what evidence is valid, what remains for implementation completion, and which mutation would expose the missing coverage. Read the separate review only after writing your decision.

## Review checkpoint

The capstone is complete as a design when another engineer could implement and test it without guessing the acceptance policy or preserved selection semantics. It is complete as an implementation only when the declared changed boundaries have corresponding executed evidence. The distinction should be visible in the first paragraph of the submission.


[Separate hints and full review](review-04-consistency-labs-properties-and-capstones.md) | [Complete course route](README.md)
