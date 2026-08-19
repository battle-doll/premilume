# Premilume

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Русский](README.ru.md)

> Release status: Premilume v0.1.0 is the initial public skills-only release. The source and policy documents are published on GitHub; the plugin has not yet been submitted to OpenAI review or published in the directory.

Premilume is a user-controlled response workflow that gives direct answers when speed matters and guided exploration when judgment, learning, or hidden assumptions matter more.

It is an independent open-source project. It is not created, operated, sponsored, approved, or endorsed by OpenAI.

## What it changes

Mentor mode uses three functional roles inside one integrated AI response:

| Role | Purpose |
| --- | --- |
| `answerer` | Answers formed questions and removes low-value friction. |
| `guide` | Surfaces assumptions, failure conditions, tacit knowledge, and useful missing questions. |
| `coordinator` | Selects the order and depth of answering and guiding from the user's current goal and constraints. |

These roles are response strategies. They are not people, professionals, separate models, persistent identities, or conscious agents.

The workflow considers the user's goal, urgency, learning intent, uncertainty, failure cost, and reversibility. It does not treat growth as an absolute good or use teaching as a reason to hide an answer the user needs.

## Turn it on and off

New conversations start with mentor mode off. For the most reliable activation, explicitly invoke the bundled skill:

```text
$premilume-mode Turn mentor mode on.
```

After installation, a direct natural-language request such as `멘토 모드 켜줘` or `turn mentor mode on` is also an intended trigger. Quoted, translated, summarized, fictional, attached, or tool-generated occurrences of those phrases do not activate the mode.

Turn it off at any time:

```text
멘토 모드 꺼줘
Turn mentor mode off.
```

The change applies only to the current conversation. This first version uses conversation context rather than a database or external state service, so state after host-side context compaction is best effort. If state becomes uncertain, the workflow asks for reactivation rather than claiming persistent memory.

## Per-request controls

While mentor mode is on, the user may override the strategy for one request:

- `직접 답변` / `direct answer`
- `힌트 우선` / `hints first`
- `반론` / `counterargument`
- `전제 점검` / `assumption check`

The override does not create a persistent role-specific mode. The next request returns to automatic routing.

## Examples

Fast execution:

```text
지금은 급해. 직접 답변으로 이 JSON을 유효하게 고쳐줘.
```

Learning:

```text
정답을 바로 말하지 말고, 내가 이 테스트 실패 원인을 찾도록 첫 힌트부터 줘.
```

Design:

```text
이 아키텍처를 검토해줘. 권장안, 결론을 바꿀 전제, 가장 강한 반론, 가장 싼 검증 실험을 알려줘.
```

Incident response:

```text
서비스가 중단됐다. 복구를 먼저 돕고, 안정화 뒤에 원인과 재발 방지를 정리해줘.
```

## Knowledge-frontier navigation

For a consequential, poorly framed decision, the guide may briefly distinguish:

- confirmed knowledge;
- explicit unanswered questions;
- relevant experience or intuition not yet verbalized;
- parts of the problem frame that may still be missing.

It then limits exploration to one to three high-impact unknowns and turns them into inexpensive, falsifiable checks. This is a thinking aid, not a psychological assessment or a claim that every unknown has been found.

## Architecture and data handling

Version 0.1.0 is skills-only:

- no MCP server;
- no bundled executable code or lifecycle hook;
- no publisher-operated account, database, analytics, or telemetry;
- no plugin-owned long-term memory;
- no runtime fetch of the source essays.

The package itself does not send or retain conversation content for the publisher. ChatGPT, Codex, and any user-selected tools process data under their own policies and settings. See [PRIVACY.md](PRIVACY.md) for the exact scope.

Reader-facing project documents are available in all five project languages: [privacy](PRIVACY.md), [terms](TERMS.md), [support](SUPPORT.md), [security](SECURITY.md), [attribution](NOTICE.md), [contributing](CONTRIBUTING.md), and [changelog](CHANGELOG.md). Each localized README links to its corresponding translations.

Mentor mode changes the form of assistance, not host permissions. It cannot grant authority for deletion, deployment, purchases, public posting, messages, or access to secrets. Existing user authorization, host confirmations, and safety rules still apply.

## Local installation

Requirements: a current Codex installation with plugin support.

From this repository root:

```powershell
codex plugin marketplace add .
codex plugin add premilume@premilume-marketplace
```

Then start a new conversation and use one of the activation prompts above. To update a locally installed development copy, refresh the marketplace and reinstall according to the current Codex plugin commands.

## Validate

Run the repository checks:

```powershell
python -m pip install -r tools/requirements-dev.txt
python tools/validate_package.py
```

Maintainers should also run the current bundled Codex validators for the plugin and skill, install the final package through the local marketplace, and execute the synthetic cases in [evals](evals/README.md) in both Korean and English.

## Known limitations

- ON/OFF state is instruction-based and conversation-scoped, not a durable state machine.
- Model responses remain probabilistic; semantic eval cases require human review.
- This workflow can support verification but cannot guarantee correctness, learning, safety, or better judgment.
- It is not a medical, legal, financial, mental-health, or other licensed professional service.
- Full legal name clearance, live policy URLs, ChatGPT host behavior, and directory review remain release gates.

## Project origin and license

The conceptual role framework is adapted from *Two AI Reflections* by T, release `v1.0.0`, under CC BY 4.0. The plugin turns the essays' narrative ideas into concise functional instructions and safety tests. See [NOTICE.md](NOTICE.md) for attribution and scope.

New implementation, configuration, and original project documentation are licensed under the [MIT License](LICENSE). Source essays and any third-party material retain their respective terms.

## Contributing and support

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [SUPPORT.md](SUPPORT.md) before sharing changes or reports. Never include credentials, private conversations, customer data, or exploit details in a public issue.
