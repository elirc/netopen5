# 04. Resolve user identity and context

The latest-media action accepts an optional userId, but it does not blindly use that value. [RequestHelpers.GetUserId](../../../jellyfin/Jellyfin.Api/Helpers/RequestHelpers.cs) compares request intent with the authenticated principal. The resolved identifier is then used for user lookup, and the resulting User object supplies both preference context and the view query's user.

## Follow the helper's branches

The helper first reads the authenticated user identifier from the principal. If the requested userId is null or empty, it returns that authenticated identifier. If an explicit nonempty identifier differs from the authenticated one, the principal must have the administrator role; otherwise the helper throws a SecurityException. An explicit identifier equal to the authenticated one is allowed by this helper.

This establishes an application-level identity rule in the inspected helper. It does not independently validate how the principal was authenticated or how its claims were issued. The controller's authorization attribute and the hosting authentication configuration belong to that broader path. A direct test can construct arbitrary claims, so its evidence begins after that construction rather than proving real credential verification.

After resolution, the action asks IUserManager for the user. A null result leads to not found. An authenticated identifier and an existing user record are therefore distinct conditions. Do not replace the user lookup with an assumption that a principal's identifier necessarily corresponds to a current user record in every fixture or deployment state.

## Keep actor and subject concepts distinct

The authenticated principal is the actor making the request. The resolved User is the subject whose latest-media context is being requested. They usually coincide, but the helper permits an administrator to choose another user. That distinction matters for preferences: HidePlayedInLatest is read from the resolved User, not from a separate administrator profile that happens to be making the request.

The view query and DTO service receive the same resolved user object in the action. A focused test can verify that object association. It should use two clearly distinct users in an administrator scenario so accidental use of the actor becomes observable. If every test uses one user, a subject-context bug can remain hidden.

Do not log credentials or full principal contents to explain this trace. Synthetic identifiers and role labels are sufficient for a learning fixture. The important evidence is which identity was requested, which was authenticated, which was resolved and which User reached each collaborator.

## Exercise JF-04A: construct an identity matrix

Include omitted userId, Guid.Empty, the actor's own identifier, another user's identifier for a nonadministrator and another user's identifier for an administrator. For each case, predict the helper outcome and whether user lookup occurs. Add a row where the resolved identifier has no corresponding user record.

Separate helper-level failure from action-level not found. The first arises while deciding whose context may be accessed; the second arises after an allowed identifier is looked up. A table that labels both simply invalid user discards information needed for testing and client behavior.

## Exercise JF-04B: verify subject preferences

Design a direct fixture with an administrator actor and a different subject user whose HidePlayedInLatest preference is true. Omit isPlayed. Verify that the query uses the subject user and resolves the filter according to that subject's preference. Then supply isPlayed explicitly and predict how the preference interacts with it.

The existing focused tests do not cover every identity branch. Treat this as a proposed addition rather than a claim about their current coverage. Before implementing, inspect the repository's principal-extension conventions so that the role and user claims are constructed in the form the helper actually reads.

## Exercise JF-04C: review a shortcut

A proposed refactor uses userId ?? principalId directly and removes RequestHelpers. Explain which branch is lost, how Guid.Empty differs from null in the current helper and why an ordinary self-request test might still pass. Write the smallest fixture that exposes the changed access decision.

Then consider a different shortcut that uses the actor's User for DTO mapping even after resolving another subject. Identify the preference and visibility assumptions that could diverge. A correct identifier in one query field does not guarantee that every downstream collaborator receives the correct user context.

## Review standard

A strong answer distinguishes actor, requested identifier, resolved identifier and loaded User. It can trace administrator access without claiming that a fabricated unit-test principal proves production authentication. Its fixtures make context substitution observable through distinct users and preferences.
