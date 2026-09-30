# 06. DTO options and requested cost

Selecting media identities is only part of producing a response. DTO options control which associated information the mapper populates. The latest-media action constructs [DtoOptions](../../../jellyfin/MediaBrowser.Controller/Dto/DtoOptions.cs), assigns Fields from the request, applies [AddAdditionalDtoOptions](../../../jellyfin/Jellyfin.Api/Extensions/DtoExtensions.cs) and sets PreferEpisodeParentPoster to true. Follow those assignments in order before describing defaults.

## Defaults can be overwritten immediately

The DtoOptions constructor enables images and user data, sets the image-type limit to int.MaxValue, enables current-program information and initializes fields and image types. The action then explicitly replaces Fields with the fields argument. It would be incorrect to say that this endpoint necessarily uses every constructor-default field simply because it creates a new DtoOptions without passing false to the constructor.

The extension sets EnableImages to the supplied nullable value or true when omitted. It updates ImageTypeLimit only when a value was supplied and EnableUserData only when supplied. It replaces ImageTypes only when the provided list is nonempty. These are different omission rules. An empty image-type list retains the option object's existing image types rather than necessarily requesting no images.

The action finally enables PreferEpisodeParentPoster. That option's documented purpose is to prefer a season or series poster for episode cards. A controller test can check the flag passed to its collaborators. It cannot prove the actual selected image in a serialized DTO without exercising the relevant mapping behavior and fixtures.

## Options can affect work as well as shape

In the inspected [DtoService](../../../jellyfin/Emby.Server.Implementations/Dto/DtoService.cs), user-data options and requested fields influence batch retrieval work. For example, enabled user data can trigger batch user-data lookups, and requested child-count fields can trigger folder count retrieval. A response option is therefore not merely a final serialization switch; it can alter work performed during mapping.

This does not mean every requested field causes one query or that the endpoint's total cost is simply item count multiplied by field count. The service batches some work, branches on item types and invokes further helpers. A performance investigation should measure actual operations with representative options instead of assigning an invented uniform price to each field.

The arithmetic limit guard says nothing about these option costs. A small item count with expensive associated information can behave differently from the same count with minimal fields. A practical request-budget proposal should consider both selection size and mapping options while preserving the current contract until a change is deliberately approved for implementation.

## Exercise JF-06A: derive an option table

Create cases for omitted and explicit enableImages, omitted and explicit enableUserData, absent and supplied imageTypeLimit, empty and nonempty enableImageTypes, and an empty fields array. Predict the exact resulting DtoOptions properties after constructor, initializer, extension and final poster assignment.

Keep each stage visible in the table. This prevents a constructor default from obscuring a later overwrite. Include a case where images are disabled but a nonempty image-type list is supplied; explain how GetImageLimit uses both EnableImages and membership when deciding its return value.

## Exercise JF-06B: verify shared option identity

Design a controller fixture that captures the DtoOptions passed to the view manager and the mapper. Determine from the action whether the same object is used. Inspect its fields and flags in a callback or recorded argument. Use distinct nondefault values so missing forwarding is observable.

The existing focused suite broadly matches DTO options and therefore does not verify every option property. Your proposed case should state which gap it closes. Avoid copying the production option-construction expression into the expected-value helper; write expected properties directly from the contract table.

## Exercise JF-06C: plan a mapping-cost experiment

Choose a small synthetic set containing a folder and an ordinary media item. Compare minimal fields with requested child counts and user data. Identify which real service dependencies need controlled fixtures to count work. Record item count, selected options, observed batch calls and elapsed time separately.

Do not claim that a mock counting one call measures database latency. A call-count test can establish batching or option-dependent invocation; a timed integration experiment measures a different layer. A complete plan assigns each question to the cheapest environment that can answer it honestly.

## Review standard

A strong answer traces option precedence, recognizes that empty arrays and absent nullable values have different meanings, and links response shape to actual mapping work. It distinguishes checking a controller flag from verifying the image or field ultimately emitted by the real DTO service.
