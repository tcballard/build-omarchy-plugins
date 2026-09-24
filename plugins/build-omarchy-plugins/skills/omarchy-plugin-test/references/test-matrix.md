# Test matrix

Select cases affected by the change during development. For a release, cover
the declared kinds and supported lifecycle; mark genuinely inapplicable states
with a reason. Missing host access is unrun evidence, not a passing result.

## Portable contract

- valid JSON object and schema version `1` as a number;
- non-empty required fields;
- globally namespaced non-reserved ID;
- unique supported kinds and required entry-point mapping;
- safe relative existing entry points;
- no symlinks outside `.git`;
- valid bar-widget placement and settings metadata;
- root README, license, install/remove instructions, and documented dependencies;
- no obvious download-to-shell, unpinned remote execution, dangerous sudoers,
  or privileged PID control from shared temporary state.

## State behavior

For data-driven plugins, cover:

- dependency missing;
- dependency present but unsupported;
- unauthenticated;
- authenticated empty result;
- success with one and many records;
- partial upstream failure;
- malformed JSON;
- non-zero exit with and without stderr;
- timeout or stalled process;
- retry and recovery;
- duplicate refresh prevention; and
- dependency removal after startup.

## Live lifecycle

- add from a clean Git checkout;
- start disabled, review, enable, and place;
- all declared kinds become visible/callable;
- horizontal and vertical bar positions;
- one and several monitors when relevant;
- QML file reload;
- shell restart;
- update with fast-forward and validation;
- disable and re-enable;
- removal and documented retained data.

## Evidence record

Record date, full plugin SHA, Omarchy version/SHA, commands, fixture identity,
environment limitations, and pass/fail status. Do not claim an unrun platform or
state.

## Integration and release regression cases

Choose cases for the implemented boundary; these are not automatic results of
static validation or mandatory work for unrelated edits. Guidance checked against
[recent marketplace review](https://github.com/omacom/omarchy-plugin-marketplace/issues/3098#issuecomment-5744992291)
on 20 September 2026:

- fixed backend source but stale downloader/default/local executable: verify
  clean install, affected-version upgrade and minimum-version rejection;
- real installer uses the transitive lock and artifact hashes, not only CI;
- image overflow, huge decoded dimensions, redirects and missing decoder: no
  unvalidated bytes reach QML;
- many valid stream events, drip-fed input and concurrent transfers: aggregate
  memory/disk budgets and absolute deadlines hold;
- hostile agent input requesting unrelated private files/actions: inspect actual
  file/tool/network exposure, and ensure missing isolation does not enable it;
- privileged bootstrap substitution: verify that trust values and final artifact
  identity come from an independent trusted component, not the writable checkout.

For each applicable case, record the production path, fixture and meaningful
result. Source inspection alone must not be reported as an executed runtime test.

## Focused regression examples — 24 September 2026

Select only cases relevant to the plugin. These are proposed runtime fixtures,
not capabilities established by static validation:

- local HTTP helper: legitimate authenticated client succeeds; missing/wrong
  credentials, hostile Host/Origin and a `127.attacker.example` outbound endpoint
  fail before disclosure or side effects;
- update tool: matching HEAD with modified, untracked or ignored loadable source
  cannot be presented as the reviewed tree; refusal preserves user changes;
- installer: unrelated launcher/service, pre-existing target directory and
  modified managed file survive a refused install/update/remove;
- slow-drip response never completing one read: absolute deadline still aborts;
  transport descendants stop before staging cleanup;
- full producer queue followed by consumer cancellation: repeated runs leave no
  blocked terminal write, open response or accumulating reader threads;
- stale/reused PID: stop does not signal another service's process;
- long pinned clipboard content: display truncation does not alter paste data;
- remote text saved and reloaded through nested QML controls: every final sink
  remains plain text and storage stays bounded;
- bar/panel button after a plugin-ID rename: the actual registered panel opens.

Record the production path and observed result, including unrun host checks.
A separate toy implementation passing these cases does not test the plugin.
