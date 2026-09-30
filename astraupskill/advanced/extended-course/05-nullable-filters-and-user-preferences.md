# 05. Nullable filters and user preferences

The isPlayed parameter has three states: true, false and absent. That third state is meaningful. In [GetLatestMedia](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), a user preference is consulted only when isPlayed has no value. If HidePlayedInLatest is true, the action replaces the absent filter with false. Otherwise it leaves the filter absent.

## Build a truth table before writing shorthand

For an explicit true request, the query receives true regardless of the preference. For explicit false, it receives false regardless of the preference. For an absent request and a true HidePlayedInLatest preference, it receives false. For an absent request and a false preference, it receives null. The last case is not equivalent to false: it represents no played-state filter at this controller boundary.

A common incorrect simplification turns every absent value into false. Another combines the preference with the request using boolean operators that cannot preserve the three-state distinction. Derive the table before proposing a compact expression. Readability is valuable, but a shorter condition is not an improvement if it changes the meaning of omission.

Explicit request intent takes precedence over the preference in this action. The preference supplies a default, not a restriction that forces every request to hide played items. This is a useful pattern for many settings: a stored preference can fill an omitted option while an explicit per-request choice remains authoritative. The exact policy must be read from each application rather than assumed universally.

## Follow the value beyond the controller

The controller writes the resolved nullable value into LatestItemsQuery. The downstream [UserViewManager](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs) can further adjust query behavior. In the inspected ordinary path, a parent collection recognized as music sets the local isPlayed variable to null. A channel path forwards the request value through a different internal query. Therefore controller forwarding is not identical to a universal final database-filter guarantee.

This is a valuable source-reading lesson. A unit test can prove that the controller sends false, while the real service deliberately transforms that value for a particular library category. Neither observation contradicts the other. They describe different boundaries. Reports should say controller-resolved filter or final internal query filter as appropriate.

The action also defaults groupItems to true and limit to twenty through optional parameters. Those defaults are separate from the nullable played preference. Do not collapse all defaults into one configuration source. Some are method defaults, some are loaded-user preferences and some are DTO option defaults applied by an extension method.

## Exercise JF-05A: test all six preference combinations

Combine the three isPlayed states with both preference values. Predict the exact nullable field sent to the view manager. Use assertions that distinguish null from false. An assertion such as not true would allow both and miss the most important boundary.

Give the fixture a valid small limit and an empty view result so that grouping and large-library concerns do not distract from the filter rule. Configure the DTO mapper to return an empty collection. The fixture should fail if the controller substitutes false for null when the preference is disabled.

## Exercise JF-05B: design a layered trace

Choose an omitted isPlayed request for a user who hides played items. First record the controller query value. Then inspect the ordinary downstream path for a music parent and record its local filter value. Explain why a controller mock test cannot establish the latter transformation.

Add a channel-parent trace and identify where it exits into a different service. Do not assume that every parent category shares the same query construction. Your diagram should show the branch that changes the value and the branch that forwards it directly, using source links for each.

## Exercise JF-05C: evaluate a client control

Design a three-choice client control: use my preference, played only and unplayed only. Specify the query representation for each choice and explain how the first differs from explicitly requesting unplayed items. Do not implement the client in this course; provide a contract and a small request table.

Consider how the client should describe library-category behavior if the server deliberately adjusts a filter downstream. Avoid promising exact semantics from a label unless the endpoint contract supports them. A useful proposal identifies the question for product design and integration testing rather than hiding it in UI wording.

## Review standard

A complete answer preserves all three nullable states and explains preference precedence. It also traces the boundary between controller intent and service-specific transformation, so a passing forwarding test is not mistaken for proof of every library query's final filter.
