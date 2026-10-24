# Local helper exercise — 24 September 2026

Fixture: [helper.py](../../fixtures/2026-09-24-local-helper/helper.py)

SHA-256: `fc5d435f8f2712f6892cfbaf9a2246acb34f3db793472ec8f5fc621f6fa024f0`

Fresh agent with no conversation history; supplied only the service skill path,
fixture path and task below. No desired findings or repair plan were supplied.
The exposed agent tool did not report a concrete provider model/version; this
is one bounded exercise, not a named-model benchmark or baseline comparison.

## Task

Use omarchy-service-ipc to assess helper.py as the local helper for an Omarchy
plugin. The plugin promises highlighted text stays local unless users opt into
remote use. Give the smallest concrete correction plan and relevant verification
cases. Do not edit files, contact services or publish anything. Report checks
actually performed.

## Returned result

The agent identified unauthenticated history/API-key disclosure, wildcard CORS,
missing Host/Origin validation, deceptive `127.attacker.example` acceptance,
false-like remote opt-ins and unsupported schemes. It also noted that the file
has no outbound request or history insertion, so actual transmission/accumulation
cannot be established from it.

It proposed removing the key from responses; authenticated bounded routes;
Host/Origin validation; strict URL/IP parsing; explicit affirmative remote opt-in;
transport-level redirect/proxy controls; and bounded history/response handling.
Its verification cases covered legitimate clients as well as hostile requests,
deceptive destinations, IPv4/IPv6, false opt-ins and slow/oversized responses.

Reported execution: read the skill and relevant references; inspected all 25
fixture lines; executed only the extracted endpoint function with synthetic
environment values. Confirmed deceptive hostname, false opt-in and FTP acceptance
and IPv6 loopback rejection. No server, service, credentials or edits were used.

## Evaluation

Meets the scoped local-helper-authority criteria: applies the new guidance to the
actual fixture, identifies additional adjacent defects and distinguishes static
inspection/extracted-function probes from a live helper test. No repaired code,
end-to-end transport or Omarchy runtime pass is claimed.
