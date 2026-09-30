# Prediction lab

Predict each outcome before reading the answer key. These questions isolate the conditions in their prompts. Real requests may be rejected earlier when those assumptions do not hold.

Use Python 3. Copy `answers.template.json` to a new filename in a location you choose, replace each null with your answer, then pass its absolute path to the checker. Copying is a learner action; the checker only reads files and never changes your answers.

From the project root:

```powershell
python astraupskill/advanced/labs/check-answers.py C:/path/to/my-answers.json
```

Use JSON booleans (`true`/`false`), numbers, arrays or objects exactly as requested. Array order matters. Keys in an object may appear in any order. Exit 0 means every prediction matches; exit 1 means one or more answers need review; exit 2 means malformed/missing input.

## Cases

### JF-P1

Largest positive signed-32-bit integer that can be doubled without overflow?

### JF-P2

First positive integer above that accepted guard threshold?

### JF-P3

Direct controller call with limit 0. Return expected userLookups, viewCalls and dtoCalls.

### JF-P4

Direct C# action call omits both optional limit and groupItems. Return their values.

### JF-P5

A test passes limit 20 explicitly. Does it detect changing the method declaration default to 21?

### JF-P6

Input reaches the action as valid integer limit 20, but user lookup returns null. Is passing the guard alone sufficient to promise a 200 response?

### JF-P7

isPlayed is absent; the resolved user has HidePlayedInLatest true. What boolean played-state filter does the action supply?

### JF-P8

Does direct invocation of GetLatestMedia with an int exercise HTTP parsing of limit=abc?

## After checking

For each mismatch, name the source function or stated contract that changes your prediction. The checker reports case IDs without printing the answer, so you can make another independent attempt.

Compare with [the answer key](answer-key.json) only after your attempt. The separate chapter answer guide explains the reasoning. This lab grades a mental model and does not compile, start, test or modify the application.

[Return to the advanced course](../README.md)
