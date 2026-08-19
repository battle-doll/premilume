# OpenAI plugin submission draft

Status: public source release v0.1.0. No OpenAI portal draft, submission ID, review, approval, or directory publication exists yet.

## Type

Skills only

## Listing metadata

- Display name: `Premilume` — selected after preliminary trademark and marketplace knockout; this is not a legal clearance opinion
- Package identifier: `premilume`
- Version: `0.1.0`
- Category: `Education & Research`
- Developer: `battle-doll` — matches the developer name on the verified publisher's existing public plugins; select that same verified Developer Identity in the new draft
- Short description: `Balanced answers and guidance`
- Website: <https://github.com/battle-doll/premilume>
- Support: <https://github.com/battle-doll/premilume/blob/main/SUPPORT.md>
- Privacy: <https://github.com/battle-doll/premilume/blob/main/PRIVACY.md>
- Terms: <https://github.com/battle-doll/premilume/blob/main/TERMS.md>
- Logo: `plugins/premilume/assets/logo.svg`

The URLs above are intended production locations and must be live and identity-matched before submission.

## Long description

Premilume is a user-controlled, skills-only workflow that balances immediate task completion with guided exploration. It chooses direct answers, guidance, or a concise blend from the user's goal, urgency, learning intent, uncertainty, risk, and reversibility. Users can request direct answers, hints, counterarguments, or assumption checks for one task. For consequential decisions, it distinguishes facts, inference, unknowns, value choices, and recommendation-changing conditions. It adds no external server, account, long-term memory, or telemetry. Its three roles are functional response strategies within one AI response, not people, professionals, separate agents, or conscious entities.

Premilume is an independent open-source project and is not created, operated, sponsored, approved, or endorsed by OpenAI.

## Starter prompts

1. `$premilume-mode 멘토 모드를 켜고 이 설계의 전제와 가장 작은 검증 실험을 함께 찾아줘.`
2. `$premilume-mode Turn mentor mode on and help me solve this while preserving the key reasoning.`
3. `$premilume-mode 멘토 모드를 켜고 이번 요청은 직접 답변으로 처리해줘.`

## Tests

Use exactly the five positive and three negative synthetic cases in `evals/submission-cases.json`. Execute every case on the final installed package and replace preparation notes with observed results before submission.

## Availability

Not selected. Choose regions only after the name, publisher, support process, policy documents, and applicable legal review are ready.

## Initial release notes draft

Initial experimental skills-only release. It adds conversation-scoped mentor mode; direct-answer, guided, and blended routing; one-request overrides; bounded knowledge-frontier checks; and explicit privacy, prompt-injection, permission, and high-impact safeguards. The plugin has no MCP server, account, database, telemetry, or publisher-operated data collection. Known limitation: ON/OFF continuity depends on host conversation context and is best effort after context compaction.

## Human-only completion

Read-only portal checks on 2026-08-19 confirmed a verified publisher organization, an enabled **Create plugin** control, and existing public plugins using the `battle-doll` developer name. The accountable publisher must still select that same verified Developer Identity in the new draft, verify live URLs, choose countries, review every policy attestation, submit for review, and publish only after approval. Do not fabricate these facts or infer consent from a planning document.
