---
name: omarchy-service-ipc
description: Build or review a process-wide Omarchy Quattro QML service and IPC contract. Use when state, polling or command execution must survive a panel closing or be shared across widgets; use QML patterns for shared implementation details, not for generic systemd services.
---

# Build an Omarchy service and IPC

Use one hosted `service` for shared state or work that survives a panel closing. Preserve the existing consumers and IPC API unless the request changes them. Read [service contract](references/service-contract.md); read [process safety](references/process-safety.md) when launching commands.

- Distinguish missing, unsupported, unauthenticated, loading, ready, empty, partial, offline and failed states when users need different actions.
- Make refresh idempotent. Bind asynchronous results to their owning request/generation so late completion cannot overwrite newer state or revive a disabled service.
- Bound polling, duration, response size, retries and error output. Stop or back off when prerequisites are absent.
- Keep credentials in the external program's store; query its status without copying or logging tokens.
- For messages, tasks or other private content crossing a process boundary, use the [stdin pattern](references/private-content.md); inspect descendant commands too.
- Put process/network/private-state operations behind narrow methods with explicit errors and cancellation. Avoid wrappers that expose arbitrary executables or destinations.
- Name IPC targets after the plugin ID. Expose small documented methods and bounded results; use the canonical shell target for shell lifecycle operations.

For external data, HTTP helpers, cancellation or mutable state, consult [reviewer boundaries](references/reviewer-boundaries.md). Verify affected ordering, failure, retry and cleanup paths against the actual code. Report any untested command or live integration.
