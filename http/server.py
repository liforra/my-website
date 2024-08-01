import http.server
import socketserver

PORT = 80
LOG_FILE = "ip_log.txt"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        super().log_message(format, *args)
        ip = self.client_address[0]
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{ip}\n")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
