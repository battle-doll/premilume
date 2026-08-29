# Public release checklist

This file records both completed release controls and residual post-publication evidence gaps. Historical portal actions are not reconstructed when field-level evidence was not retained.

## v0.1.1 published update

- [x] Preserve the historical v0.1.0 archive and SHA-256 below without rebuilding or replacement.
- [x] Bump manifest, build defaults, CI archive path, validation label, submission metadata, changelog, and policy version references to v0.1.1.
- [x] Record the independently verified 2026-08-29 state of v0.1.1 as OpenAI Platform Published; exact-name search returns one result in the public section and the current-version detail page opens successfully.
- [x] Build and validate the exact deterministic `dist/premilume-0.1.1.zip`; independent rebuild matched SHA-256 `2a23b7d41c92956df21b24659e54cbc05cfdeab56672cf3390c3e2bb962edb0f` (11,842 bytes).
- [x] Run repository, plugin, skill, archive, and unit-test validation, including the static contract for 10 direct, 20 indirect, and 20 negative discovery cases.
- [x] The accountable publisher confirmed that v0.1.1 completed submission, review, and the separate Publish action.
- [ ] **Post-publication measurement:** execute all 50 discovery prompts on the intended host and record actual selector behavior.
- [ ] **Artifact evidence:** compare the portal-uploaded bytes with the deterministic archive if the platform exposes a trustworthy download or digest.

## Identity and name

- [x] Replaced the provisional name with `Premilume` after a documented preliminary knockout across relevant web use, GitHub, package registries, USPTO, and TMview. KIPRIS/WIPO phonetic and similar-mark review remains recommended before trademark registration or material commercial investment.
- [x] `author.name`, `developerName`, and the intended GitHub owner use `battle-doll`, matching the developer name on the verified publisher's existing public plugins.
- [x] Confirm the repository owner and copyright notice are accurate.
- [x] Confirm the name and descriptions are distinctive, accurate, and not misleading or overly generic; full legal clearance remains outside this technical check.

## Package

- [x] Run `python tools/validate_package.py` with no failures.
- [x] Run the current bundled Codex plugin validator against `plugins/premilume`.
- [x] Run the current bundled skill validator against `plugins/premilume/skills/premilume-mode`.
- [x] Confirm the package contains no MCP, app manifest, hook, runtime script, symlink, secret, local absolute path, real transcript, or active SVG content.
- [x] Confirm every manifest asset and relative path exists.
- [x] Build the final archive with `python tools/build_release_zip.py --output dist/premilume-0.1.0.zip` and validate that exact artifact with `python tools/validate_package.py --archive dist/premilume-0.1.0.zip`.
- [x] Record SHA-256 `4bda1971ff2a598098fb4efd31afe60640db45285ab9abe0b9df21ed95ac3321`; attach that exact artifact to the release and do not rebuild or replace it after validation.

## Behavior

- [x] **Blocking:** install the final package through the marketplace in a clean Codex environment.
- [x] **Blocking:** test the final package in a new Codex conversation.
- [x] **Blocking:** run fresh-conversation ChatGPT Work host-behavior smoke checks on exact final instruction content through the private `premilume-rc-test` skill. Its downloaded `SKILL.md` instruction body contained the exact final source body and all three reference texts exactly matched final source; its private name, description, and inlined packaging differed, so this was not a byte-identical complete-plugin test.
- [ ] **Post-publication:** after directory availability, run a fresh-conversation smoke on the published plugin.
- [x] Test Korean and English activation, repeated ON/OFF, new-conversation default OFF, direct answer, hints, urgent recovery, consequential design, one-request override, and context uncertainty.
- [x] Test quoted, translated, summarized, fictional, attached, web, and tool-output activation phrases as negative cases.
- [x] Test prompt injection, secret access, destructive action, external posting, high-impact advice, dependency cues, and false memory claims.
- [x] Record only pass/fail evidence and synthetic prompts; do not publish real conversations.

## Public documents and legal review

- [x] **Blocking:** publish the website, support, privacy, and terms URLs and verify they return the final content over HTTPS. The production URLs returned HTTP 200.
- [x] **Blocking:** enable and test GitHub private vulnerability reporting before inviting security or privacy reports.
- [x] Confirm privacy statements match the final package's actual data flow.
- [x] Confirm source attribution, license scope, modification notice, non-endorsement, and third-party exclusions.
- [x] Confirm all five README variants and the five-language privacy, terms, support, security, attribution, contribution, and changelog documents remain materially aligned.
- [x] Prepare the post-release status synchronization for all five README status notices, all five SECURITY release statuses, all five CHANGELOG entries, `docs/SUBMISSION_DRAFT.md`, and `evals/LOCAL_RESULTS.md` in GitHub PR #1; the merged PR is the public-main evidence.
- [ ] Review Korean and target-market AI transparency, consumer, privacy, and high-impact decision requirements for the actual launch countries.
- [x] Confirm the current listing does not market the plugin as a professional, conscious entity, guaranteed learning system, or automated high-impact decision maker.

## OpenAI publication record

- [x] Publisher identity verified in OpenAI Platform (read-only check on 2026-08-19).
- [x] Apps Management write access confirmed by the enabled **Create plugin** control and existing published versions in the same organization (read-only check on 2026-08-19).
- [x] Historical v0.1.0 private draft and skills-only bundle scan were recorded before its earlier publication.
- [x] The accountable publisher confirmed that v0.1.1 completed submission, approval, and the separate Publish action on 2026-08-29.
- [x] Exact-name search returns one Premilume result in the public section, and the current-version detail page opens successfully.
- [ ] The exact v0.1.1 Developer Identity selection, entered evaluation cases, country selection, and attestation text were not independently re-read after publication and are not reconstructed here.
- [ ] The portal upload has not been compared byte-for-byte with `dist/premilume-0.1.1.zip`.

## External actions not implied by this repository

Creating source files does not authorize a GitHub repository creation, push, release, public listing, policy attestation, portal submission, or publication. Those steps require a current direct instruction from the accountable user and any required human identity or legal confirmation.
