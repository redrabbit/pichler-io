from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import pichler

device = pichler.Pichler()

class RequestHander(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/vent-level":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            vent_level = device.datapoint_read_value(59)
            self.wfile.write(bytes(str(vent_level), "ascii"))

        elif self.path == "/outdoor-temp":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            datapoint = device.datapoint_read_value(30)
            outdoor_temp = int(str(datapoint)[1:]) / 10
            self.wfile.write(bytes(str(outdoor_temp), "ascii"))

    def do_POST(self):
        if self.path == "/vent-level":
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                level = data.get('level')
                if level is None:
                    self.send_response(400)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Missing 'level' parameter"}).encode())
                    return

                if not isinstance(level, int) or level < 0 or level > 4:
                    self.send_response(400)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Level must be an integer between 0 and 4"}).encode())
                    return

                device.setpoint_write_value(14, 0, level)

                self.send_response(200)
                self.end_headers()

            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())

if __name__ == "__main__":
    http_server = HTTPServer(("0.0.0.0", 8080), RequestHander)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    http_server.server_close()
