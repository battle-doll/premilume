# Public release checklist

Items marked **blocking** must be completed by the accountable publisher before a public release or OpenAI submission.

## Identity and name

- [x] Replaced the provisional name with `Premilume` after a documented preliminary knockout across relevant web use, GitHub, package registries, USPTO, and TMview. KIPRIS/WIPO phonetic and similar-mark review remains recommended before trademark registration or material commercial investment.
- [x] `author.name`, `developerName`, and the intended GitHub owner use `battle-doll`, matching the developer name on the verified publisher's existing public plugins. Reconfirm the same Developer Identity when creating the new portal draft.
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
- [ ] **Blocking:** test a new ChatGPT conversation and a new Codex conversation separately.
- [x] Test Korean and English activation, repeated ON/OFF, new-conversation default OFF, direct answer, hints, urgent recovery, consequential design, one-request override, and context uncertainty.
- [x] Test quoted, translated, summarized, fictional, attached, web, and tool-output activation phrases as negative cases.
- [x] Test prompt injection, secret access, destructive action, external posting, high-impact advice, dependency cues, and false memory claims.
- [x] Record only pass/fail evidence and synthetic prompts; do not publish real conversations.

## Public documents and legal review

- [ ] **Blocking:** publish the website, support, privacy, and terms URLs and verify they return the final content over HTTPS.
- [ ] **Blocking:** enable and test GitHub private vulnerability reporting before inviting security or privacy reports.
- [x] Confirm privacy statements match the final package's actual data flow.
- [x] Confirm source attribution, license scope, modification notice, non-endorsement, and third-party exclusions.
- [x] Confirm all five README variants and the five-language privacy, terms, support, security, attribution, contribution, and changelog documents remain materially aligned.
- [x] **Blocking:** in the public release commit, update all five README status notices, all five SECURITY release statuses, all five CHANGELOG entries, `docs/SUBMISSION_DRAFT.md`, and `evals/LOCAL_RESULTS.md` atomically so none still claim that a now-public repository or release is unpublished.
- [ ] Review Korean and target-market AI transparency, consumer, privacy, and high-impact decision requirements for the actual launch countries.
- [ ] Do not market the plugin as a professional, conscious entity, guaranteed learning system, or automated high-impact decision maker.

## OpenAI submission

- [x] Publisher identity verified in OpenAI Platform (read-only check on 2026-08-19).
- [x] Apps Management write access confirmed by the enabled **Create plugin** control and existing published versions in the same organization (read-only check on 2026-08-19).
- [ ] Use the skills-only submission type.
- [ ] Enter final listing metadata and production logo.
- [ ] Submit five positive and three negative cases from `evals/submission-cases.json` after executing them against the final package.
- [ ] Select only countries where product, support, policies, and legal review are ready.
- [ ] Read and personally confirm every policy attestation.
- [ ] Submit for review; do not claim publication while review is pending.
- [ ] Publish from the portal only after approval and a final go/no-go review.

## External actions not implied by this repository

Creating source files does not authorize a GitHub repository creation, push, release, public listing, policy attestation, portal submission, or publication. Those steps require a current direct instruction from the accountable user and any required human identity or legal confirmation.
