# 01. Follow the latest-media request

The latest-media endpoint is a useful entry into a large application because its action combines arithmetic, identity, preferences, query construction and response mapping in one readable path. Start at [UserLibraryController](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs), specifically GetLatestMedia. Do not begin by reading the whole controller from top to bottom. Locate this behavior, list its direct collaborators and follow only the values needed to explain its result.

## Draw the execution stages

The action validates limit before resolving the requested user. It obtains a user identifier through RequestHelpers, looks up the user, applies a preference only when isPlayed was omitted, constructs DTO options and creates a LatestItemsQuery. The view manager returns tuples containing a possible container and a list of child items. The action chooses one representative per tuple, maps representatives to DTOs, restores selected child counts and returns a successful result.

This sequence contains more contracts than a description such as fetch recent items suggests. The limit guard controls whether downstream work begins. User resolution controls whose preferences and library context apply. Query construction transfers request intent. Tuple resolution decides whether a child or its container is displayed. DTO mapping transforms those selected items into the public response. Each stage can fail independently or be tested at a different boundary.

The early paths are equally important. An invalid limit returns a bad-request result before user lookup, view access or DTO mapping. A valid limit followed by a missing user returns not found before the view manager is called. An empty view result still reaches DTO mapping with an empty array. Record those branches instead of drawing one uninterrupted happy path.

## Identify the actual dependencies

Read [IUserViewManager](../../../jellyfin/MediaBrowser.Controller/Library/IUserViewManager.cs) and its [UserViewManager implementation](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs). The controller delegates latest-item retrieval and grouping to that service. It does not perform the underlying library query itself. A mock-based controller test can establish the query passed to the service, but it cannot establish how the real service selects database rows or groups a full library.

The result mapping uses IDtoService with skipVisibilityCheck set to true. The nearby comment explains that visibility has already been handled in GetLatestItems. Treat that as a trust relationship to investigate, not as an independent proof that every possible view-manager implementation enforces visibility correctly. A future refactor that bypasses the view manager must review this relationship before reusing the mapping call.

Follow actual overloads and named arguments. A service may expose several DTO helpers, and nearby actions in the same controller may use different options. Copying behavior from GetItem or GetRootFolder into your explanation of GetLatestMedia can introduce errors even though the method names look related. A source map should name the precise method and the value it receives.

## Distinguish method calls from HTTP requests

The controller is authorized and inherits an ApiController base. Those attributes matter in a hosted request pipeline. Calling GetLatestMedia directly from a unit test does not execute routing, authentication middleware or model binding. The supplied ClaimsPrincipal and argument values are test inputs constructed in memory. The result object is also observed before real response serialization.

This does not make direct tests weak. They are well suited to arithmetic boundaries, forwarding and call ordering. Their strength comes from isolating those concerns. A hosted test is needed for claims about an unauthenticated request, malformed query text, route selection or serialized error shape. Write the evidence level next to the behavior instead of treating one kind of test as a substitute for every other kind.

## Exercise JF-01A: construct a source map

Draw the guard, identity helper, user lookup, preference resolution, options construction, view query, representative selection, DTO mapping and response. Annotate each arrow with the actual value passed: integer limit, resolved Guid, User, nullable played filter, DtoOptions, LatestItemsQuery, tuple list, BaseItem array and DTO sequence. Add the invalid-limit and missing-user branches.

For each stage, identify one question that source inspection answers and one that requires execution or broader investigation. For example, the action shows that the same user object is supplied to the query and mapper, while a direct mock test does not establish what rows that user can access in a real library. Keep those statements separate.

## Exercise JF-01B: predict an empty result

Use a valid limit, an existing user and an empty tuple list from the view manager. Predict the sizes of resolvedItems and childCounts, whether the selection loop runs, whether DTO mapping is called and what kind of successful result is returned. Give the mapper an empty DTO result explicitly in the fixture.

Then change only the user lookup to return null. Explain which earlier setup becomes unused and why the result is different from a successful empty library. A client should not have to infer user existence from an empty item collection when the action already has a distinct missing-user path.

## Exercise JF-01C: write an evidence ledger

Choose five claims from your map. Label each as source inspection, existing focused test, proposed direct test or proposed HTTP test. Link the exact source or test file supporting the first two labels. Do not mark an exercise as executed merely because its expected result is obvious from reading the code.

The completed ledger should let another learner tell what has been observed and what remains a plan. Review it before using words such as verified, guaranteed or always. Those words are useful only when their scope matches the evidence.

## Review standard

A strong submission separates retrieval, grouping and mapping, preserves early-return order and identifies the actual trust boundary around visibility. It also explains why the endpoint's name is not a complete contract: latest, limit, user and group each acquire meaning through a specific stage in the source.
