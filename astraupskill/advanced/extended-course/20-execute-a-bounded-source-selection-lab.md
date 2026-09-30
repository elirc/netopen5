# 20. Execute a bounded source-selection lab

The [latest selection lab](labs/latest_selection_lab.py) compiles extracted statements from the real [UserViewManager](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs) and [UserLibraryController](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs). It supplies small explicit stand-ins for media types and retrieval, then exercises grouping, representative selection, and positive-only count restoration. This is stronger than a handwritten Python imitation of the algorithm and narrower than a full Jellyfin build or hosted request.

The chapter teaches how to interpret that middle evidence boundary accurately. The extraction executes real method logic, but its stand-ins do not establish library visibility, metadata loading, model binding, authentication, or serialization behavior. Those limits are part of the experiment's design rather than details to hide in a footnote.

## Identify exactly what is copied

The runner locates the public GetLatestItems method in UserViewManager by its unique signature and copies the balanced method block. A generated host provides GetItemsForLatestItems as a controlled candidate-list source. Therefore, the real grouping loop executes, while the real private candidate-retrieval method does not.

From GetLatestMedia, the runner extracts the representative-array construction and the later child-count restoration loop. Those statements retain the real container, MusicAlbum, and positive-count conditions. The generated wrapper exposes them as local functions that the harness can call. It does not execute the action's limit guard, identity helper, user lookup, option construction, or framework result path.

The stand-in BaseItem has only the properties needed by these statements: identity, folder flag, and latest-items container. MusicAlbum supplies the runtime type distinction. The DTO stand-in has identity and ChildCount. Keeping that surface small makes the dependency boundary visible, but it also means the lab cannot prove the behavior of the actual media classes' properties.

## Treat extraction as a reviewed fixture dependency

The extractor uses unique signature checks and brace balancing suitable for the inspected method blocks. It is a bounded source extractor, not a general C# parser. If those methods later gain braces in strings or comments that affect this simple scan, the extraction must be reviewed rather than trusted as a universal parsing tool. A changed signature or mutation expression causes an explicit stop.

The generated code retains the method statements without rewriting their comparisons into another language. That reduces one source of transcription error, but the harness still supplies its own environment. A passing result means the extracted statements behaved as asserted under that environment. It does not prove the surrounding application compiles with all current packages or that every dependency honors the same assumptions.

Read the generated boundary description before reporting the run. Phrases such as real-source algorithm lab or extracted grouping statements with stand-ins are accurate. Phrases such as full controller integration passed or live latest-media endpoint verified are not supported by this experiment.

## Predict the grouping cases

The harness covers empty candidates, grouping disabled, folder bypass, repeated container identities, first-container object retention, early threshold exit, and siblings encountered before or after that exit. Each case is chosen to distinguish a branch or ordering property rather than merely add more ordinary inputs.

Consider A1, B1, A2 with a group limit of two. The loop creates group A, then group B, reaches the threshold, and stops. A2 is not visited, so A's collected child count remains one. With A1, A2, B1, the second A child is added before the threshold is reached, so A contains two. The difference is candidate order relative to the break, not a complete-container count policy.

A limit of one stops after the first candidate creates the first group. It does not continue accumulating later siblings of that group. This case is particularly good at detecting a mutation that changes the break comparison. A large random fixture can miss the boundary if it never asserts the collected membership precisely.

Two different container objects with the same Guid are grouped through the dictionary key. The first container object remains the representative container stored in that tuple. This tests identity-key grouping separately from object-reference equality. The stand-in objects are deliberately distinct so the assertion can tell those strategies apart.

## Predict representative selection and restoration

The representative fixture contains a multi-child nonalbum group, a singleton nonalbum group, a singleton album, and a null-container group. The expected selected identities are the first container, the singleton child, the album, and the ungrouped child. The corresponding recorded count vector is two, zero, one, zero.

The mapper is not executed. Instead, the harness constructs DTO stand-ins in the selected order and seeds every ChildCount with ninety-nine. Running the real restoration statements should change only the positive positions to two and one, preserving ninety-nine at the zero positions. This seed is intentional: starting every count at zero would not reveal an accidental overwrite with zero.

