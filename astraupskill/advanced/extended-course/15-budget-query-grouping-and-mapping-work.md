# 15. Budget query, grouping and mapping work

The latest-media path has several different size measures: requested limit, candidate query limit, candidates returned, groups assembled, representatives selected, DTOs produced and serialized bytes. A performance investigation should record them separately. Treating all of them as item count hides where work is amplified or reduced.

## Begin with a work ledger

On an ordinary retrieval path, an internal query is initially given twice the requested limit. Grouping may collapse several candidates into one container, and the loop stops when enough groups have been assembled. Some specialized collection branches instead use the original limit with a different retrieval method. DTO mapping performs further option- and type-dependent batch work.

The response can therefore contain fewer representatives than candidates, while each representative can still carry substantial associated data. A sparse or heavily grouped result is not necessarily cheap to produce. Conversely, the largest arithmetic input in a mocked test can cost almost nothing because the mock returns an empty list. Performance conclusions require a representative execution boundary.

Define measurements before adding instrumentation. Candidate count explains selection workload; group count explains output cardinality; distinct container count helps interpret grouping; mapper batch calls explain associated-data work; serialized bytes explain network payload. Elapsed time is useful but can be noisy and does not identify the stage responsible without additional context.

## Compare controlled scenarios

Use small and medium synthetic fixtures with ungrouped items, many children sharing containers and a mix of folders and ordinary media. Hold query options constant for one comparison, then vary fields or user-data options separately. This avoids attributing a mapping-cost change to grouping when the fixtures changed both dimensions.

Warm and cold behavior may differ because caches and initialization affect timing. Record which state a measurement represents. Do not average together unrelated runs and present a precise number without sample information. The course does not require a production benchmark; it teaches how to make a bounded experiment interpretable.

Operational limits are proposals that should follow such evidence. A lower maximum, option budget, response-size budget or time budget can constrain different resources. Each policy needs a clear rejection or truncation behavior and compatibility review. Silently returning fewer items under overload can create a different client contract from rejecting an oversized request.

## Exercise JF-15A: define the measurements

Build a table for request limit, assigned query limit, candidates returned, groups produced, DTO count and response bytes. Add the branch and selected options. Explain which component can observe each value without guessing. Distinguish a requested upper bound from an observed count.

For a fixture with many candidates sharing one container, predict which counts can differ and why. Do not claim the current loop scans all candidates after reaching its group threshold. Use the actual early-break rule in your prediction.

## Exercise JF-15B: design an experiment matrix

Choose three grouping shapes and two option profiles. Specify a fixed synthetic data set for each shape, expected representative IDs and the measurements to collect. Include a correctness assertion in every timed run so a faster but wrong result is not counted as an improvement.

Keep the half-maximum boundary out of real retrieval benchmarks. Its purpose belongs to the mocked arithmetic test. A realistic budget experiment can use modest sizes and extrapolation only when the model and uncertainty are stated explicitly.

## Exercise JF-15C: review a proposed cache

Consider a cache of selected latest-media groups. Identify dimensions that affect selection, including subject user, parent, played intent after preference resolution, included types and grouping. Then identify DTO options that may affect mapped output even if selection is reused.

Separate caching domain selections from caching fully mapped DTOs. The latter can contain user-specific fields and option-specific images. Define invalidation questions for library changes and preference changes. This exercise produces a review plan, not an implemented cache or a claim that a complete key has been discovered.

## Review standard

A complete investigation names the work populations, controls comparison variables and includes correctness checks alongside timing. It uses the arithmetic guard as one bounded safety fact and develops operational policy from measured work rather than treating a representable integer as a resource budget.
