# 14. Build context and reproducible test evidence

A test command is not a complete evidence record without its working directory, project and environment. The Jellyfin checkout has a [global.json](../../../jellyfin/global.json), root build properties, central package versions and test-specific inherited properties. Those files influence which SDK, target framework, analyzers and dependencies are used before any behavior assertion runs.

## Follow inherited configuration

The test [Directory.Build.props](../../../jellyfin/tests/Directory.Build.props) imports the parent build properties and sets the test target to net10.0. The root [Directory.Build.props](../../../jellyfin/Directory.Build.props) enables nullable analysis and treats warnings as errors with specified exceptions. The focused [test project](../../../jellyfin/tests/Jellyfin.Api.Tests/Jellyfin.Api.Tests.csproj) references the real API and server implementation projects rather than an isolated copy of the controller.

The test project's package references omit explicit versions because versions are managed elsewhere, including [Directory.Packages.props](../../../jellyfin/Directory.Packages.props). Copying only the project file into an unrelated directory can lose that context. A build failure caused by missing inherited configuration is not evidence that the controller's limit behavior is wrong.

The SDK policy in global.json requests version 10.0.0 with latestMinor roll-forward. Record the SDK actually selected in an execution environment rather than assuming the requested string is the installed executable version. Starting from the nested checkout makes that context clearer. Do not substitute another project's SDK policy because both happen to target a recent framework.

## Separate stages in the run ledger

Restore resolves dependencies. Build compiles source and runs configured analyzers. Discovery finds tests. Execution runs assertions. Reporting summarizes outcomes. A failure at one stage limits what can be concluded about later stages. For example, a compiler error means no assertion in the selected suite has been observed, even if the intended test filter was correct.

An executable observation lab that copies selected source into a small disposable project has a different boundary from the real test project. It can provide focused evidence about that copied source with controlled collaborators, but it may omit framework attributes, real dependency registrations or build analyzers. Label it actual-source isolated lab rather than full application test.

Do not install packages, alter central versions or disable analyzers merely to produce a green documentation report. If the task is authoring learning content and dependencies are unavailable, record that limitation and supply a reproducible plan. When execution is appropriate and possible, preserve the exact command and output rather than relying on memory.

## Exercise JF-14A: build an environment manifest

Record the nested repository path, selected SDK, test target, project references, central package file and relevant build properties. Identify which values are inspected from source and which are observed from a command. Include the focused test class name as the intended filter scope.

Do not include credentials, personal environment dumps or unrelated machine configuration. The manifest needs enough information to reproduce the build boundary, not every variable on the computer. Synthetic or redacted paths can be used in shared learning submissions where appropriate.

## Exercise JF-14B: classify three failures

Consider missing restored assets, a warning promoted to an error and an assertion failure at the half-maximum boundary. For each, identify the stage reached, the evidence available and the next investigation. Explain why only the last directly contradicts the expected behavior assertion.

Then consider a run with zero discovered tests and exit success. Decide what evidence is needed before calling the focused suite passed. A command's exit code alone may not establish that the intended cases actually executed. Preserve discovery and count information.

## Exercise JF-14C: write a run report template

Create fields for command, working directory, environment, intended scope, discovered cases, passed/failed/skipped counts, exit code, output artifact and limitations. Add a separate section for documentation link checks so they are not mixed with application test results.

Use the template for a proposed run if you have not executed it, leaving observed fields explicitly pending. A complete template is useful preparation; fabricated pass counts are not. Later course verification should fill those fields only from actual tool output.

## Review standard

A strong report lets another engineer distinguish environment setup from behavior evidence and reproduce the intended scope. It respects repository build context and never promotes a copied-source lab, a successful build or a zero-test run into proof that the full application suite passed.
