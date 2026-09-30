# Lab evidence: selection and semantic mutations

This guide turns the [extracted-source runner](labs/latest_selection_lab.py) into a reviewable evidence packet. It complements [chapter 20](20-execute-a-bounded-source-selection-lab.md) with a concrete receipt format, a case inventory, and interpretation exercises. It is instructional material, not a claim that the full server suite was executed.

## What the delivered run established

The baseline built successfully with zero warnings and errors and passed twenty-two assertions. Three mutated generated programs also built successfully and exited with semantic failures at the predicted assertions. The early-break mode failed at later sibling excluded after threshold; the album mode failed at representative identities; the zero-restoration mode failed at zero leaves mapper value. Both original source-file hashes were unchanged after every invocation.

These results establish that the extracted statements distinguish the selected fixtures under the generated stand-in environment. They also establish that the assertion suite can detect three plausible semantic changes. They do not establish the private candidate query, real media-property behavior, user authorization, DTO service batches, model binding, result serialization, middleware registration, or hosted performance.

A useful one-sentence receipt is: the SDK-only extracted grouping and selection lab passed twenty-two assertions, and three deliberate generated-source mutations failed at named semantic assertions after successful compilation. Add the preservation scope and exact command when sharing it. Avoid shortening the sentence to Jellyfin integration passed, which changes its meaning.

## Case inventory by purpose

The empty-candidate case checks zero groups. Two ungrouped assertions check one group per candidate and null container positions. The folder case checks that a folder bypasses its supplied container. Three container-identity assertions check merging by Guid, accumulated child count, and retention of the first container object.

Two early-threshold assertions check group count and exclusion of a later sibling. Two limit-one assertions check that the first group stops the loop immediately and therefore contains only the first visited child. Another assertion checks that a sibling encountered before the threshold is included. Null-container candidates remain separate groups.

The representative fixture checks the ordered identity vector and recorded count vector across four shapes. The restoration fixture checks that identities are unchanged, a multi-child count is restored, a zero position preserves its seed, a singleton album count is restored, and a null-container position preserves its seed. The final two cases check empty selection and the expected failure for an invalid empty child list.

This grouping of assertions is more informative than a bare count of twenty-two. It lets a reviewer see which assumptions are exercised and which remain outside the harness. The empty-child case, for example, characterizes an invalid collaborator shape; it does not prove the real provider produces that shape or that the endpoint should accept it.

## Prepare an independent prediction sheet

Before running, write candidate labels in order and draw the group list after each visited item. Mark the exact iteration where the threshold becomes true. Stop the hand trace there; do not add later siblings because you know their container matches. That discipline catches the common mistake of treating collected children as a complete-container total.

Next write the representative identity for each group without consulting the generated harness. A singleton nonalbum uses its child; a singleton album uses its container. Then write the count vector and the seeded mapper values. Apply positive-only restoration by hand and retain the zero-position seeds. These independent values are the oracle for interpreting the output.

For each mutation, predict the first assertion that should fail, not merely that some test will be red. The named assertion tells you whether the experiment reached the intended distinction. A different earlier failure can mean the extraction, fixture, or source assumptions changed. Preserve that discrepancy for investigation rather than immediately changing the expected label.

## Record four separate outcomes

The first outcome is extraction: the unique method signature and exact mutation expression matched the reviewed source. The second is build: the generated C# project restored SDK assets and compiled. The third is semantics: the baseline passed or the intended mutation reached its named failing assertion. The fourth is preservation: the two selected original hashes still match.

A failure in one stage does not imply success in another. A missing SDK can prevent all semantic execution. A compiler error can make a mutated run nonzero without testing the assertion. A semantic failure can occur while preservation still succeeds. A preservation mismatch is a separate issue even if the baseline assertions pass.

Keep the receipt short but complete. Include working directory, mode, build result, semantic result, and hash result. Do not paste the entire generated program into every receipt; link to the runner and source anchors instead. The report's file manifest identifies the delivered artifact version for later review.

## Work through two misleading reports

Report one says the mutation was caught because dotnet returned an error. Ask whether the output shows compilation success and the expected assertion label. If it instead shows a missing type or malformed extracted block, the mutation was not evaluated semantically. The next action is to repair the experiment after source review, not to celebrate a killed mutation.

Report two says all latest-media behaviors are covered because the baseline is green. Ask where the limit guard, identity helper, private retrieval, and real mapper are executed. They are outside this harness. The next useful checks depend on the claim: direct controller tests for guard and forwarding, real collaborator tests for retrieval and mapping, and hosted requests for binding and public response behavior.

Neither correction makes the lab unhelpful. Its value is precise execution of selected statements with controlled inputs and a small dependency surface. Evidence becomes stronger when its limits are explicit because reviewers can combine it with other layers without double-counting the same assertion as several kinds of proof.

## Extend the lab responsibly

A learner can propose a new case for repeated child candidates, a different threshold order, or a container-identity substitution. First state whether the case is valid provider output or a contract violation. Then write the independent expected groups and representatives. Add only the stand-in properties needed by the extracted statements; do not turn the harness into an undocumented reimplementation of Jellyfin.

If source evolves beyond the simple brace extractor's reviewed assumptions, replace the extraction strategy deliberately or stop using the lab until it is updated. Broadening string matches to make a run pass can silently copy the wrong method. The current tool is intentionally bounded to known blocks, not a general compiler front end.

Original source should remain read-only during these experiments. Mutations belong in generated temporary code, and cleanup should remain restricted to the uniquely owned directory. The runner does not perform repository cleanup, dependency installation, commits, or pushes. Its preservation receipt covers selected originals during the run rather than certifying every preexisting workspace file.

## Final evidence exercise

Write two versions of your result: one sentence for a reviewer and one detailed table for a learner reproducing it. Both should agree on the execution boundary and outcomes. Then list one additional test that would add a genuinely new layer of evidence, rather than rerunning the same extracted assertions under a different label.

A strong answer can explain why the album mutation changes representative identity, why the break mutation changes collected membership, and why the zero mutation destroys a mapper-supplied value. It can also say clearly that no real library query or HTTP request ran. That combination of concrete behavior and honest scope is the standard for the course's final assessment.
