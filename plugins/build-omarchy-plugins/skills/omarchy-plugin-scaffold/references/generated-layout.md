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
| Built for Omarchy \| `omarchy` |
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
