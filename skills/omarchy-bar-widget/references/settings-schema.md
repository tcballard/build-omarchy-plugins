# Bar-widget settings

Settings live directly on the matching entry in
`~/.config/omarchy/shell.json`. There is no nested `config` object and no deep
merge.

Manifest example:

```json
{
  "barWidget": {
    "displayName": "Example",
    "description": "Compact example status",
    "category": "Developer Tools",
    "allowMultiple": false,
    "defaultSection": "right",
    "defaults": {
      "refreshIntervalSec": 300
    },
    "schema": [
      {
        "key": "refreshIntervalSec",
        "type": "integer",
        "label": "Refresh interval (seconds)",
        "min": 60,
        "max": 3600,
        "step": 60,
        "defaultValue": 300
      }
    ]
  }
}
```

Current first-party manifests use types including `boolean`, `enum`, `integer`,
`path`, and `string`. Follow the target Omarchy source when adding a type or
field not already used by a current plugin.

Inside `BarWidget`, read through `setting("refreshIntervalSec", 300)` and clamp
again before using a value to drive timers or resource consumption. Schema
metadata improves editing but is not a security boundary.

Set `allowMultiple: true` only when every setting mutation can identify the
intended instance. Selectors that address only the plugin ID are ambiguous when
several instances exist.
