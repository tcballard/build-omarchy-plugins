import importlib.util
import json
import os
import queue
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


HAS_QT = importlib.util.find_spec("PySide6") is not None
if os.environ.get("OMARCHY_REQUIRE_QT") == "1" and not HAS_QT:
    raise RuntimeError("The Qt rendering job requires PySide6-Essentials")


@unittest.skipUnless(HAS_QT, "Optional Qt fixture: install PySide6-Essentials")
class QtTextRenderingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        os.environ.setdefault("QT_QUICK_BACKEND", "software")
        from PySide6.QtGui import QGuiApplication
        cls.app = QGuiApplication.instance() or QGuiApplication([])
        cls.requests = queue.Queue()

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                cls.requests.put(self.path)
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.end_headers()
                try:
                    self.wfile.write(b'<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>')
                except BrokenPipeError:
                    pass

            def log_message(self, *_):
                pass

        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def render(self, kind, format):
        from PySide6.QtCore import QObject, QUrl
        from PySide6.QtQml import QQmlComponent, QQmlEngine
        from PySide6.QtTest import QTest
        from PySide6.QtQuick import QQuickWindow
        while not self.requests.empty():
            self.requests.get_nowait()
        payload = f'<img src="http://127.0.0.1:{self.server.server_port}/pixel">Private fixture'
        body = f'objectName: "display"; text: window.payload; textFormat: {format}; property bool literal: textFormat === Text.PlainText'
        display = f'{kind} {{ {body} }}'
        if kind == "ToolTip":
            display = f'ToolTip {{ parent: window.contentItem; visible: true; contentItem: Text {{ {body} }} }}'
        source = f'import QtQuick; import QtQuick.Controls; Window {{ id: window; visible: true; width: 600; height: 100; property string payload: {json.dumps(payload)}; {display} }}'
        engine = QQmlEngine()
        component = QQmlComponent(engine)
        component.setData(source.encode(), QUrl())
        self.assertFalse(component.errors(), component.errors())
        window = component.create()
        self.assertIsInstance(window, QQuickWindow)
        try:
            for _ in range(30):
                self.app.processEvents()
                time.sleep(0.01)
            self.assertFalse(window.grabWindow().isNull())
            item = window.findChild(QObject, "display")
            self.assertIsNotNone(item)
            self.assertEqual(item.property("text"), payload)
            return item.property("literal"), not self.requests.empty()
        finally:
            window.close()
            window.deleteLater()
            QTest.qWait(10)

    def test_plain_controls_render_without_image_requests_and_observer_detects_rich_text(self):
        _, fetched = self.render("Text", "Text.RichText")
        self.assertTrue(fetched, "The observer must detect an actual Qt image request")
        for kind in ("Text", "Label", "TextEdit", "TextArea", "ToolTip"):
            with self.subTest(kind=kind):
                format, fetched = self.render(kind, "Text.PlainText")
                self.assertTrue(format)
                self.assertFalse(fetched)


if __name__ == "__main__":
    unittest.main()
