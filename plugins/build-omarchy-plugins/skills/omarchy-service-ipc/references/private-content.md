# Private content across processes

Treat messages, tasks, notification text and filenames as private, not only
credentials. Use fixed argv and bounded JSON on stdin; keep payloads out of
logs, environment variables and every descendant's argv. Use native filesystem
calls instead of forwarding a private filename to `mv` or `chmod`.

For a one-shot Quickshell `Process` with a fixed helper command:

```qml
stdinEnabled: true
onStarted: {
    write(pendingJson)
    pendingJson = ""
    stdinEnabled = false
}
```

Before each launch, reject overlapping requests, bound the UTF-8 JSON to 16 KiB
and reset `stdinEnabled = true`. A watchdog must stop a stalled helper; clear
pending content on failure/disable. Keep private storage at `0700`/`0600`,
including existing files. Use native session D-Bus for private notifications.

The copyable [reader](../assets/private-request/read_request.py) accepts only
`{"text": "…"}` and rejects oversized/malformed input without echoing it.
Call `read_request(sys.stdin.buffer)` inside the helper's error handler, then
invoke the specific domain operation. It provides input validation, not storage,
authentication, timeouts or process supervision. Do not build a generic command
runner around it.

Test Unicode and markup-looking text, overflow, malformed JSON, repeated sends,
cancel/start failure, and the entire process tree's command lines. On the real
host, verify no payload appears in diagnostics or notifications unexpectedly.

Checked 30 October 2026: [ArchyWidgets](https://github.com/omacom/omarchy-plugin-marketplace/issues/13129#issuecomment-6474345255),
[Omail's downstream filename leak](https://github.com/omacom/omarchy-plugin-marketplace/issues/13269#issuecomment-6504607813),
[Quickshell Process](https://quickshell.org/docs/v0.2.1/types/Quickshell.Io/Process/).
