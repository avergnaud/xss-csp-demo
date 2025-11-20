#!/usr/bin/env python3
"""
Simple HTTP server to demonstrate XSS vulnerability with CSP controls.
Serves Angular static files with configurable Content Security Policy headers.
"""

import argparse
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class CSPRequestHandler(SimpleHTTPRequestHandler):
    """Custom request handler that adds CSP headers based on configuration."""

    csp_mode = None  # Will be set from command-line arguments

    def end_headers(self):
        """Override to inject CSP header before sending response."""
        if self.csp_mode == 'strict':
            # Strict CSP that blocks inline scripts - prevents XSS
            self.send_header('Content-Security-Policy', "script-src 'self'")
        # If csp_mode is 'none', we don't add any CSP header (XSS works)

        super().end_headers()

    def log_message(self, format, *args):
        """Override to provide cleaner log messages."""
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")


def serve(port, dist_path, csp_mode):
    """Start the HTTP server with specified configuration."""

    # Change to the dist directory to serve files
    if not os.path.exists(dist_path):
        print(f"Error: Distribution directory not found: {dist_path}")
        print(f"Please build the Angular app first with: cd some-frontend && ng build")
        sys.exit(1)

    os.chdir(dist_path)

    # Set the CSP mode in the handler class
    CSPRequestHandler.csp_mode = csp_mode

    server_address = ('', port)
    httpd = HTTPServer(server_address, CSPRequestHandler)

    # Print startup information
    print("=" * 60)
    print(f"XSS/CSP Demo Server")
    print("=" * 60)
    print(f"Server running on: http://localhost:{port}")
    print(f"CSP Mode: {csp_mode.upper()}")
    if csp_mode == 'none':
        print(f"  - No CSP headers (XSS will work)")
    elif csp_mode == 'strict':
        print(f"  - CSP: script-src 'self' (XSS blocked)")
    print(f"Serving files from: {dist_path}")
    print("=" * 60)
    print(f"Press Ctrl+C to stop the server")
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()


def main():
    parser = argparse.ArgumentParser(
        description='HTTP server for XSS/CSP demonstration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python server.py --no-csp          Run without CSP (XSS works)
  python server.py --strict-csp      Run with strict CSP (XSS blocked)
  python server.py --no-csp -p 3000  Run on port 3000 without CSP
        """
    )

    # CSP mode arguments (mutually exclusive)
    csp_group = parser.add_mutually_exclusive_group(required=True)
    csp_group.add_argument(
        '--no-csp',
        action='store_true',
        help='Run without CSP headers (allows XSS)'
    )
    csp_group.add_argument(
        '--strict-csp',
        action='store_true',
        help="Run with strict CSP: script-src 'self' (blocks XSS)"
    )

    # Optional arguments
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=8080,
        help='Port to run the server on (default: 8080)'
    )
    parser.add_argument(
        '-d', '--dist',
        type=str,
        default='some-frontend',
        help='Path to the frontend files'
    )

    args = parser.parse_args()

    # Determine CSP mode
    csp_mode = 'none' if args.no_csp else 'strict'

    # Resolve dist path
    dist_path = Path(args.dist).resolve()

    serve(args.port, dist_path, csp_mode)


if __name__ == '__main__':
    main()
