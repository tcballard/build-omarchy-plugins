# Architecture

StarterWidget.qml owns a per-instance, in-memory toggle. It uses the host BarWidget and WidgetButton APIs and follows the host bar orientation. The manifest declares only the implemented bar-widget kind.

No files, network requests, background processes, global configuration or installation hooks are used. Destroying the widget releases its state. Keep process-wide work in an explicit service if the feature later needs one, and document ownership and shutdown before adding it.

The starter only renders fixed symbols and fixed tooltip strings. For external text, use explicit Text.PlainText content items, including nested delegates and preview buttons. Do not rely on Qt AutoText.

Node is a development dependency for portable checks; it is not used by the runtime widget. Workbench registration and command trust remain explicit user actions.
