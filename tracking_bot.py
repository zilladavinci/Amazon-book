import http.server
import socketserver
import os
import time

# Amazon tracking link
AMAZON_LINK = "https://www.amazon.com/dp/B0DXLK1CYQ"

# Render assigns a port dynamically, so grab from environment
PORT = int(os.environ.get("PORT", 10000))

# Storage for visitor logs
visit_log = []

class TrackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global visit_log
        client_ip = self.client_address[0]  # Default (if no proxy)

        # Fetch headers to check if Render is forwarding real IPs
        forwarded_ip = self.headers.get("X-Forwarded-For")
        cloudflare_ip = self.headers.get("CF-Connecting-IP")
        real_ip = self.headers.get("X-Real-IP")

        # Determine which IP is valid
        if forwarded_ip:
            ip_used = forwarded_ip.split(",")[0]  # First IP in list
        elif cloudflare_ip:
            ip_used = cloudflare_ip
        elif real_ip:
            ip_used = real_ip
        else:
            ip_used = client_ip  # Default fallback

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # Log all headers (for debugging)
        print(f"\n[{timestamp}] Visitor Detected:")
        print(f"  🔹 Client IP (raw): {client_ip}")
        print(f"  🔹 Forwarded IP: {forwarded_ip}")
        print(f"  🔹 Cloudflare IP: {cloudflare_ip}")
        print(f"  🔹 X-Real-IP: {real_ip}")
        print(f"  ✅ Final Logged IP: {ip_used}\n")

        # Store log
        visit_log.append(f"{timestamp} - {ip_used}")

        # Redirect user to Amazon link
        self.send_response(302)
        self.send_header('Location', AMAZON_LINK)
        self.end_headers()

# Start tracking server
try:
    with socketserver.TCPServer(("", PORT), TrackHandler) as httpd:
        print(f"🔥 Tracking bot running on port {PORT}")
        print(f"📊 Tracking visitors in real time. Logs update live.\n")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n❌ Server stopped manually.")
