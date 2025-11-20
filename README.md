# XSS and CSP Demo

This project demonstrates a simple Cross-Site Scripting (XSS) vulnerability and how Content Security Policy (CSP) headers can prevent it.

## Project Structure

```
xss-csp-demo/
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

## Setup Instructions

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

## Server Options

```bash
# Run on custom port
python server.py --no-csp --port 3000

# Specify custom dist directory
python server.py --strict-csp --dist path/to/dist

# View help
python server.py --help
```

## How It Works

### The Vulnerability

1. **User Input:** User enters malicious HTML/JavaScript
2. **Bypass Security:** The Angular component uses `bypassSecurityTrustHtml()` which tells Angular to trust the HTML
3. **Render:** The `[innerHTML]` binding renders the untrusted HTML directly into the DOM
4. **Execute:** Without CSP, the browser executes any `<script>` tags

### The Protection (CSP)

When CSP header `script-src 'self'` is set:
- Browser only allows scripts from the same origin (the server itself)
- Inline scripts (like `<script>alert('XSS')</script>`) are blocked
- The XSS attack fails even though the vulnerable code exists

## Educational Notes

### Why This Is Vulnerable

- **Never use `bypassSecurityTrustHtml()`** with untrusted user input
- Angular's built-in sanitizer would normally strip `<script>` tags
- Bypassing this protection creates an XSS vulnerability

### Defense Layers

1. **Primary Defense:** Don't bypass Angular's sanitizer
2. **Secondary Defense (CSP):** Even if code is vulnerable, CSP headers can prevent exploitation
3. **Best Practice:** Use Angular's safe bindings like `{{ }}` for text content

### CSP Policies Explained

- `script-src 'self'`: Only allow scripts from same origin
- `script-src 'none'`: Block all scripts (very restrictive)
- `script-src 'unsafe-inline'`: Allow inline scripts (defeats CSP protection against XSS)

## Testing Different Payloads

Try these different XSS payloads to see what works with/without CSP:

```html
<!-- Classic script tag -->
<script>alert('XSS')</script>

<!-- Image with onerror (also blocked by CSP) -->
<img src=x onerror=alert('XSS')>

<!-- SVG with onload (also blocked by CSP) -->
<svg onload=alert('XSS')>

<!-- Safe HTML (works in both modes) -->
<b>Bold text</b>
<span style="color: red;">Red text</span>
```

## Clean Up

To stop the server, press `Ctrl+C` in the terminal.

## Security Warning

This project is for **educational purposes only**. It demonstrates:
- How NOT to handle user input
- Why Angular's security features exist
- How CSP provides defense-in-depth

**Never deploy code that uses `bypassSecurityTrustHtml()` with user input in production!**

## License

This is a demonstration project for educational purposes.
