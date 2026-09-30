# From an integer guard to an HTTP contract

This continuation uses Jellyfin's latest-media endpoint to teach boundary analysis, observable side effects, compatibility and evidence selection. A small guard is a useful starting point because you can reason about every accepted and rejected boundary without needing a full media library.

You should be able to read a C# method, a boolean condition, a mocked dependency and an HTTP request. Plan five or six sessions. Start with arithmetic and direct controller calls, then design a separate HTTP-level extension. Keep those evidence layers distinct in your notes.

1. [Route and source map](01-route-and-source.md): prerequisites, commands and evidence boundaries.
2. [Worked boundary traces](02-boundary-traces.md): calculate exact edges and downstream calls.
3. [Debugging labs](03-debugging-labs.md): distinguish plausible but incomplete fixes.
4. [Independent exercises](04-independent-exercises.md): defaults, forwarding and HTTP test design.
5. [Solutions and review](05-solutions-and-review.md): check predictions and assess evidence.
6. [Capstone](06-capstone.md): defend a complete endpoint contract.

The [prediction worksheet](labs/README.md) runs without .NET or a server. It checks your model of the documented controller behavior; it does not test Jellyfin. Use the actual focused .NET suite when making claims about controller execution. Use a real HTTP pipeline when making claims about routing, binding and middleware.

The mathematical upper bound avoids one integer-doubling overflow. It is not a recommended page size or proof that a server can service a request of that magnitude. Keep large-boundary experiments in mocked tests; do not ask a running media server to process a billion-item query for a lesson.

[Original course](../README.md) · [Historical verification](../VERIFICATION.md)


[Extended latest-media engineering course](extended-course/README.md): twenty-four chapters, seventy-two exercises, separate reviews, a bounded extracted-source lab, and two assessed capstones.
