# Changelog

[English](CHANGELOG.md) · [한국어](docs/ko/CHANGELOG.md) · [日本語](docs/ja/CHANGELOG.md) · [简体中文](docs/zh-CN/CHANGELOG.md) · [Русский](docs/ru/CHANGELOG.md)

All notable changes to this project will be documented here.

## [0.1.1] - 2026-08-29

### Changed

- Reframed manifest, skill, and agent metadata around explicit opt-in mentor-mode requests in natural Korean and English.
- Made the manual-only activation boundary and non-goals for ordinary advice, learning, critique, and orchestration controls explicit without changing runtime behavior or permissions.
- Reworked the five README openings around the user problem, audience, use path, starter prompts, and key boundaries.
- Added a validated discovery golden set with 10 direct, 20 indirect, and 20 negative Korean/English cases, including cross-plugin cannibalization checks.
- Synchronized candidate version surfaces and publication records while preserving the immutable v0.1.0 artifact and checksum.

### Publication status

- Verified on 2026-08-29: v0.1.1 is Published in OpenAI Platform at <https://chatgpt.com/plugins/plugins_6a86431fd1188191bde1b5da4c920825>; exact-name search returns one result in the public section and the current-version detail page opens successfully.
- Publication is not evidence of improved selector performance. A post-publication fresh-conversation smoke and actual selector success across all 50 discovery prompts remain unmeasured.

## [0.1.0] - 2026-08-19

### Added

- Skills-only plugin and local marketplace package.
- Conversation-scoped mentor mode with explicit ON/OFF behavior.
- Functional `answerer`, `guide`, and `coordinator` routing.
- One-request direct-answer, hints-first, counterargument, and assumption-check controls.
- Bounded knowledge-frontier navigation.
- Prompt-injection, permission, high-impact, privacy, and anti-dependency boundaries.
- English, Korean, Japanese, Simplified Chinese, and Russian reader documentation; synthetic evals; static validation; and submission-preparation materials.
- Explicit OFF-state early return and a private vulnerability reporting channel.

### Release status

- Version 0.1.0 was released publicly on GitHub on 2026-08-19 with live policy and support URLs and private vulnerability reporting enabled.
- An OpenAI portal draft exists and its skills-only bundle scan passed; the complete final package also passed Codex validation.
- On 2026-08-20, a private ChatGPT Work release-candidate skill passed fresh-conversation host-behavior smoke checks on exact final instruction content. Its downloaded instruction body and three reference texts matched the final source, but its private name, description, and inlined packaging differed, so it was not a byte-identical complete-plugin test. Review submission, approval, and directory publication remain outstanding, and the published plugin requires a post-publication smoke after directory availability.

### Known limitations

- Mode state is instruction-based and best effort after host context compaction.
