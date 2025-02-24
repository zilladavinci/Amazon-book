import http.server
import socketserver
import os
import time

# Amazon tracking link
AMAZON_LINK = "https://www.amazon.com/dp/B0DXLK1CYQ"

# Use the correct Render-assigned port
PORT = int(os.environ.get("PORT", 10000))

# Storage for visitor logs
visit_log = []

class TrackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global visit_log
        client_ip = self.client_address[0]  # Default (may be 127.0.0.1 if proxied)

        # Check for real IP from proxy headers (Render/AWS/Cloudflare)
        forwarded_ip = self.headers.get("X-Forwarded-For")
        real_ip = forwarded_ip.split(",")[0] if forwarded_ip else client_ip  # Get first IP in chain

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # Log visitor details
        visit_log.append(f"{timestamp} - {real_ip}")
        print(f"[{timestamp}] Visitor Detected:")
        print(f"  🔹 Client IP (raw): {client_ip}")
        print(f"  🔹 Forwarded IP: {forwarded_ip}")
        print(f"  🔹 Logged IP: {real_ip}")

        # Redirect user to Amazon link
        self.send_response(302)
        self.send_header('Location', AMAZON_LINK)
        self.end_headers()

# Start the local tracking server
try:
    with socketserver.TCPServer(("", PORT), TrackHandler) as httpd:
        print(f"🔥 Tracking bot running on port {PORT}")
        print(f"📊 Tracking visitors in real time. Logs update live.\n")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n❌ Server stopped manually.")
