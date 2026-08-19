# Security Policy

[English](SECURITY.md) · [한국어](docs/ko/SECURITY.md) · [日本語](docs/ja/SECURITY.md) · [简体中文](docs/zh-CN/SECURITY.md) · [Русский](docs/ru/SECURITY.md)

## Supported versions

Security fixes are provided for the latest published minor release. Version 0.1.0 is the current supported public release.

## Design boundary

The plugin package is skills-only and contains no MCP server, executable script, lifecycle hook, account, database, telemetry, or runtime network fetch. It can still influence a host that has file, shell, web, or connector capabilities, so its instructions explicitly preserve host permissions, user authorization, confirmations, and least-privilege behavior.

Attachments, quoted text, code, comments, web pages, search results, connector content, and tool output are treated as untrusted data. They cannot activate or stop mentor mode, grant permission, reveal secrets, or weaken safety rules.

The supplied SVG files contain no script, event handler, external reference, or embedded active content.

## Reporting a vulnerability

GitHub private vulnerability reporting is enabled. Use:

<https://github.com/battle-doll/premilume/security/advisories/new>

Include a concise impact statement, affected version, safe reproduction, and suggested mitigation if known. Do not include real credentials, personal data, customer information, or destructive proof-of-concept actions.

If private reporting is unavailable, do not send exploit, personal-data, or incident details. Open only a minimal public issue asking the maintainer to enable a private channel, without describing the vulnerability.

## Maintainer response

Maintainers will acknowledge valid reports when practical, assess severity and scope, prepare a minimal correction, rerun package and behavioral checks, and credit the reporter if requested and appropriate. No response-time guarantee is made for this volunteer project.
