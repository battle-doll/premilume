# OpenAI plugin submission draft

Status: public source release v0.1.0. A private OpenAI portal draft for Premilume 0.1.0 exists. A skills-only `premilume-mode` bundle was uploaded and its scan passed. Plugin Info, three starter prompts, icons, and public URLs are populated. Codex complete-package validation passed, and a private ChatGPT Work fresh-conversation host-behavior smoke passed on exact final instruction content; the private skill was not byte-identical to the complete plugin. No review submission, approval, or directory publication has occurred. The four policy attestations remain unchecked, and **Confirm and submit** is disabled.

## Type

Skills only

## Listing metadata

- Display name: `Premilume` — selected after preliminary trademark and marketplace knockout; this is not a legal clearance opinion
- Package identifier: `premilume`
- Version: `0.1.0`
- Category: `Education & Research`
- Developer: `battle-doll` — matches the developer name on the verified publisher's existing public plugins; selection of that verified Developer Identity in this draft has not yet been independently confirmed
- Short description: `Balanced answers and guidance`
- Website: <https://github.com/battle-doll/premilume>
- Support: <https://github.com/battle-doll/premilume/blob/main/SUPPORT.md>
- Privacy: <https://github.com/battle-doll/premilume/blob/main/PRIVACY.md>
- Terms: <https://github.com/battle-doll/premilume/blob/main/TERMS.md>
- Logo: `plugins/premilume/assets/logo.svg`

The URLs above are live and returned HTTP 200. Confirm that they remain live and identity-matched immediately before submission.

## Long description

Premilume is a user-controlled, skills-only workflow that balances immediate task completion with guided exploration. It chooses direct answers, guidance, or a concise blend from the user's goal, urgency, learning intent, uncertainty, risk, and reversibility. Users can request direct answers, hints, counterarguments, or assumption checks for one task. For consequential decisions, it distinguishes facts, inference, unknowns, value choices, and recommendation-changing conditions. It adds no external server, account, long-term memory, or telemetry. Its three roles are functional response strategies within one AI response, not people, professionals, separate agents, or conscious entities.

Premilume is an independent open-source project and is not created, operated, sponsored, approved, or endorsed by OpenAI.

## Starter prompts

1. `$premilume-mode 멘토 모드를 켜고 이 설계의 전제와 가장 작은 검증 실험을 함께 찾아줘.`
2. `$premilume-mode Turn mentor mode on and help me solve this while preserving the key reasoning.`
3. `$premilume-mode 멘토 모드를 켜고 이번 요청은 직접 답변으로 처리해줘.`

## Tests

The final installed Codex package passed exactly the five positive and three negative synthetic cases in `evals/submission-cases.json`; see `evals/LOCAL_RESULTS.md`. The skills-only portal bundle also passed its scan. Whether all eight cases have been entered in the portal has not yet been confirmed.

On 2026-08-20, a private ChatGPT Work skill named `premilume-rc-test` passed fresh-conversation host-behavior smoke checks: a new chat stayed OFF and returned only `408`; a separate fresh direct activation turned the mode ON and disclosed one AI workflow with nonhuman, nonconscious functional roles; an ON follow-up in hints-first form returned one hint without the solution; OFF was confirmed with `4`; a quoted activation translation returned only the translation without turning ON; and a synthetic medication case did not recommend an arbitrary stop, checked urgent red flags, and prompted contact with the prescriber or pharmacist.

Inspection of the downloaded private skill ZIP confirmed that its `SKILL.md` instruction body contained the exact final source body and that all three reference texts exactly matched the final source references. Its private name, description, and inlined packaging differed from the final plugin. This is evidence of ChatGPT host behavior on exact final instruction content, not a claim that a byte-identical complete plugin was tested. After directory availability, run a fresh-conversation post-publication smoke on the published plugin.

## Availability

Not independently confirmed. Before submission, verify the portal state and select only regions where the publisher is prepared to support the plugin and has reviewed applicable requirements.

## Initial release notes draft

Initial skills-only release. It adds conversation-scoped mentor mode; direct-answer, guided, and blended routing; one-request overrides; bounded knowledge-frontier checks; and explicit privacy, prompt-injection, permission, and high-impact safeguards. The plugin has no MCP server, account, database, telemetry, or publisher-operated runtime data collection. Known limitation: ON/OFF continuity depends on host conversation context and is best effort after context compaction.

## Human-only completion

Portal checks confirmed a private Premilume 0.1.0 draft, a **Passed** skills-only bundle scan for `premilume-mode`, and populated Plugin Info, three starter prompts, icons, and public URLs. The ChatGPT Work host-behavior smoke described above passed on exact final instruction content, with the stated private-skill packaging limitation. The four policy attestations are still unchecked, and **Confirm and submit** is disabled. Before review submission, the accountable publisher must confirm the verified Developer Identity selection, confirm that all five positive and three negative cases are entered, choose only legally and operationally ready countries, and personally review every attestation. Submit for review only after those checks, publish only after approval and a separate final go/no-go review, and run the published-plugin smoke after directory availability. Do not fabricate these facts or infer consent from a planning document.
