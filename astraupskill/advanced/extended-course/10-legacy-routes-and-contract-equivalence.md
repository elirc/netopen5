# 10. Legacy routes and contract equivalence

The application retains a legacy latest-media route, Users/{userId}/Items/Latest, alongside Items/Latest. The legacy method is marked obsolete and hidden from API exploration, but it remains implemented. Its body delegates every parameter to GetLatestMedia. Compatibility is therefore expressed through shared action logic rather than a second copied implementation.

## Shared logic does not erase route differences

The primary action accepts an optional userId from the query. The legacy action receives a required userId from the route. Those are different binding surfaces even when they ultimately call the same method. A direct legacy-method test proves delegation for the supplied arguments; it does not prove that every URL binds as intended or that generated documentation displays both routes.

The legacy method carries the same default limit of twenty and grouping default of true. It forwards parent, fields, included item types, played filter, image options, user-data option, limit and grouping. A forwarding omission could preserve simple invalid-limit behavior while losing a nondefault option on successful calls. Compatibility tests should include representative nondefault values, not only one rejection case.

Obsolete is a development signal, not proof that an endpoint has been removed. IgnoreApi affects API exploration visibility, not necessarily route availability. Read the attributes according to their role and verify hosted route behavior when that is the claim. Documentation metadata and runtime execution are related but distinct evidence.

## Define equivalence carefully

For the same resolved inputs and principal, the two method paths should reach the shared implementation with equivalent arguments. That is a useful direct-call contract. It does not mean their URL syntax, required parameters or documentation entries are identical. A compatibility note should state the shared behavior and the differences clients must still observe.

Error equivalence also has layers. An invalid integer value passed directly to either method reaches the same limit guard. Malformed route identifiers and malformed query text involve different binding paths before the action logic. A hosted test matrix should cover those separately instead of assuming delegation proves all input errors equivalent.

When changing the primary action's signature, review the legacy forwarding call immediately. Positional parameters are especially easy to misalign when several adjacent options share types. Distinct test values and named arguments in new internal code can improve reviewability, but any style change should preserve the actual public binding contract.

## Exercise JF-10A: construct a forwarding checklist

List every parameter in both signatures and the expression supplied by the legacy call. Record binding source, nullability and default. Highlight where the primary optional query identifier becomes a required route identifier in the legacy surface.

Choose nondefault values for played, grouping, image visibility, user data and image limit. Explain which captured collaborator argument or DTO option would reveal a forwarding mistake for each. A single final empty response cannot establish that all options survived delegation.

## Exercise JF-10B: design paired direct tests

Run or specify the primary and legacy methods with equivalent synthetic inputs and separately constructed mocks. Compare the captured LatestItemsQuery, DtoOptions and final result. Use independent fixtures so one call's mock history does not accidentally satisfy another call's verification.

Include invalid limit, missing user and one nonempty group case. Keep the obsolete-warning suppression limited to the legacy call. State that these tests verify method equivalence after arguments have been supplied, not HTTP route binding.

## Exercise JF-10C: propose a migration note

Write a client migration note that replaces the route user identifier with the primary endpoint's query parameter while preserving selected filters and defaults. Explain how omission differs from explicitly supplying a user and how administrator subject selection remains governed by the shared helper.

Do not invent a removal date or claim current deprecation policy beyond the source attributes. A useful migration note can explain the mechanical request change and verification steps without making unsupported promises about release schedules. Include a small before-and-after request shape using synthetic identifiers.

## Review standard

A strong answer treats compatibility as a measurable relation between two surfaces. It verifies forwarding, preserves meaningful defaults and separates shared action behavior from differences in routing, binding and API discovery. It can explain why one passing legacy guard test is valuable but not exhaustive.
