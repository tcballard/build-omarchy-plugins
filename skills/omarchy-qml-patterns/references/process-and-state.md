# Process and asynchronous-state patterns

## Commands

Prefer argument arrays:

```qml
Process {
  id: statusProcess
  command: ["example-cli", "status", "--json"]
  stdout: StdioCollector {
    waitForEnd: true
    onStreamFinished: root.consumeStatus(text)
  }
}
```

Do not interpolate data into `bash -c`. If a shell is unavoidable, constrain the
script literal and quote each external value with `Util.shellQuote`.

## State discipline

- Clear old output before starting a new request.
- Keep a serial/generation number when stale completions could overwrite newer
  state.
- Prevent overlapping refreshes or explicitly queue one follow-up.
- Cap error text before storing or displaying it.
- Treat exit code, stdout parse success, and domain success as separate checks.
- Use a timer only while the prerequisite state justifies it; stop on close or
  unsupported/missing dependencies.
- Do not infer authentication from one failed data request unless the CLI gives
  an explicit authentication error.

## Storage

Use `shell.json` inline values for ordinary widget settings. Use XDG state for
durable runtime state, XDG cache for regenerable data, and the external program's
own store for credentials. Avoid predictable privileged PID files under `/tmp`;
use the owner-only `XDG_RUNTIME_DIR` for ephemeral coordination.
