# Boundaries repeatedly raised in marketplace review

Derived from HANCORE-linux's public reviews in
[omacom/omarchy-plugin-marketplace](https://github.com/omacom/omarchy-plugin-marketplace/issues),
reviewed 12 September 2026. These are recurring review concerns, not a substitute
for the current marketplace contract or an assertion that every concern applies
to every plugin. Apply the relevant boundary while implementing the feature.


## Navigation

- External data and the shared shell
- Execution and lifetime
- Files, credentials and privileged helpers
- Image and aggregate limits
- Independent privileged trust
- Local HTTP and agent endpoints
- Cancellation and identity regressions
- Presentation and action fidelity

## External data and the shared shell

Set `textFormat: Text.PlainText` on text carrying remote content, window titles,
repository metadata, helper errors or other external strings. Trace through
shared controls too; formatting one parent does not secure every child sink.
Keep intentional rich text fixed or generated from explicitly trusted content.
See [review #3360](https://github.com/omacom/omarchy-plugin-marketplace/issues/3360#issuecomment-5464817134).

Enforce byte limits **while receiving**, before full reads, JSON parsing,
`StdioCollector`, `FileView`, `responseText` or temporary-file accumulation.
Truncating afterwards leaves the memory/disk exhaustion path intact. Bound
stdout and stderr separately, then fields, records, nesting and retained history.
Use a whole-operation deadline in addition to socket timeouts; drip-fed input
can otherwise keep a request alive. Test overflow, an unterminated line, stalled
input and oversized error output on the actual production read path.
See [review #1667](https://github.com/omacom/omarchy-plugin-marketplace/issues/1667#issuecomment-5451236689).

## Execution and lifetime

Use direct argv with trusted executable identities and a minimal explicit
child environment for unattended or sensitive work. Bare names, user-writable
shims, and a successful `command -v` are not proof of that identity. Fix the
interpreter too; Python isolation may be needed where inherited search paths
could load code. Do not apply these Linux runtime choices to unrelated portable
builder scripts. See [review #6292](https://github.com/omacom/omarchy-plugin-marketplace/issues/6292#issuecomment-5645360550).

Validate option-shaped values and terminate option parsing where supported.
A list of arguments prevents shell interpretation but does not prevent a tool
from treating attacker-controlled data as an option. Avoid constructing shell,
Python or configuration source from external values.

Supervise the original child and descendants through bounded termination and
reaping. Do not assume setting QML `running=false` cleans up descendants. Avoid
broad `pkill -f`, and avoid delayed signal helpers that reopen a bare numeric
PID/PGID after the original child may have exited and its ID been reused.
Use an identity-preserving supervisor appropriate to the platform. Test a
stubborn child, child descendants, cancellation and late completion. Rate-limit
public IPC, serialize state changes and bound restart/backoff attempts.
See [review #6157](https://github.com/omacom/omarchy-plugin-marketplace/issues/6157#issuecomment-5647018532).

## Files, credentials and privileged helpers

For sensitive mutable state, open from a trusted directory with retained parent
descriptors and no-follow component traversal. Verify file type, ownership,
permissions and byte bounds on the opened object. A pathname check followed by
a fresh open races; final-component `O_NOFOLLOW` alone does not protect ancestors.
Create private temporary files exclusively and unpredictably, then replace
relative to the retained parent. When sharing state with another writer, check
its revision before replacement; an unrelated plugin lock is insufficient.
See [review #6426](https://github.com/omacom/omarchy-plugin-marketplace/issues/6426#issuecomment-5646894185).

Reject `.` and `..` explicitly in basename-only fields. Validate redirects and
URL schemes at the boundary actually used, not only on the initial input.

Keep authentication with the owning CLI/key store. Never pass tokens or recovery
phrases in argv, log them, or retain arbitrary process command lines as undo
state. If a CLI cannot accept secrets safely, design the plugin around an
already-configured account. Disclosure alone does not fix exposure.
See [review #2766](https://github.com/omacom/omarchy-plugin-marketplace/issues/2766#issuecomment-5446596212).

Do not elevate a script from a user-writable checkout. A privileged helper needs
a trusted installation and immutable executable identity; a path check before
`pkexec` is insufficient. Review downloaded executable provenance separately.

## Image and aggregate limits

Reviews checked 20 September 2026 make these producer boundaries explicit.
MPRIS/API artwork is external input: avoid assigning arbitrary URLs directly to
QML `Image.source`. Fetch through a bounded helper, validate schemes/redirects,
bytes, format, decoded pixel dimensions and total duration, then expose only the
validated local artifact. If the required decoder is absent, fail closed instead
of passing unvalidated bytes through. Declare the validating dependency.
See [artwork review](https://github.com/omacom/omarchy-plugin-marketplace/issues/7180#issuecomment-5735649258).

Bound aggregate retained events/bytes and total stream duration, not just each
line or an inactivity timer. For transfers, reserve an aggregate budget across
active work, enforce conservative per-file/concurrency limits and available-disk
constraints, and clean up partials on overflow/cancellation. Test many individually
valid inputs as well as a single oversized input.
See [stream accumulation](https://github.com/omacom/omarchy-plugin-marketplace/issues/7047#issuecomment-5735500611)
and [transfer budgets](https://github.com/omacom/omarchy-plugin-marketplace/issues/6068#issuecomment-5735045519).

## Independent privileged trust

A checksum supplied by the same mutable checkout as the elevated program does
not authenticate that program. Use a separately installed trusted verifier or
package path with independently authenticated expected identities before root
executes or installs any payload. Inline `pkexec` shell strings and importing a
signing key from that checkout retain the same problem. Authenticate final
package bytes through installation, not just downloaded source.
See [bootstrap re-review](https://github.com/omacom/omarchy-plugin-marketplace/issues/5371#issuecomment-5745040622).

## Local HTTP and agent endpoints

For browser-facing local helpers, binding to loopback does not establish request
identity. Authenticate sensitive reads, mutations and paid actions; validate
allowed Host authorities and browser Origins as appropriate, and reject invalid
requests before side effects. CORS response headers alone are not authentication.
For local-only outbound endpoints, parse the URL and IP address instead of
accepting a hostname prefix such as `127.`; `127.attacker.example` is not a
loopback literal. Handle redirects and resolved destinations under the same
policy. Remote use requires the agreed explicit opt-in.
See [local API review](https://github.com/omacom/omarchy-plugin-marketplace/issues/8352#issuecomment-5819807404)
and [local-only leak](https://github.com/omacom/omarchy-plugin-marketplace/issues/8434#issuecomment-5819147536),
checked 24 September 2026. Test allowed clients, unauthenticated requests,
hostile Host/Origin values and deceptive endpoint names without real credentials.

## Cancellation and identity regressions

A deadline checked only after a blocking read returns is not a total deadline.
Test a peer that continuously trickles bytes without completing the requested
read; enforce cancellation at the operation boundary, including transport children.
On overflow or cancellation, make terminal queue writes non-blocking or bounded,
close responses on every exit and join/reap readers within a bounded wait.
Repeat cancellation with a full queue to expose retained threads and resources.
See [slow reads](https://github.com/omacom/omarchy-plugin-marketplace/issues/8371#issuecomment-5819019831),
[git children](https://github.com/omacom/omarchy-plugin-marketplace/issues/8392#issuecomment-5819774887)
and [queue shutdown](https://github.com/omacom/omarchy-plugin-marketplace/issues/5619#issuecomment-5784771145).

For stop actions, retain process identity from launch through signaling. Reading
a reused PID's current start time twice does not bind it to the original service;
a pathname check followed by numeric-PID signaling can race. Prefer a suitable
user service/cgroup or a race-free process handle and avoid elevating user-process
cleanup. See [DevWatch](https://github.com/omacom/omarchy-plugin-marketplace/issues/7927#issuecomment-5815441990)
and [Phonecam](https://github.com/omacom/omarchy-plugin-marketplace/issues/7497#issuecomment-5795173133).

## Presentation and action fidelity

Keep bounded display previews separate from canonical action data. Truncating a
clipboard row for display must not silently replace what gets pasted; reject
oversized stored input explicitly if needed. Trace remote strings through
persistence and shared child controls, bounding stored fields and setting each
external Text sink to PlainText. Verify every visible button and IPC invocation
uses the actual manifest ID, especially after a rename.
See [Clipbar](https://github.com/omacom/omarchy-plugin-marketplace/issues/8478#issuecomment-5819340291),
[persisted location](https://github.com/omacom/omarchy-plugin-marketplace/issues/8395#issuecomment-5819055337)
and [panel target](https://github.com/omacom/omarchy-plugin-marketplace/issues/8463#issuecomment-5819309888).
