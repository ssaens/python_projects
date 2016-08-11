import os

class URL:

    valid_tokens = ['p', 'd', 'r']

    def __init__(self, url):
        while url.startswith('/'):
            url = url[1:]
        self.url = url
        self.parse()

    def parse(self):
        tokens = self.url.split('/')
        self.prefix = tokens.pop(0)
        if not tokens or self.prefix not in valid_tokens:
            raise Exception('bad url')
        self.resource = tokens[-1]
        self.parent = '/'.join(tokens)[:-1]

    def root_with(self, root):
        self.url = os.join(root, self.url)
        self.parse()

    def __str__(self):
        return self.url
