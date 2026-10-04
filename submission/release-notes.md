# Build Omarchy Plugins v0.7.0 — Give your agent enforceable rules

This v0.7.0 candidate turns selected architecture decisions into checks your
plugin can run in CI, and brings the skills up to date with the marketplace
reviewed on 3 October.

- **Make chosen boundaries stick.** The validator can now reject recognized
  QML/JS networking, dynamic code, process execution or collected-input patterns
  with repeatable `--deny-capability` flags. Rules are opt-in; ordinary advisory
  findings keep their existing behaviour.
- **Start with literal text.** Generated panels, menus and overlays explicitly
  render text as plain text, including external summon data and titles.
- **Follow current reviewer decisions.** Guidance separates withdrawn resource
  findings from active credential, command and filesystem concerns, and explains
  form errors, repository migrations, refresh delays and manual setup.
- **Reuse small, testable boundaries.** Design and service guidance now defines
  narrow contracts for network readers, process runners, private storage, display
  text and approvals. Callers get explicit results and errors; implementation
  details stay inside the adapter.

The provider-neutral bundle still contains twelve skills, with synchronized
portable and OpenAI copies, OpenCode support and native Claude packaging.
The package retains transactional updates and an SPDX 2.3 SBOM.
CI targets Linux, macOS, and Windows; release automation prepares drafts and
cannot publish them. Install commands continue to point at the
published v0.6.1 release while this candidate is under review.

The new gate is lexical: comments can match and indirect code can escape it.
It does not sandbox QML or establish marketplace approval. Live Omarchy rendering
and lifecycle checks remain unrun, and token savings have not been measured.
Validation evidence is recorded in `evals/ACCEPTANCE.md`; final CI and publication
are separate gates.

[Changes since v0.6.1](https://github.com/tcballard/build-omarchy-plugins/compare/v0.6.1...release/v0.7.0)
