import sys
import crawler as c
import os
import time

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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

def output(data):
    rows, columns = os.popen('stty size', 'r').read().split()
    separater = bcolors.OKBLUE + '-' * int(columns) + bcolors.ENDC
    ind = 1
    for headline, authors, time, content in data:
        if headline:
            print(separater)
            print('{1} {0}HEADLINE:{2} {3}'.format(bcolors.OKGREEN, ind, bcolors.ENDC, headline.strip()))
            print('AUTHOR(S): ', authors)
            print('UPDATED: ', time)
            if display_long:
                print(separater)
                print(content[:params['num_chars']].strip() + '...')
            print(separater + '\n')
            ind += 1

def wait_for_input(data):
    while True:
        print('type exit() to leave')
        raw_selection = input('Selected headline for full story: ')
        if raw_selection == 'exit()':
            print('Thanks for using pynews!')
            return
        else:
            try:
                selection = int(raw_selection) - 1
                display_selection(selection, data)
            except Exception as e:
                print('please only enter integers from 1 to {0}'.format(params['num_headlines']))
        output(data)

def display_selection(selection, data):
    article = data[selection]
    headline, authors, time, content = article
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Press \'b\' to go back\n')
    print(content)
    while True:
        action = input()
        if action == 'b':
            return


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print('pynews v. 0.01\n')
    args = sys.argv
    if len(args) > 1:
        parse_args(args[1:])
    crawler = c.Crawler(_sites[0], params)
    data = crawler.crawl()
    output(data)
    wait_for_input(data)
    sys.exit()
