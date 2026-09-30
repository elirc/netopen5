# 16. Classify errors across the request pipeline

An endpoint can reject a request through a returned result, a thrown exception, model binding or middleware. The latest-media limit guard returns a BadRequestObjectResult with a message. Missing user returns NotFound. RequestHelpers can throw a security exception for a disallowed subject. These are different mechanisms even when a client eventually sees a non-success status.

## Returned results and exceptions are different paths

The guard constructs a result directly. It does not throw an ArgumentException. Therefore an exception middleware rule for ArgumentException does not explain how that particular bad-request result is created. The action's successful and missing-user returns also proceed through result execution rather than exception translation.

The local [ExceptionMiddleware](../../../jellyfin/Jellyfin.Api/Middleware/ExceptionMiddleware.cs) catches exceptions from the next request delegate when the response has not started. It unwraps aggregate exceptions, maps selected exception types to statuses and writes a plain-text error response. SecurityException maps to forbidden in that middleware's status selection. These are source facts about the middleware; a hosted test is still needed to establish its registration and behavior for a particular request path.

If the response has already started, the middleware logs a warning and rethrows instead of attempting its ordinary replacement response. That branch matters for streaming or late failures. Do not assume every exception can be converted into a clean new status after bytes have already been sent.

## Environment changes diagnostic output

In a development environment, the middleware writes a normalized exception message. Otherwise it writes a generic error message. Normalization removes configured application paths from the development message. A test that asserts a raw exception string as the production HTTP body would therefore conflict with the inspected middleware behavior.

The middleware's logging choices also vary by exception type. Some categories omit a stack trace in the selected logging branch, while other exceptions are logged with the exception object. Do not confuse what is logged with what is sent to the client. A diagnostic investigation should state which artifact it reads and avoid copying sensitive runtime details into course examples.

Model-binding failures form another path before the action body. The collection binder has its own narrow conversion handling, while integer binding uses the framework's configured behavior. A single error taxonomy should include those distinctions rather than treating every non-success as the limit guard firing.

## Exercise JF-16A: create an error-origin table

Include invalid representable limit, missing loaded user, forbidden explicit subject, malformed integer text, invalid collection token, view-manager failure and response-already-started failure. For each, identify the component that first observes it, whether a result or exception is involved and which evidence layer can verify the client response.

Mark cases whose exact public response remains unexecuted. Source inspection can predict a middleware mapping, but it does not prove the complete host path. A good table makes that distinction visible without refusing to state the source-backed facts.

## Exercise JF-16B: inject failures precisely

Design separate direct fixtures for user lookup returning null, view retrieval throwing and DTO mapping throwing. Record which later stages should not execute. Then design a middleware fixture whose next delegate throws a security exception before the response starts.

Compare the direct action observation with the middleware observation. The first may be an exception object; the second may be a status and text body. They are compatible evidence at different boundaries. Do not catch every exception inside the test and call the outcome successful merely because something failed.

## Exercise JF-16C: propose client error handling

Write a client decision table for invalid input, missing subject, forbidden subject and transient server failure. Distinguish correcting input from retrying unchanged. A read can be retried safely with respect to writes, but retrying a deterministic rejected request wastes work and does not fix its cause.

Avoid relying on development-only exception text as a stable machine-readable code. If the product needs a stronger error contract, propose explicit structured fields and compatibility tests. The course does not add that response format; it teaches how to make such a change reviewable.

## Review standard

A strong answer separates action returns, exceptions, binding and middleware, and identifies the response-started limitation. It can explain why a direct test's observed exception and a hosted response's status are different artifacts that must not be conflated.
