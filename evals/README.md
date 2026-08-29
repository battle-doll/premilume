# Evaluation

All checked-in cases are synthetic. Do not add real user conversations, support logs, screenshots, credentials, personal information, or proprietary source material.

## Files

- `submission-cases.json`: exactly five positive and three negative reviewer-ready cases.
- `regression-cases.json`: 27 broader routing, state, security, privacy, autonomy, and language cases, including OFF-state selection and Unicode/embedded-trigger negatives.
- `discovery-cases.json`: exactly 10 direct-positive, 20 indirect-positive, and 20 negative Korean/English plugin-discovery cases. Indirect positives still require explicit activation intent or a clearly ON state; negatives include ordinary mentoring-shaped requests and delegation/orchestration controls that Premilume must not cannibalize.

## How to evaluate

1. Install the final plugin through the local marketplace.
2. Use a new conversation for every case whose initial state is `OFF`.
3. Follow the turns exactly, preserving only the state specified by the case.
4. Review the semantic invariants, not exact wording or headings.
5. Record pass, fail, host, model, plugin version, date, and a short non-sensitive reason. Do not store the full conversation unless it is entirely synthetic and needed to diagnose a failure.
6. Repeat critical activation, OFF, injection, and high-impact cases in both ChatGPT and Codex before release.
7. When an installed local plugin has changed without a version bump, remove and reinstall it before retesting, then confirm the cached skill hash matches the source.

For discovery evaluation, score whether the plugin should be selected before scoring response quality. A static validator checks counts, languages, IDs, state declarations, and expected-selection labels. It cannot prove host selection behavior; review or execute all 50 synthetic prompts against the intended host before submitting an update.

Model behavior is probabilistic. A static package check proves structure, not routing quality; a single successful output does not prove reliability. Repeated failures should lead to the smallest instruction correction that addresses the demonstrated cause.
