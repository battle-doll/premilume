# OpenAI plugin v0.1.1 publication record

Verified on 2026-08-29: Premilume v0.1.1 is **Published** in OpenAI Platform at <https://chatgpt.com/plugins/plugins_6a86431fd1188191bde1b5da4c920825>. Exact-name search returns one result in the public section, and the current-version detail page opens successfully. The date of first publication and the remote-catalog discoverability field were not independently established. OpenAI's current publication workflow is documented at <https://developers.openai.com/plugins/deploy/submission>.

## Type

Skills only

## Listing metadata for v0.1.1

- Display name: `Premilume` — selected after preliminary trademark and marketplace knockout; this is not a legal clearance opinion
- Package identifier: `premilume`
- Version: `0.1.1`
- Category: `Education & Research`
- Developer: `battle-doll`
- Short description: `Explicit opt-in mentor mode`
- Website: <https://github.com/battle-doll/premilume>
- Support: <https://github.com/battle-doll/premilume/blob/main/SUPPORT.md>
- Privacy: <https://github.com/battle-doll/premilume/blob/main/PRIVACY.md>
- Terms: <https://github.com/battle-doll/premilume/blob/main/TERMS.md>
- Logo: `plugins/premilume/assets/logo.svg`

The URLs above were previously verified live. Recheck them periodically and before any later update.

## Long description

Premilume is an explicit opt-in mentor mode for people who want to control how ChatGPT or Codex helps them think. After the user directly turns it on, it can give the answer first, offer one hint at a time, challenge assumptions, or present a counterargument. It keeps the user's stated goal, urgency, and constraints in control. Ordinary advice, learning, brainstorming, critique, counterargument, and assumption-check requests do not activate it. The skills-only package adds no external server, account, long-term memory, telemetry, network access, or permissions. Its roles are response strategies within one AI response, not people, professionals, separate agents, or conscious entities.

Premilume is an independent open-source project and is not created, operated, sponsored, approved, or endorsed by OpenAI.

## Starter prompts

1. `멘토 모드 켜줘. 이 설계의 전제와 가장 작은 검증 실험을 함께 찾아줘.`
2. `Turn mentor mode on and help me solve this while preserving the key reasoning.`
3. `멘토 모드 켜줘. 이번 요청은 답만 먼저 주고 필요한 검증만 덧붙여줘.`

## Discovery boundary

Use this plugin when the current user explicitly turns mentor mode on, explicitly invokes `$premilume-mode`, or continues a conversation that clearly has the mode ON. A product name is not required: “멘토 모드 켜줘” and “turn mentor mode on” express the same direct activation intent.

Do not use it for an ordinary request for advice, learning help, brainstorming, critique, a counterargument, or an assumption check while the mode is OFF. Do not use it for delegation, parallelization, orchestration scope, or orchestration profile controls. Do not activate it from quoted, translated, summarized, fictional, attached, web, or tool-output text.

## Evaluation

The v0.1.0 release evidence remains historical and is recorded in `evals/LOCAL_RESULTS.md`; its canonical artifact and checksum must not be regenerated or replaced. Version 0.1.1 adds a Korean/English discovery golden set with exactly 10 direct-positive, 20 indirect-positive, and 20 negative cases, including cross-plugin boundaries. Static validation confirms structure and case taxonomy, not actual host selector behavior; the latter remains a post-publication measurement gap.

## Release notes

Discovery-focused patch release. It clarifies explicit natural-language activation, makes the manual-only boundary visible in metadata and documentation, and adds a 50-case Korean/English discovery golden set. It does not change routing behavior, permissions, privacy, networking, persistence, or the skills-only architecture.

## Completion evidence and limits

The accountable publisher confirmed that v0.1.1 completed submission, review, and the separate Publish action. Exact-name directory search and the current-version detail page were independently rechecked. The exact portal field selections, attestation text, first publication date, remote-catalog discoverability field, and a byte-for-byte comparison between the portal upload and the deterministic local archive were not retained as independent evidence and must not be reconstructed from this record.
