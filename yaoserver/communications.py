import time
import re
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
            raise Exception('Empty Request String')

    def parse(self):
        lines = self.raw.split('\r\n')
        self.head = lines.pop(0)

        header = self.head.split(' ')
        self.method = header[0]
        self.http_ver = header[-1]
        self.uri = header[1].replace('%20', ' ')
        while self.uri.startswith('/'):
            self.uri = self.uri[1:]

        self.headers = dict()
        for line in lines:
            match = re.match('(.*?):(.*)', line)
            if match:
                self.headers[match.group(1)] = match.group(2)

    def __str__(self):
        return self.head


class Response:

    def __init__(self):
        self.headers = list()
        self.header = 'HTTP/1.1 200 OK\r\n'
        self.body = ''

    def set_code(self, code):
        self.code = code
        self.header = 'HTTP/1.1 %s\r\n' % status_codes[self.code]

    def set_body(self, filename, content):
        self.add_header('Content Type', mimetypes.guess_type(filename)[0])
        self.add_header('Content Length', len(content))
        self.body = content

    def add_header(self, field, value):
        self.headers.append('{0}: {1}'.format(field, value))

    def clear(self):
        self.headers = list()
        self.body = ''

    def encode(self):
        self.head = self.header + '\r\n'.join(self.headers) + '\r\n\r\n'
        if type(self.body) == bytes:
            response = self.head.encode() + self.body + '\r\n'.encode('UTF-8')
        else:
            response = (self.head + self.body + '\r\n').encode('UTF-8')
        return response

    def __str__(self):
        return self.header


def uri(pattern, handler):
    pattern = re.compile(pattern + '(.*)')
    def match_uri(uri, req, res):
        match = pattern.match(uri)
        if match:
            tail = match.group(1)
            handler(tail, req, res)
            return True
        return False
    return match_uri
