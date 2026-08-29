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
