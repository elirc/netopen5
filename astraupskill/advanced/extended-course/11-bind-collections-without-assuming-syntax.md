# 11. Bind collections without assuming syntax

The latest-media action marks fields, includeItemTypes and enableImageTypes with [CommaDelimitedCollectionModelBinder](../../../jellyfin/Jellyfin.Api/ModelBinders/CommaDelimitedCollectionModelBinder.cs). Those attributes connect HTTP query text to typed arrays before the action runs. Direct controller fixtures supply arrays themselves and therefore bypass this behavior entirely.

## Read the two input paths

The binder asks the value provider for the parameter's values. If there is more than one supplied value, it passes that list directly to its conversion helper. Otherwise it takes the first value, splits a nonnull string on commas with empty entries removed, and converts the resulting pieces. If no value is present, it returns an empty array of the requested element type.

Repeated parameters and one comma-separated parameter therefore take different preprocessing branches. A repeated value containing its own comma is passed as one conversion input in the multi-value branch; it is not explicitly split again by this binder. The eventual converter may have its own behavior for that text, especially for enums, so do not invent a universal result without examining or testing the relevant element type.

The conversion helper trims each string and calls the type converter. It catches FormatException, logs a debug conversion error and omits unsuccessful entries from the resulting typed array. It does not catch every possible exception type. A statement that every malformed value is always ignored would exceed what the catch clause establishes.

## Existing tests provide useful examples

The [binder tests](../../../jellyfin/tests/Jellyfin.Api.Tests/ModelBinders/CommaDelimitedCollectionModelBinderTests.cs) cover comma-separated strings, integers and enums, double commas, repeated enum values, an empty query and examples in which invalid enum text is omitted. They construct a binding context and query value provider directly. This verifies the binder in that environment, not the whole hosted endpoint.

An empty bound includeItemTypes array has downstream meaning: the view manager can infer types or media categories from parents. An invalid-only input that becomes empty through conversion can therefore resemble omission at later stages. Whether that is desirable is a contract question. Do not assume that silently omitted invalid tokens necessarily cause the request to fail.

The fields and image-type arrays have different downstream rules even though they share a binder. Fields replaces the DTO option field list; an empty image-type array leaves existing image types in the extension. Input syntax is shared, but semantic interpretation belongs to each consumer. A good source trace follows both stages.

## Exercise JF-11A: make a syntax matrix

List omitted parameter, one ordinary value, one comma-separated value, repeated values, double commas, whitespace around values and a mixed valid/invalid enum input. Identify which binder branch processes each representation. Record the exact element type because converter behavior can differ by type.

For cases already covered by existing tests, cite the test. For a repeated value containing a comma, write a prediction and mark the converter behavior as requiring investigation. Do not label two syntaxes equivalent merely because both can express two simple values in the common case.

## Exercise JF-11B: trace an empty result downstream

Compare an omitted includeItemTypes parameter with an invalid-only input whose conversion produces an empty array in a controlled fixture. Follow that empty array into the view manager's parent-based inference. Then compare an empty fields array and an empty image-type array at DTO option construction.

Write a client-facing proposal for invalid-token handling if you believe the current behavior should change. Specify whether mixed inputs fail entirely or retain valid entries, how errors identify the parameter and what compatibility impact existing clients might experience. This is a design proposal, not a modification made by the course.

## Exercise JF-11C: choose test layers

Design one binder-unit case for preprocessing, one controller case for typed-array forwarding and one hosted case for actual query syntax. Explain which failure each catches that the others cannot. Keep the hosted retrieval fixture empty so the test focuses on binding rather than library scale.

A strong test report records the raw query representation and resulting typed array. Logging only the final response can hide whether a surprising result came from binding, downstream inference or grouping. Preserve those intermediate observations in synthetic test artifacts.

## Review standard

A complete answer follows the single-value and multi-value branches separately, respects the narrow caught exception type and distinguishes parsing from semantic defaults. It can explain why sharing a binder does not make three array parameters behave identically after binding.
