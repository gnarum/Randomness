#!/usr/bin/env python3
# encoding: utf-8
# Originally posted here:  https://gist.github.com/acdha/925e9ffc3d74ad59c3ea
# and here:  https://parsiya.net/blog/2020-11-15-customizing-pythons-simplehttpserver/
# Modified to reflect the value sent in the Origin header to bypass CORS restrictions
"""Use instead of `python3 -m http.server` when you need CORS"""
import sys,logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

PORT = int(sys.argv[1])

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def get_origin(self):
        parsed = urlparse(self.path)
        query_string = parsed.query
        path = parsed.path
        self.origin = self.headers.get("Origin")

    def do_GET(self):
#        logging.error(self.headers)
        SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', self.get_origin())
        self.send_header('Access-Control-Allow-Methods', 'GET POST')
        self.send_header('Access-Control-Allow-Headers', '*')
#        self.send_header('Access-Control-Allow-Credentials', 'true')
#        self.send_header('Access-Control-Expose-Headers', '*')
#        self.send_header('Access-Control-Max-Age', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(CORSRequestHandler, self).end_headers()


httpd = HTTPServer(('0.0.0.0', PORT), CORSRequestHandler)
print(f"CORS-Bypassed HTTPD Server listening on port {PORT}")
httpd.serve_forever()
