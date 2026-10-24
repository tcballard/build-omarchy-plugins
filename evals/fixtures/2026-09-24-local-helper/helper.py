from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import os

history = []
api_key = os.environ.get('FICTIONAL_API_KEY', '')

def model_endpoint():
    endpoint = os.environ.get('MODEL_HOST', 'http://127.0.0.1:11434')
    host = urlparse(endpoint).hostname or ''
    if not host.startswith('127.') and not os.environ.get('ALLOW_REMOTE'):
        raise ValueError('remote disabled')
    return endpoint

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({'history': history, 'key': api_key}).encode()
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    HTTPServer(('127.0.0.1', 8766), Handler).serve_forever()
