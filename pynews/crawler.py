import re
from parser import CNNArticleParser, CNNHomeParser
from urllib.request import urlopen

class Crawler:

    def __init__(self, target, params):
        self.target = target
        self.num_headlines = params['num_headlines']
        self.num_lines = params['num_chars']
        self.query = params['query']

    def crawl(self):
        try:
            crawled_news = []
            home_parser = CNNHomeParser(self.num_headlines)

            home_parser.feed(self.get_html(self.target))
            to_visit = home_parser.get_links()

            num_visited = 0
            while to_visit and num_visited < self.num_headlines:
                visited = to_visit.pop(0)
                article_parser = CNNArticleParser()
                print('*gathering from: ',visited)
                article_parser.feed(self.get_html(visited))
                headline, authors, time = article_parser.get_head()
                if headline:
                    print('\t==success==\n')
                    headline = headline.replace('\\', '')
                    content = article_parser.get_content().replace('\\', '')
                    crawled_news.append((headline, authors, time, content))
                    num_visited += 1
                else:
                    print('\t**failed**\n')
            return crawled_news
        except Exception as e:
            print(str(e))

    def get_html(self, url):
        sock = urlopen(url)
        source = str(sock.read())
        sock.close()
        return source
