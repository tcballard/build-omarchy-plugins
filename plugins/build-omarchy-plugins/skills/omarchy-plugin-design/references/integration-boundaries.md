# Agent, authentication and privileged integrations

Use only for plugins with these integrations. Based on specific maintainer
reviews checked 20 September 2026; these are implementation concerns, not new
universal gates for ordinary widgets.

## Agents consuming external data

Remote incidents, repository diffs and voice input are untrusted data even after
shell quoting. Keep trusted instructions separate, bound the data, and provide
an explicit review step where the user needs to authorize the proposed action.
Delimiters alone do not prevent prompt injection. For automated analysis, expose
only the required files and tools; read-only access to the whole filesystem
still permits private-data disclosure. Allowlist the filesystem, minimize CLI
state/credentials and restrict tools separately from the model transport. If
required isolation is unavailable, fail closed or omit the affected feature.
A second phrase through the same microphone is not independent authorization
for dangerous actions; retain a local confirmation or agent permission boundary.

Evidence: [AppSignal](https://github.com/omacom/omarchy-plugin-marketplace/issues/7141#issuecomment-5722655664),
[Chezmoi Hound](https://github.com/omacom/omarchy-plugin-marketplace/issues/7526#issuecomment-5746267624),
[Jarvis](https://github.com/omacom/omarchy-plugin-marketplace/issues/5614#issuecomment-5734988047).

## Hosted credential services

Committed OAuth broker source does not establish what code runs in a mutable
shared deployment. Prefer existing user-controlled/local authentication. If a
broker is needed, substantiate the deployed-code and credential trust boundary;
do not send bearer/refresh credentials to an unverified default shared service.
See [Coinbase](https://github.com/omacom/omarchy-plugin-marketplace/issues/7520#issuecomment-5741977697).

## Privileged bootstrap

Identify the independent trust anchor before choosing an installer. A writable
checkout must not supply both the root-executed verifier and its expected hash,
commit or signing key. Inline shell strings and later root-owned copies do not
repair that initial boundary. Prefer a separately trusted package/root-owned
component; authenticate final package bytes as well as source inputs. Importing
a key from the same mutable checkout does not establish independent trust.

Evidence: [OmaNomad](https://github.com/omacom/omarchy-plugin-marketplace/issues/5371#issuecomment-5745040622),
[signing-key bootstrap](https://github.com/omacom/omarchy-plugin-marketplace/issues/5402#issuecomment-5672481038).
