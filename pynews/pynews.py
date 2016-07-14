import sys
import crawler as c
import os

_sites = [  'http://www.cnn.com',
            ]
_tags = {   '-h' : 'displays supported tags and functions',
            '-n' : 'display number of headlines to show',
            '-s' : 'display source of headline',
            '-l' : 'number of characters to display from each headline',
            '-q' : 'search for the specified query'
        }
params = {  'num_headlines' : 10,
            'num_chars' : 400,
            'display_src' : False,
            'query' : None
        }

HTML_TEMPLATE = '/Users/Min/projects/python_projects/pynews'
MAX_HEADLINES = 50
MAX_CONTENT = 5000
display_long = True

# Takes a list of arguments and parses for tags
# returns number of headlines to display, number of lines to display,
# and whether or not to display site
def parse_args(args):
    global display_long
    for i, v in enumerate(args):
        if v == '-h':
            display_help()
        elif v == '-n':
            num_headlines = args[i+1]
            if 0 < int(num_headlines) < MAX_HEADLINES:
                params['num_headlines'] = int(num_headlines)
        elif v == '-l':
            num_lines = args[i+1]
            if type(num_lines) == int and 0 < num_lines < MAX_CONTENT:
                params['num_chars'] = num_lines
        elif v == '-s':
            parmas['display_src'] = not params['display_src']
        elif v == '-q':
            query = args[i+1]
            if type(query) == str:
                params['query'] = query
        elif v == '-c':
            display_long = False

def display_help():
    help_text = ''
    for tag, desc in _tags.items():
        help_text += '\t{0}: {1}\n'.format(tag, desc)
    print(help_text)

def output(content):
    print(content)


if __name__ == '__main__':
    args = sys.argv
    rows, columns = os.popen('stty size', 'r').read().split()
    if len(args) > 1:
        parse_args(args[1:])
    crawler = c.Crawler(_sites[0], params)
    data = crawler.crawl()
    separater = '-' * int(columns)
    ind = 1
    for headline, authors, time, content in data:
        if headline:
            print(separater)
            print(ind, 'HEADLINE:', headline)
            print('BY: ', authors)
            print('UPDATED: ', time)
            if display_long:
                print(separater)
                print(content[:400].strip() + '...')
            print(separater + '\n')
            ind += 1
