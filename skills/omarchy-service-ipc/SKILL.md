---
name: omarchy-service-ipc
description: Build or review an Omarchy Quattro headless service and its IPC contract. Use for singleton polling, process execution, shared state, authenticated CLI integration, timers, retries, or `IpcHandler`; not for generic systemd services.
---

# Omarchy Service and IPC

A `service` entry point is one process-wide QML object hosted by
`omarchy-shell`. Use it for state that must be shared by widgets on multiple
monitors or must survive a panel being closed.

Read [references/service-contract.md](references/service-contract.md) for host
injection, service lookup, and IPC patterns. Read
[references/process-safety.md](references/process-safety.md) whenever the
service launches an external command.

## State machine

- Model installed, supported, authenticated, loading, ready, partial, empty,
  offline, and failed states separately when they can lead to different user
  actions.
- Make refresh idempotent and reject overlapping process chains unless
  concurrency is deliberate.
- Bound polling frequency, command duration, response size, retry rate, and
  error text. Stop or back off when prerequisites are absent.
- Keep credentials in the external CLI's credential store. Ask the CLI for
  status and data; do not read, copy, persist, or log its tokens.
- Apply optimistic updates only when rollback or a clear failure state exists.

## IPC

Name the `IpcHandler` target after the plugin ID. Expose a small stable surface
such as `refresh`, `status`, `open`, or a domain action. Return bounded,
documented results and avoid credential-bearing debug payloads. Shell-wide
lifecycle operations should go through the canonical `omarchy-shell shell`
target rather than reimplementing Quickshell socket calls.
