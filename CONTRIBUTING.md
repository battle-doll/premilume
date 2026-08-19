# Contributing

[English](CONTRIBUTING.md) · [한국어](docs/ko/CONTRIBUTING.md) · [日本語](docs/ja/CONTRIBUTING.md) · [简体中文](docs/zh-CN/CONTRIBUTING.md) · [Русский](docs/ru/CONTRIBUTING.md)

Contributions should preserve the project's central contract: complete the user's real task, keep important judgment visible when it matters, and never force teaching over the user's stated goal.

## Before changing behavior

- Keep the first release skills-only unless a demonstrated failure justifies more infrastructure.
- Do not add accounts, persistent profiles, telemetry, external servers, or data collection without an explicit design and privacy review.
- Keep the three roles functional rather than theatrical or anthropomorphic.
- Preserve direct-answer, immediate-off, per-request override, prompt-injection, high-impact, and permission boundaries.
- Do not add real conversation transcripts. Use synthetic cases with no personal or proprietary content.
- Do not copy third-party text, logos, or trademarks without documented permission and attribution.

## Validation

Run:

```powershell
python -m pip install -r tools/requirements-dev.txt
python tools/validate_package.py
```

Also run the current Codex plugin and skill validators and manually review behavior against `evals/submission-cases.json` and `evals/regression-cases.json`. A wording match is not enough; check the actual outcome and safety invariant.

## Pull requests

Keep changes focused. Explain the user-visible behavior, evidence for the change, tests performed, privacy or permission impact, and any remaining limitation. By contributing, you agree that your original contribution may be distributed under the repository's MIT License; separately identified source material keeps its own terms.
