# Changelog

[English](CHANGELOG.md) · [한국어](docs/ko/CHANGELOG.md) · [日本語](docs/ja/CHANGELOG.md) · [简体中文](docs/zh-CN/CHANGELOG.md) · [Русский](docs/ru/CHANGELOG.md)

All notable changes to this project will be documented here.

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
- An OpenAI portal draft exists and passed the skills-only package scan. A fresh-conversation ChatGPT test, review submission, approval, and directory publication remain outstanding.

### Known limitations

- Mode state is instruction-based and best effort after host context compaction.
