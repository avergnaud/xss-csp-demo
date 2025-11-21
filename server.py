#!/usr/bin/env python3
import sys
import os;
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class CSPHandler(SimpleHTTPRequestHandler):
    csp_mode = None

    def end_headers(self):
        if self.csp_mode == 'strict':
            self.send_header('Content-Security-Policy', "script-src 'self'")
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ['--no-csp', '--strict-csp']:
        print("Usage: python server.py [--no-csp|--strict-csp]")
        sys.exit(1)

    csp_mode = 'none' if '--no-csp' in sys.argv else 'strict'
    port = 8080
    dist = 'some-frontend'

    Path(dist).exists() or sys.exit(f"Error: {dist} not found")
    os.chdir(dist)

    CSPHandler.csp_mode = csp_mode
    print(f"Server: http://localhost:{port} | CSP: {csp_mode}")

    try:
        HTTPServer(('', port), CSPHandler).serve_forever()
    except KeyboardInterrupt:
        print("\nStopped")
