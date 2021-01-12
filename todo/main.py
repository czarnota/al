#!/usr/bin/env python

import http.server

class Handler(http.server.BaseHTTPRequestHandler):
    output = "foo"
    def do_GET(self):
        self.wfile.write(self.path.encode("utf-8"));
        self.wfile.write(self.output.encode("utf-8"));

def main():
    address = ('', 8000)
    server = http.server.HTTPServer(address, Handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
