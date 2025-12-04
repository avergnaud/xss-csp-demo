# XSS and CSP Demo

This project demonstrates a simple Cross-Site Scripting (XSS) vulnerability and how Content Security Policy (CSP) headers can prevent it.

## Project Structure

```
xss-csp-demo/demo-1
├── some-frontend/          # simple page with XSS 
├── server.py               # Python HTTP server with CSP controls
└── README.md              # This file
```

## Components

### 1. Frontend (some-frontend)
- Simple HTML page with a text input and submit button

### 2. Python HTTP Server (server.py)
- Serves the built Angular static files
- Provides two modes:
  - `--no-csp`: No CSP headers (XSS vulnerability works)
  - `--strict-csp`: Adds `Content-Security-Policy: script-src 'self'` header (blocks inline scripts)

## Prerequisites

- Python 3.x

## Running the Demo

### Demo 1: XSS Vulnerability (No CSP)

This demonstrates the XSS vulnerability working without any CSP protection.

```bash
python server.py --no-csp
```

**Expected behavior:**
1. Open browser to `http://localhost:8080`
2. Enter in the text input: `<img src=x onerror=alert('XSS')>`
3. Click "Submit"
4. **Result:** Alert box appears - XSS is successful!

### Demo 2: XSS Prevention (Strict CSP)

This demonstrates how CSP headers can block the XSS attack.

```bash
python server.py --strict-csp
```

**Expected behavior:**
1. Open browser to `http://localhost:8080`
2. Enter in the text input: `<img src=x onerror=alert('XSS')>`
3. Click "Submit"
4. **Result:** Alert does NOT appear - XSS is blocked!
5. Open browser DevTools Console - you'll see a CSP violation error:
   ```
   Refused to execute inline script because it violates the following
   Content Security Policy directive: "script-src 'self'"
   ```

## How It Works

### The Protection (CSP)

When CSP header `script-src 'self'` is set:
- Browser only allows scripts from the same origin (the server itself)
- Inline scripts (like `<script>alert('XSS')</script>`) are blocked
- The XSS attack fails even though the vulnerable code exists

### CSP Policies Explained

- `script-src 'self'`: Only allow scripts from same origin
- `script-src 'none'`: Block all scripts (very restrictive)
- `script-src 'unsafe-inline'`: Allow inline scripts (defeats CSP protection against XSS)

## License

This is a demonstration project for educational purposes.
