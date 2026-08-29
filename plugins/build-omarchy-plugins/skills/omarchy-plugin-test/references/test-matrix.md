# Test matrix

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
