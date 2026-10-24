# Design abstractions that constrain agent choices

Use for repeated process, network, storage, rendering or approval boundaries.
Prefer a small local adapter or an existing reviewed library over reimplementing
those boundaries in each feature. These are design contracts, not new Omarchy
APIs or claims that this bundle ships an implementation of every adapter.

## Select the boundary

| Boundary | Narrow caller contract | Decisions kept inside | Evidence |
| --- | --- | --- | --- |
| Network reader | Approved endpoint, request data, finite budget → bounded result or typed error | Credential origin, redirects, resolved destination, bytes, whole-operation deadline | Redirect, DNS change, overflow, slow-drip and cancellation fixtures on the actual reader |
| Process runner | Named operation and validated values → bounded result/cancel handle | Executable identity, argv, environment, concurrency, descendants and reaping | Option-shaped input, stubborn descendants, late completion, repeated cancellation |
| Private store | Schema-valid record and expected revision → saved/conflict/unavailable | Private ownership, descriptor-relative access, atomic replace, size and conflict handling | Missing versus unreadable, symlink ancestors, concurrent writer, failed write |
| Display text | External string → literal text | Plain-text rendering, presentation limits; retain separate canonical action data | Markup-looking title through every nested view; unchanged clipboard/action payload |
| Approval operation | Verified operation identity → one authorized action | Trusted recipient, displayed operation, expiry, replay and execution binding | Real requesting PID with forged operation/helper; cancellation and replay |

Expose only parameters the feature needs. Avoid a generic `run(anyCommand)` or
`request(anyUrl, anyHeaders)` escape hatch beside a supposedly constrained API.
Reuse Omarchy's `qs.Ui`/`qs.Commons` and lifecycle interfaces before wrapping them.
For process/store blocks, inspect Omakit's current API, license, copied source
and revision; accept it only if the actual boundary and dependencies fit.
Do not assume a reusable helper covers network consent or privileged identity.

## Make the chosen architecture executable

Keep one owner for each policy; UI components call a narrow service/adapter.
Enforce cheap, deterministic invariants in CI. Use the test skill's opt-in
`--deny-capability` checks for a project that deliberately excludes direct
QML/JS networking or dynamic code. This is a project rule, not marketplace policy.
Keep the adapter's runtime tests: lexical checks cannot establish data flow,
producer limits, cleanup, provenance or authorization.

Name a rule, its scope and its permitted alternative. Handle a legitimate
exception by reviewing the boundary and updating the declared policy/tests;
do not hide code from scanning or add a blanket disable. Keep domain logic
flexible; a clock does not need a network transport or privileged-operation layer.

## Assess cost and unwindability

Use two different real call sites to assess fit when available. For a new
single-use boundary, a short concrete function may be enough. Prefer explicit
errors and inspectable data over a new DSL, deep hierarchy or global registry.
Keep schemas/version changes deliberate and callers independent of implementation
internals so a bad adapter can be replaced locally.

Compare behavior and total maintenance cost, not only generated line count.
Measure prompt/context tokens, edit size, test failures and review iterations on
comparable tasks before claiming token savings. Copied code still has update and
provenance costs. Agents can make rewrites cheaper; they cannot undo leaked
credentials, destructive writes or already-issued privileged commands.
