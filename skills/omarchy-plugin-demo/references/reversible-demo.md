# Reversible demo harness

## Preflight

- Require every external command before mutation.
- Refuse a locked session, unsupported monitor transform, missing normal shell
  config, or ambiguous existing plugin path.
- Refuse stale demo backups from a prior interrupted run.
- Capture the current workspace, shell process identity, plugin installation,
  shell config, and cursor state needed for restoration.

## Isolation

- Create runtime state with `mktemp -d` under `XDG_RUNTIME_DIR` or `/tmp`.
- Put a committed fictional CLI shim first in a demo-only `PATH`.
- Point the shim at a committed fixture and runtime write directory through
  explicit environment variables.
- After the demo shell starts, inspect its environment or IPC identity to prove
  that the fixture process—not a user's real CLI—will be invoked.
- Use a previously unused empty workspace.

## Cleanup

Install `EXIT`, `INT`, `TERM`, and `HUP` traps before the first mutation. Restore
in dependency order: configuration and plugin path, workspace/cursor, then the
normal shell. Remove temporary data only after successful restoration.

If restoration fails, print the retained backup paths and leave them intact.
Never recursively delete a broad path or a target derived only from an unset
environment variable.

## Screenshot

Wait for a machine-readable ready state over IPC. Dismiss unrelated shell
surfaces, focus the intended monitor/workspace, and capture the smallest useful
region. The community marketplace accepts a single root `preview.png`, `.jpg`,
`.jpeg`, `.webp`, or `.avif`, currently limited to 50 MB and 40 megapixels.
