# 07. Group candidates and choose representatives

The view manager and controller both participate in grouping, but they do different jobs. [UserViewManager.GetLatestItems](../../../jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs) assembles groups from retrieved candidates. [GetLatestMedia](../../../jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs) chooses a representative item from each returned tuple. Separating these steps makes ordering, limits and child-count behavior easier to reason about.

## How the view manager assembles groups

For each candidate, the view manager uses no container when the item is a folder or grouping is disabled. Otherwise it reads LatestItemsIndexContainer. An item without a container becomes a new tuple with a null container and a one-item child list. A previously seen container receives another child in its existing group. A new container creates a new tuple and records its index by container ID.

The loop checks the number of groups after processing each candidate and stops when that count reaches the requested limit. This is not a full scan followed by a final Take over every possible group. Once the threshold is reached, later candidates are not processed by this loop. Consequently, the child lists represent candidates collected before the break, not necessarily every child of each container in the entire library.

Group order follows first appearance in the candidate sequence. Appending another child to an existing container does not move the group to the end. The dictionary locates an existing list index; output order is carried by the list. This distinction prevents an explanation that accidentally depends on dictionary enumeration.

## How the controller chooses a card

For each returned tuple, the controller initially selects the first child and assigns a child count of zero. If a nonnull container has more than one child, it selects that container and records the child-list count. It also selects a MusicAlbum container even when there is only one child. A nonalbum container with exactly one child leaves the child as the representative.

This policy creates useful edge cases. One episode in a series-like container can be represented by the child under this logic, while one track in a MusicAlbum is represented by the album. Two children with a nonnull container select that container. A null container leaves the first child selected regardless of the hypothetical number of children in an adversarial tuple.

The controller accesses the first child before evaluating the container condition. It therefore assumes each tuple has a nonempty child list. The inspected view-manager construction creates groups with an initial child, but a malformed mock can violate that assumption. Such a fixture probes a collaborator contract; it does not establish that the real service currently emits empty groups.

## Exercise JF-07A: trace candidate grouping

Use candidates A1, B1, A2, C1 where A1 and A2 share container A, B1 has container B and C1 has no container. With a group limit of three, record the list and container-index map after each candidate. Then reduce the limit to two and identify which later candidates are never processed.

Explain how the smaller limit can affect A's collected child count even though A appeared first. The loop stops once the second group is created, so a later A2 may not join A. This is a bounded-candidate grouping result, not a complete count of A's library children.

## Exercise JF-07B: build representative fixtures

Create tuples for null container plus one child, nonalbum container plus one child, nonalbum container plus two children and MusicAlbum plus one child. Predict selected item identity and saved child count for each. Use distinct IDs for container and child so the mapper input reveals the decision.

Add an empty child-list fixture as an explicit contract-violation probe. State the expected direct-call failure from the current indexing operation and explain why you would not include that fixture in a valid-output generator without first changing the collaborator contract.

## Exercise JF-07C: propose complete-count metadata

Suppose a client wants a container's total library child count rather than the collected latest-candidate count. Design a separate metadata field or query strategy. Explain how it differs from the current saved childCounts values and what additional service work might be required.

Do not relabel the current count as a total simply because it appears on a container DTO. A correct proposal defines the population being counted, handles visibility and filter context, and avoids mixing a complete total with a partial latest-candidate list. Include one fixture where those populations differ.

## Review standard

The final trace should separate candidate retrieval, group assembly and representative selection. It should show the early break, the album exception and the nonempty-child assumption. Strong answers name the population behind every count instead of treating all child counts as interchangeable.
