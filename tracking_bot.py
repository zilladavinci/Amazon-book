import http.server
import socketserver
import time
import os

PORT = int(os.environ.get("PORT", 8080))
AMAZON_LINK = "https://www.amazon.com/dp/B0DXLK1CYQ"
visit_log = []

class TrackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global visit_log
        client_ip = self.client_address[0]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        visit_log.append(f"{timestamp} - {client_ip}")
        print(f"[{timestamp}] Visitor from {client_ip}")
        self.send_response(302)
        self.send_header('Location', AMAZON_LINK)
        self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), TrackHandler) as httpd:
        print(f"🔥 Tracking bot running on port {PORT}")
        print(f"📊 Tracking visitors live.\n")
        httpd.serve_forever()
