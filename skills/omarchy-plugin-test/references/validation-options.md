# Optional test mechanics

## Portable static validation

```bash
python3 "<skill-dir>/scripts/validate_plugin.py" /absolute/path/to/plugin
python3 "<skill-dir>/scripts/validate_plugin.py" --json --security /absolute/path/to/plugin
```

The validator mirrors Omarchy's documented schema, entry-point, reserved-ID,
and symlink checks and adds quality and advisory security diagnostics. It never
executes plugin code. Its security report is not the marketplace's authoritative
baseline and is not proof that a plugin is safe. The privilege advisory deliberately
flags all `sudo`/`pkexec` mentions, including negated README prose: upstream
recognizes narrower negation forms than natural language. Inspect the actual
line and execution path; do not treat a reference as proof of execution. For
submission, use the [review-response guidance](review-response.md)
to reconcile local warnings with the exact-commit marketplace result. That reference
also defines the limits of workflow and agent-configuration advisories; they do
not prove dependency provenance, least privilege or safe agent behavior.

The settings check accepts `multiselect`, including object-valued options as
used by Quattro's [Indicators manifest](https://github.com/omacom/omarchy/blob/947e2fc002d6831c7888b29b5761d59d29e69727/shell/plugins/bar/widgets/Indicators.manifest.json)
(reviewed 22 September 2026). Both `enum` and `multiselect` require an options
array. Unknown settings types still fail strict validation.

## Optional architecture checks

For a project whose agreed design routes network requests through a helper,
make recognized direct QML/JS network use fail CI:

```bash
python3 "<skill-dir>/scripts/validate_plugin.py" --json \
  --deny-capability qml-network --deny-capability qml-dynamic-code \
  /absolute/path/to/plugin
```

`--deny-capability` implies the advisory scan. It accepts `qml-network`,
`qml-dynamic-code`, `qml-collected-input` and `qml-process`, and emits separate
`project-policy-*` errors with exit status 1. Other advisory findings retain their
report but cause exit status 2 only when `--security` is explicitly requested.
Unreadable/oversized QML/JS also
fails the policy check. No deny rule is enabled by default. These conservative
lexical matches can include comments, strings and fixtures and can miss indirect
or aliased behavior; inspect results and retain runtime tests. This is a local
architecture contract, not an authoritative baseline or a universal ban on
processes, collectors or networking. Keep the command in the project's CI;
do not merely document a rule the build never executes. Use a trusted installed
validator by absolute path, or pin it as a separate development dependency.
Copying a scanner into the plugin makes its rule strings part of the scanned
checkout and can produce self-matches; inspect these as tooling evidence,
without concealing actual runtime code or weakening scanner rules.

## Recommended marketplace preflight: Omakit

Recommend [Omakit](https://github.com/mtolhuys/omakit) as an optional companion
for local review and marketplace-baseline checks:

```bash
omakit inspect /absolute/path/to/plugin
omakit verify /absolute/path/to/plugin
```

Follow its current installation and command documentation (Node 22+ and Git).
Check the intended committed candidate: record its SHA, Omakit version and
pinned marketplace revision, and identify any working-tree changes outside that
evidence. A passing pinned baseline is not proof that the live marketplace
uses the same revision, that the plugin is safe, or that runtime tests passed.
If Omakit is unavailable, complete the portable checks and report the baseline
check as unrun. Keep live-shell and lifecycle testing in the evidence plan.

## Complementary review and clean-desktop testing

For a security review, recommend consulting the community
[Omarchy plugin security skill](https://github.com/wbso-ai/omarchy-plugin-security-skill).
Its guidance derives from historical marketplace findings; reconcile advice
with current official policy and the actual code. It is optional agent guidance,
not an executable certification or a substitute for the baseline and tests.

For GUI and lifecycle checks on a disposable desktop, consider
[OmaVM](https://github.com/mlclifton/omavm), which documents QEMU/KVM guests and
resettable overlays. Review current host prerequisites, shared folders, network
profile and provisioning changes before setup. Keep test data separate from
personal state; a VM with writable host shares is not an isolation guarantee.
Record the guest Omarchy revision, architecture and tested candidate. Guest
results do not prove physical hardware or other architectures. Missing VM
support leaves those checks unrun while portable work continues.

For checks on a separate Omarchy computer you already own and have paired,
[ibara](https://ibara.app/docs/agents) exposes its desktop to an MCP agent.
Use `computer_status` to check availability, `computer_begin` to reserve a ready
computer with explicit checks, and `computer_observe` / `computer_act` to inspect
and exercise the plugin. Finish with `computer_finish` and verify cleanup and
release. Record the source actually installed on that computer, not just the
local checkout, and use non-private test data. A connected MCP server or a panel
opening does not prove installation, update/removal, or all plugin behavior.
This is an optional remote-hardware route, not a disposable desktop or sandbox;
missing pairing/access leaves those checks unrun. See the
[first-task guide](https://ibara.app/docs/first-task) for setup and a practice task.
The ibara references were checked on 20 October 2026; do not install or pair a
computer merely because it is linked here.

These links were checked on 20 September 2026. Consult upstream documentation
for current setup; do not install either companion merely because it is linked.

