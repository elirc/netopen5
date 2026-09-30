# Capstone: explain and test the whole request boundary

Deliver a small test improvement and a review packet for latest-media behavior. Complete the controller milestone first. Treat the HTTP fixture as a second stage with its own setup and evidence, not as a passing feature merely because the design is written down.

## Milestone A — contract matrix

Document defaults, accepted arithmetic range, malformed query examples, user lookup outcomes and compatibility behavior. Separate “passes the integer guard” from “returns a successful HTTP response.” Include the first layer that should handle each input and the collaborator calls permitted afterward.

## Milestone B — direct controller evidence

Add or demonstrate meaningful cases for the two adjacent upper-edge values, the smallest positive value, nonpositive input, omitted defaults and filter forwarding. Use the real controller and controlled collaborators. Preserve exact response status/value expectations while accommodating the actual typed result subclass.

Record the focused .NET command, discovered outcomes and any setup limitation. A worksheet or independently copied implementation cannot replace these results when claiming the source controller passed.

## Milestone C — HTTP fixture

Build an owned test host with real controller routing, an explicit fictional authentication setup and substituted library services. State its lifecycle and cleanup. Exercise current and legacy paths, query omission, invalid text and unauthenticated access. Keep the actual request/response evidence free of real credentials or private media data.

The fixture should show which layer rejected a request. A 400 response from binding is useful evidence, but it is different from the controller returning `BadRequest` after receiving a representable integer. Do not count both as the same assertion merely because the status number matches.

## Milestone D — defend an operational proposal

Write a short proposal for a practical result-size policy without changing production behavior as part of the lesson. Explain compatibility, user experience and measurement needs. Distinguish an arithmetic invariant from acceptable latency, allocation and service capacity. Keep maximum-value experiments mocked.

## Handoff

Provide the contract matrix, changed test files, setup, exact commands, observed outcomes and omitted claims. Ask the reviewer to choose one new input and predict the first rejecting layer. Finish with a brief explanation of what a future real-library integration test would add and why that was outside this controlled exercise.

[Advanced index](README.md) · [Main course](../README.md)
