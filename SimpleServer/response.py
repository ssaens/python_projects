import time

class Response:
    status_codes = {100:'100 CONTINUE', 101:'101 SWITCHING PROTOCOLS', 200:'200 OK', 201:'201 CREATED', 400:'400 BAD REQUEST', 404:'404 NOT FOUND', 403:'403 FORBIDDEN'}

    def __init__(self, status_code, content, filename):
        self.filename = filename
        self.status_code = status_code
        self.content = content
        self.contenttype = 'text/html'
        self.size = len(content)
        self.getType()
        self.header = [ 'HTTP/1.1 %s'%self.status_codes[self.status_code],
                        'Date: ' + time.strftime('%a, %d %b %Y %H:%M:%S GMT+8', time.gmtime()),
                        'Content-Type: %s'%self.contenttype,
                        'Connection: keep-alive',
                        'Content-Length: %d'%self.size,
                    ]

    def getType(self):
        extention_list = self.filename.split('.')
        if len(extention_list) > 1:
            extention = extention_list[1]
            if extention in ['html', 'txt', 'py']:
                self.contenttype = 'text/%s'%extention
            elif extention in ['gif', 'png', 'jpeg', 'ico']:
                self.contenttype = 'image/%s'%extention

    def add_header(self, field, value):
        if type(field) == str and type(value) == str:
            self.header.append('{0}: {1}'.format(field, value))
        else:
            raise Exception('field and value must be strings')

    def head(self):
        self.header.append('\n')
        head = '\n'.join(self.header)
        print(head)
        return head

    def encode(self):
        return self.head().encode() + self.content

    def __repr__(self):
        return self.head() + self.content
