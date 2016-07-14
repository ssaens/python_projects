from html.parser import HTMLParser
import re

class CNNArticleParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.headline = ''
        self.content = []
        self.authors = []
        self.time = ''
        self.current_content = ''
        self.active_state = None
        self.prior_state = None

    def handle_starttag(self, tag, attrs):
        if tag == 'h1' and ('class', 'pg-headline') in attrs:
            self.active_state = 'headline'
        elif ('class', 'zn-body__paragraph') in attrs:
            self.active_state = 'body'
        elif tag == 'p' and ('class', 'update-time') in attrs:
            self.active_state = 'time'
        elif tag == 'span' and ('class', 'metadata__byline__author') in attrs:
            self.active_state = 'author_span'
        elif self.active_state == 'body':
            if tag == 'a':
                self.active_state = 'in_body_link'
            else:
                self.active_state = 'in_body_tag'

    def handle_endtag(self, tag):
        self.prior_state = self.active_state
        if self.active_state == 'in_body_link':
            self.active_state = 'body'
        elif self.active_state == 'in_body_tag':
            self.active_state = 'body'
        else:
            self.prior_state = self.active_state
            self.active_state = None


    def handle_data(self, data):
        if self.active_state == 'headline':
            self.headline = data
        elif self.active_state == 'time':
            self.time = data
        elif self.active_state == 'author_span':
            self.authors.append(data)
        elif self.active_state in ['body', 'in_body_tag']:
            if data:
                if self.prior_state == 'in_body_link':
                    self.content[-1] += data
                else:
                    self.content.append(data)
        elif self.active_state == 'in_body_link':
            self.content[-1] += data

    def get_head(self):
        authors = ''.join(self.authors)
        return self.headline, authors, self.time

    def get_content(self):
        return '\n\n'.join(self.content)

    def parse_authors(self, raw_text):
        m = re.compile('By (.*) .*')


class CNNHomeParser(HTMLParser):

    def __init__(self, max_headlines):
        HTMLParser.__init__(self)
        self.max_headlines = max_headlines
        self.links = []
        self.active_state = None

    def handle_starttag(self, tag, attrs):
        if tag == 'h3' and ('class', 'cd__headline') in attrs:
            self.active_state = 'headline'
        elif tag == 'a' and self.active_state == 'headline':
            for field, value in attrs:
                if field == 'href':
                    if value.startswith('/'):
                        value = 'http://www.cnn.com' + value
                    self.links.append(value)

    def handle_endtag(self, tag):
        if tag == 'h3' and self.active_state == 'headline':
            self.active_state = None
        elif tag == 'a' and self.active_state == 'headline':
            self.active_state = None

    def get_links(self):
        return self.links
