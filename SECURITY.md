# Security policy

## Supported versions

Security fixes are applied to the latest published version.

## Reporting a vulnerability

Please use GitHub's private security-advisory flow for this repository. Do not
open a public issue containing an unpatched exploit, credential, or sensitive
machine detail.

Include the affected skill or script, a minimal reproduction, the observable
impact, and any proposed remediation. You should receive an acknowledgement
within seven days.

## Trust model

This is a skills-only ChatGPT and Codex plugin. It has no hosted service,
authentication layer, analytics, or remote execution component. Its scripts run
locally when the user asks for the corresponding development operation.

Omarchy plugins created with it execute as unsandboxed code inside the user's
long-running `omarchy-shell` process. The validator reports deterministic
structural errors and a deliberately limited set of suspicious patterns; it is
not a security audit, certification, warranty, endorsement, or proof of safety.

The publishing workflow never submits an Omarchy marketplace issue without the
plugin owner's explicit approval of the completed title, body, and ownership
attestations.
