from url import URL
import re

class Request:

    def __init__(self, raw_request):
        if raw_request:
            self.raw_request = raw_request.decode()
            self.parse()

    def parse(self):
        lines = self.raw_request.split('\r\n')
        self.content = lines[:]

        self.head = lines.pop(0)
        header = self.head.split(' ')
        self.method = header.pop(0)
        self.http_ver = header.pop()
        self.uri = URL(' '.join(header))

        headers = dict()
        for line in lines:
            match = re.match('(.*?):(.*)', line)
            if match:
                headers[match.group(1)] = match.group(2)
        self.headers = headers

    def __str__(self):
        return self.raw_request