An empty group list produces empty representative arrays. A group with an empty child list violates the controller's assumed input shape and reaches the first-child access failure. That case characterizes the extracted boundary's assumption; it does not claim the real view manager emits empty groups. A robust test distinguishes invalid collaborator output from valid application behavior.

## Run the baseline from the project root

Use Python and the already installed .NET 10 SDK. The runner creates a uniquely owned temporary directory, writes an SDK-only project with no third-party package references, clears package sources, restores only the generated project's assets, builds it, and runs its executable. It does not restore Jellyfin's projects or install packages.

```powershell
python -B astraupskill/advanced/extended-course/labs/latest_selection_lab.py
```

The expected baseline reports twenty-two extracted-source algorithm assertions. The output must show a successful build before the semantic success line. It also reports unchanged hashes for the two original source files. Those hashes cover the selected files during that invocation, not every file in the repository or preexisting learner changes.

The temporary project targets .NET 10 independently of Jellyfin's own build configuration. This is a deliberate bounded execution choice. Full-project assets or test prerequisites may still be unavailable even when this lab passes. Keep the lab result separate from the existing focused test suite, which the earlier authoring pass reviewed but did not execute.

## Use three semantic mutations

The early-break mutation changes greater-than-or-equal to strictly greater. The album mutation removes the singleton-album exception from representative selection. The restoration mutation changes positive-only overwrite to include zero. All are signature-compatible changes to generated source only; original application files remain untouched.

```powershell
python -B astraupskill/advanced/extended-course/labs/latest_selection_lab.py --mode broken-early-break
python -B astraupskill/advanced/extended-course/labs/latest_selection_lab.py --mode broken-album
python -B astraupskill/advanced/extended-course/labs/latest_selection_lab.py --mode broken-zero-restore
```

Predict the first failing assertion before execution. The break mutation allows a later sibling to be collected after the threshold in the discriminating fixture. The album mutation changes the selected identity sequence. The restoration mutation destroys the seeded mapper value at a zero-count position. A nonzero process exit counts as intended evidence only when compilation succeeded and the expected semantic assertion failed.

If the source signature or exact mutation expression changes, review the extraction and oracle. Do not broaden a string replacement until it happens to match somewhere. The experiment's safety and meaning depend on knowing which statements were copied and which single expression was changed.

## Interpret a surviving or unexpected mutation

A surviving mutation can mean the cases do not distinguish the changed behavior, the mutation is equivalent for those inputs, or the stated contract is wrong. Investigate those possibilities before adding random assertions. An unexpected earlier failure can mean a fixture violates the nonempty-child contract or an extraction dependency changed.

Preserve the original prediction and the observed assertion label. If the baseline fails, do not proceed to interpret mutation failures as successful detection. A failing environment can make every mode red without executing any meaningful case. The runner separates build failure from semantic exit specifically to prevent that misinterpretation.

A useful extension might test a different grouping identity or a changed candidate order. Keep expected values independent from the source expression. For example, write the expected representative IDs explicitly rather than deriving them by calling the same selection wrapper twice. Two identical wrong executions do not form an oracle.

## Independent exercises

Exercise JF-20A asks you to draw the extracted and stubbed boundaries. Identify three current endpoint behaviors the lab cannot prove and three algorithmic contracts it does execute. Explain why real source extraction is stronger than a prose-only prediction but weaker than a hosted request.

Exercise JF-20B asks you to predict baseline identities, count vectors, and the three mutation failure labels before running. Explain why seeded nonzero DTO counts and different container objects sharing an identity make the assertions discriminating.

Exercise JF-20C asks you to propose one additional semantic mutation and its independent fixture. State how you would detect extraction drift, distinguish compilation failure from semantic failure, and preserve original source. Consult the lab evidence guide and final review only after completing your prediction sheet.

## Review checkpoint

The chapter is complete when you can reproduce the bounded result and describe its exact scope in one paragraph. You should be able to explain every stand-in, every preserved source file, and why a green lab is useful without presenting it as a full Jellyfin server verification.


[Separate hints and full review](review-04-consistency-labs-properties-and-capstones.md) | [Complete course route](README.md)


Use the [detailed evidence guide](lab-evidence-selection-and-mutations.md) to record extraction, compilation, semantic behavior, and preservation as four separate outcomes. Keep your original prediction sheet alongside the receipt so a later reviewer can see why the observed result changed or confirmed your model.
