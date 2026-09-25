# External process safety

## Command boundary

- Prefer a purpose-built CLI with JSON output.
- Pass arguments as an array, not a constructed command string.
- Require an explicit CLI version when behavior depends on a minimum contract.
- Probe installed, supported, and authenticated separately.
- Cap stdout/stderr retained in memory and user-facing error text.
- Use a timeout or a state-machine watchdog for commands that may never exit.

## Authentication

Let the CLI own authentication and credential persistence. A shell plugin may
launch the CLI's documented login flow after a user action, then poll a bounded
status command. It should not read tokens from config files, copy them into QML
state, or print them to diagnostics.

## Privilege

Avoid `sudo` and `pkexec` in shell plugins. If machine-level privilege is
unavoidable, move it into a separately installed, root-owned helper with a
fixed command surface and treat it as machine integration requiring dedicated
security review. Never trust a PID or command from predictable shared `/tmp`
state for privileged process control.

## Remote code

Do not download and execute code at runtime. Pin build-time external Git source
to a full immutable commit and verify the checked-out revision. Prefer packaged
dependencies installed outside the shell plugin.

## Agents and credential brokers

When forwarding remote incidents or diffs to an agent, shell quoting does not
stop prompt injection. Separate bounded data from trusted instructions, restrict
the agent's actual files and tools, and preserve authorization for its actions.
A read-only bind of the whole filesystem still exposes secrets; allowlist only
required inputs and CLI state, and fail closed when isolation is unavailable.
See [Chezmoi Hound](https://github.com/omacom/omarchy-plugin-marketplace/issues/7526#issuecomment-5746267624).

Repository source cannot attest a live OAuth broker deployment. Use local or
user-controlled authentication, or substantiate the deployed credential boundary
before routing tokens through a shared service. See [Coinbase](https://github.com/omacom/omarchy-plugin-marketplace/issues/7520#issuecomment-5741977697).

For concrete producer limits, executable identity, descendant cleanup and
state-file races, consult the [marketplace reviewer boundaries](reviewer-boundaries.md) when those paths exist.
