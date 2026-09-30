# 12. Trace parent and library query branches

The controller turns an omitted parentId into Guid.Empty. The downstream [UserViewManager](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs) interprets that request context through several branches. Reading only the final InternalItemsQuery initializer misses channel handling, parent fallback, type inference and specialized grouped retrieval.

## Resolve the parent path first

For a nonempty parent identifier, the service looks up the parent item. A Channel uses a channel-specific latest-items query and returns from that branch. A Folder is added to the parents list. If no parents have been selected, the ordinary path falls back to the user's root children, keeps folders and excludes IDs in the user's latest-item exclusion preferences. If the resulting parents list remains empty, it returns no candidates.

This means an explicit parent that does not become a recognized Folder or Channel can lead to fallback rather than a direct not-found response in this method. Do not generalize from the controller's missing-user handling to a missing-parent guarantee. They are different inputs processed at different layers with different behavior.

The service's channel query includes the requested played state, start index, limit and included item types, with total-record counting disabled. The ordinary latest-media controller does not set StartIndex on LatestItemsQuery, even though that model has the property. A property existing in a shared query type does not make it a parameter of every endpoint that uses the type.

## Infer types only under the specified conditions

When included item types are empty, the service can infer Movie or Episode from selected UserView collection types when all relevant views match the corresponding category. If types remain empty, it derives media types from collection folders, including category-specific combinations. It then chooses a default excluded-item-type set only when both included types and derived media types are empty.

These branches make an empty includeItemTypes array semantically active: it invites inference rather than necessarily meaning every possible item type. An explicit nonempty array bypasses some of that inference. A forwarding test at the controller boundary can show which array was supplied but cannot establish the final internal query without exercising or inspecting the service.

The ordinary query orders by DateCreated descending, then SortName descending, then ProductionYear descending. It excludes virtual items and initially uses the doubled limit. Avoid describing latest as purely newest timestamp with no tie behavior when the query explicitly contains additional order fields. At the same time, do not claim a unique total ordering unless ties across all those fields are resolved elsewhere.

## Specialized grouping changes retrieval

When grouping is enabled, the service examines collection type and can call GetLatestItemList for television, music or movies with query.Limit reset to the original limit. Otherwise it calls GetItemList using the ordinary query. Candidate retrieval and the later group-assembly loop are distinct stages; both can influence the final number and shape of returned groups.

Do not say that the service always fetches exactly twice limit. Query limits are upper-bound requests to collaborators, and several branches use different values or methods. The number returned can be smaller because of available data, filters or collaborator behavior. Precise language should identify the assigned limit and selected retrieval method.

## Exercise JF-12A: draw a parent decision tree

Include empty parent, Channel, Folder, an unrecognized or missing parent result, fallback roots with exclusions and no remaining parents. For each leaf, identify the retrieval method or early empty return. Record which user preferences participate.

Use synthetic parent IDs and small lists. The objective is to understand branch authority, not recreate a complete library. Mark which observations come from source and which would need a real library-manager fixture to execute.

## Exercise JF-12B: construct final-query examples

Create examples for explicit included types, empty types with movie UserViews, empty types with collection-folder media inference and the default excluded-type branch. Record order fields, virtual-item policy, played state and limit at the chosen retrieval call.

Add a grouped movie case that replaces the initial doubled limit. Explain why this does not invalidate the arithmetic guard: the initializer still evaluates before the replacement on that path. Keep expression evaluation separate from the final property value seen by the collaborator.

## Exercise JF-12C: design a parent-validation proposal

Suppose a product requirement says an explicitly missing parent must return a clear error instead of falling back. Identify the service and API contract changes needed, how channel behavior should remain distinct and which clients could observe the difference.

Do not implement the proposal in the original application as part of this reading exercise. Supply a before-and-after behavior table, regression cases and an unresolved compatibility question. A precise proposal is useful even when the current behavior is intentionally retained.

## Review standard

A strong answer follows early returns, inference and specialized retrieval without flattening them into one query. It distinguishes properties on a shared request model from parameters exposed by this endpoint and names the actual ordering and limit assignment at each branch.
