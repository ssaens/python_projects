import re
import time
import mimetypes

status_codes = {100:'100 Continue',
                101:'101 Switching Protocols',
                200:'200 OK',
                201:'201 Created',
                400:'400 Bad Request',
                403:'403 Forbidden',
                404:'404 Not Found',
                500:'500 Server Error'
                }

"""Class to used to wrap and parse an incomming request from the client/browser. Takes in
the encoded request string"""
class Request:
    def __init__(self, raw_request):
        if raw_request:
            self.raw = raw_request.decode()
            self.parse()
        else:
            raise Exception('403 BAD REQUEST')

    def parse_request(self):
        lines = self.raw.split('\r\n')
        self.head = lines.pop(0)

        header = self.head.split(' ')
        self.method = header.pop(0)
        self.http_ver = header.pop()
        self.uri = ' '.join(header)

        self.headers = dict()
        for line in lines:
            match = re.match('(.*?):(.*)', line)
            if match:
                self.headers[match.group(1)] = match.group(2)

    def __str__(self):
        return self.raw


class Response:

    def __init__(self):
        self.body = list()

    def set_code(self, code):
        self.code = code
        self.head = 'HTTP/1.1 %s\r\n' % status_codes[self.code]

    def set_body(self, filename, content):
        self.contenttype = mimetypes.guess_type(filename)

    def add_header(self, field, value):
        self.body.append(field + ': ' + value)

    def __str__(self):
        return self.head + '\r\n'.join(self.body) + '\r\n\r\n'


class URI:

    def __init__(self, uri):
        while uri.startswith('/'):
            uri = uri[1:]
        self.uri = uri
        self.parse()

    def parse(self):
        units = self.uri.split('/')
        self.token = units.pop(0)
        self.tail = units.pop()
        self.parent = '/'.join(units)
