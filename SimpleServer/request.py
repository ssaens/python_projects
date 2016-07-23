import re

class Request:

    def __init__(self, raw_request):
        if raw_request:
            self.raw_request = raw_request.decode()
            self.parse()

    def parse(self):
        lines = self.raw_request.split('\r\n')
        request_line = lines.pop(0).split(' ')
        self.method = request_line[0]
        self.uri = request_line[1]
        self.http_ver = request_line[2]
        headers = dict()
        for line in lines:
            match = re.match('(.*?):(.*)', line)
            if match:
                headers[match.group(1)] = match.group(2)
        self.headers = headers

    def __str__(self):
        return self.raw_request
