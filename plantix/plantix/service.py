"""
(!) You are not supposed to be looking at the implementation of this
    service. The real service is a REST API which sits in the cloud.

    This code is an implementation DETAIL and cannot be modified. You
    can't draw any assumptions from anything you see in this entire
    file (and if you do, they will be WRONG).
"""

import os
import json

from http.server import HTTPServer, BaseHTTPRequestHandler


ADDRESS = "0.0.0.0"
PORT = 8970


class CommunityService(BaseHTTPRequestHandler):
    """A toy implementation of the imaginary Plantix Community API.

    Do not read, rely on, modify or extend this code.
    """
    DB = json.load(open(
        os.path.join(os.path.dirname(__file__), "service.db")
    ))

    def do_GET(self):
        """GET https://plantix.net/community/experts/:uid
        """
        resource, uid = self.path.rsplit("/", 1)

        if resource != "/community/experts" or uid not in CommunityService.DB:
            self.send_error(404)
        else:
            response = CommunityService.DB[uid]

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

    def log_request(self, *a, **k):
        pass


def serve(address=ADDRESS, port=PORT):
    httpd = HTTPServer((address, port), CommunityService)
    httpd.serve_forever()


if __name__ == "__main__":
    serve()
