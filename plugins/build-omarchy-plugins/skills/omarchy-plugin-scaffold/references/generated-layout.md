# Generated repository

The generator creates a standalone public Git repository with this baseline:

```text
plugin-name/
├── .github/workflows/test.yml
├── .omarchy-workbench.json
├── demo/fixtures/example.json
├── scripts/validate_manifest.py
├── tests/run
├── manifest.json
├── <entry-point QML files>
├── README.md
├── LICENSE
└── preview.svg
```

## Generator options

```text
--id ID                 Permanent third-party plugin ID
--name NAME             Display name
--kind KIND             Repeatable supported kind
--author NAME           Manifest and license author
--description TEXT      Manifest and README description
--version SEMVER        Initial version; default 0.1.0
--output PATH           New empty destination
--default-section SIDE  left, center, or right for bar widgets
--allow-multiple        Permit multiple configured widget instances
--no-git                Do not initialize a Git repository
```

The generator refuses:

- reserved `omarchy.*` IDs;
- non-lowercase or path-like IDs;
- unsupported or duplicate kinds;
- invalid semantic versions; and
- non-empty destinations.

## After generation

Replace sample state and copy, convert `preview.svg` to a current root preview
image, and document every real dependency. Preserve the generated manifest
mapping, lifecycle functions, test entry point, explicit install/remove
instructions, and license.

The generated validator is a portable structural check for CI. On the target
machine, `omarchy plugin validate .` remains authoritative for the installed
Omarchy revision.

The Workbench definition declares the root plugin and the exact
`["./tests/run"]` argument vector as both a portable check and a
capability-gated validation workflow. It also declares Git and Python as
required environment probes and Omarchy as optional. Plugin Workbench reads
those commands during registration but deliberately leaves them untrusted until
the user reviews the file and explicitly approves project commands and the
workflow capability.


## README badges and GitHub topics

Pair the [community badge](https://github.com/tcballard/omarchy-badges) with
consistent repository topics:

| Badge | Topics |
| --- | --- |
| Built for Omarchy | `omarchy` |
| Built for Omarchy \| Plugin | `omarchy`, `omarchy-plugin` |
| Built for Omarchy \| App | `omarchy`, `omarchy-app` |
| Built for Omarchy \| Theme | `omarchy`, `omarchy-theme` |

The Plugin category here means an Omarchy shell plugin. App covers standalone
applications and games; Theme covers Omarchy colour schemes and themes. Use
the general badge for tooling or integrations that do not fit those categories.

The scaffold produces shell plugins, so its default pair is `omarchy` and
`omarchy-plugin`. Recommend these topics alongside the README badge. When
repository metadata changes are part of the user's request, add the appropriate
topics while preserving existing relevant topics. Otherwise include the
recommendation in the handoff. A generated README does not configure GitHub
metadata: the repository owner can add topics using the gear beside About on
GitHub.

This is a community discovery convention, not a marketplace requirement or
approval signal. Keep actual compatibility and testing evidence in the README.


## Compact README badge row

Place one compact badge group directly below the project title and before the
summary. Follow the familiar CI / licence / platform badge layout:

1. CI status, when an actual workflow exists; link to that workflow and use its
   live status badge rather than a static “passing” claim.
2. Licence, matching the project's licence and linking to its licence file.
3. Built for Omarchy with the appropriate category box.
4. Omarchy version support, immediately beside identity, when the maintainer
   has declared a supported range; link to the project's Compatibility section.

Omit badges whose information is unavailable. Do not infer a support range
from the scaffold's target version or from one passing test. Record exact
versions tested, platform, date and limitations separately in Compatibility.
An extension-format label such as Chrome's Manifest V3 is not equivalent to
an operating-system support range.

Use equal displayed heights and small, consistent gaps. Use 20 px when mixing these SVGs with native GitHub CI or standard licence
badges. GitHub treats the HTML height as a maximum, so 24 px does not enlarge
an intrinsically 20 px badge. A row containing only our SVGs can use 24 px.
Preserve aspect ratios. Preserve the official icon, outlined font and category
colours. Do not stretch widths to make badges equal-sized. Keep links and alt
text on every badge. Use one paragraph with whitespace between linked images,
not a table or a separate paragraph for each badge. Allow natural wrapping on
mobile rather than forcing horizontal scrolling. Follow the title's existing
left or centre alignment.

Markdown image links work at the assets' native sizes. For mixed-height assets,
use linked HTML images with the same `height` and omit `width` so their
proportions remain intact. For example, after confirming 4.0.0+ is the project's
actual support policy:

```html
<p>
  <a href="https://github.com/tcballard/omarchy-badges"><img alt="Built for Omarchy: Plugin" height="20" src="https://raw.githubusercontent.com/tcballard/omarchy-badges/75975e5b5bf75e7ede3764bcd2950046f7abfe2c/badges/v1/omarchy-plugin.svg"></a>
  <a href="#compatibility"><img alt="Supported Omarchy versions: 4.0.0+" height="20" src="https://raw.githubusercontent.com/tcballard/omarchy-badges/dd84bb21f19caf617caa5b3c1af7ff3c6cb847c3/badges/v1/compatibility/omarchy-4.0.0-plus.svg"></a>
</p>
```

Add CI and licence links ahead of this pair only after resolving the project's
actual workflow and licence. Add the destination Compatibility heading and its
support/test notes before publishing the example. Choose the appropriate
[compatibility preset](https://github.com/tcballard/omarchy-badges/blob/7e00b3342bddefab7fece63f4806e47f4b77bf7c/COMPATIBILITY.md)
without changing an existing pinned badge's artwork. Check the rendered row at
normal size and a narrow viewport; badge layout is presentation, not evidence
of compatibility or marketplace approval.
