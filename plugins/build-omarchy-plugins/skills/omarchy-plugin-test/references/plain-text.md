# Optional plain-text policy

```bash
python3 "<skill-dir>/scripts/check_plain_text.py" /absolute/path/to/plugin
```

The lexical check requires literal `Text.PlainText`/`TextEdit.PlainText` on
`Text`, `Label`, `TextEdit` and `TextArea`, including qualified names. It checks
nested objects separately and rejects attached tooltip text/show. Use an
explicit `ToolTip` with a plain-text `contentItem` instead. Comments and string
contents do not satisfy the check.

For intentional rich text, give the object a unique QML ID and record its
reviewed input boundary in CI:

```bash
python3 "<skill-dir>/scripts/check_plain_text.py" /absolute/path/to/plugin \
  --allow-rich-text 'About.qml:credits=Fixed bundled licence markup'
```

Exceptions apply to one file/object and fail when unused. This is an opt-in
project policy, not a marketplace rule or a QML/data-flow parser. Custom control
inheritance, JavaScript mutations and sanitizers still need review. Run qmllint
and exercise the real component with markup-looking device names, errors and
stored text. Assert literal display and zero image requests. A deliberately
rich-text control should trigger the test observer, proving it can see requests.

Checked 30 October 2026: [Bluetooth names](https://github.com/omacom/omarchy-plugin-marketplace/issues/13257#issuecomment-6503501447),
[stored account names](https://github.com/omacom/omarchy-plugin-marketplace/issues/13302#issuecomment-6508507122),
[Qt ToolTip](https://doc.qt.io/qt-6/qml-qtquick-controls-tooltip.html).
