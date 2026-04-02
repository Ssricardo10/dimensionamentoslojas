"""Servidor local para desenvolvimento."""

import sys
import os
import http.server
import socketserver
import webbrowser
from pathlib import Path

ROOT = Path(__file__).parent.parent
PORT = 8000

os.chdir(ROOT)

print(f"\n  🌐 http://localhost:{PORT}/web/index.html")
print(f"  Pressione Ctrl+C para encerrar\n")

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    webbrowser.open(f"http://localhost:{PORT}/web/index.html")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor encerrado.")
