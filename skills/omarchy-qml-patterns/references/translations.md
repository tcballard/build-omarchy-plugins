# Plugin-owned translations

Reviewed against Quattro `cce8b1c971df64a7610b818ff8819e4bea04584a` on 17 October 2026. Check the installed host for `Commons.Translations` before adopting it; do not silently raise an existing plugin's supported minimum version.

Ship flat JSON catalogs beside the QML in `i18n/`. Start with `en.json`; add languages incrementally using codes from `$OMARCHY_PATH/default/i18n/locales.json`.

```qml
import QtQuick
import qs.Commons as Commons

Item {
  property int count: 0
  Commons.Translations { id: strings; directory: Qt.resolvedUrl("i18n") }
  Text {
    textFormat: Text.PlainText
    color: Commons.Color.foreground
    text: strings.tn("panel.items", count).arg(Commons.I18n.formatNumber(count))
  }
}
```

```json
{
  "panel.title": "Items",
  "panel.items": { "one": "%1 item", "other": "%1 items" }
}
```

- Use `strings.t()` for plugin text and `strings.tn(key, count)` for counted strings. Do not depend on built-in Omarchy catalog keys; they may change independently.
- Keep whole sentences with `%1` placeholders and `.arg()`, rather than concatenating translated fragments. Use each language's CLDR plural forms; `one` and `other` are English's forms, not a universal pair.
- Missing strings fall back from regional to base language, then English, then key. Missing catalogs do not require downloading translations.
- Keep translation calls in bindings so language switching updates visible text without restart. Event-time text must be rebuilt when the language changes.
- Format numbers with `Commons.I18n.formatNumber`; format dates with `Qt.locale(Commons.I18n.formatLocale)` so they follow the current selection.
- `KeyboardPanel` and `PopupCard` provide mirroring. Explicit positions must respect `LayoutMirroring.enabled`; directional glyphs follow `Commons.I18n.rightToLeft`, and Left/Right navigation uses `Util.readingKey(event)` (with the unqualified Commons import for `Util`).
- Keep brands, units, keyboard names and diagnostic logs unchanged where appropriate.

Verify English and missing-key fallback, regional fallback, counted strings, live language switching and RTL layout/navigation. Portable catalog checks are not evidence of actual live language switching.

Sources: [plugin guide](https://github.com/omacom/omarchy/blob/cce8b1c971df64a7610b818ff8819e4bea04584a/default/agents/skills/omarchy/plugins.md), [Translations.qml](https://github.com/omacom/omarchy/blob/cce8b1c971df64a7610b818ff8819e4bea04584a/shell/Commons/Translations.qml).
