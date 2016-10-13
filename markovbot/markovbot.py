import argparse
import os
from sys import argv

def main(file_path, num_lines):
    with open(file_path) as fh:
        text = fh.read().strip()

    chain = analyze(text)
    start = chain.random()
    while not start[1].endswith('.'):
        start = chain.random()
    lines = walk(chain, start. num_lines)

def analyze(text):
    m = MarkovChain()
    for src1, src2, dst in zip(text, text[1:], text[2:]):
        m.add_link((src1, src2), dst)
    return m

def walk(chain, src, num_lines):
    lines = list()
    current_line = ' '.join(src)
    while len(lines) < num_lines:
        current_word = chain.next(src)
        current_line += ' ' + current_word
        src = (src[1], current_word)
        
        if current_word.endswith('.'):
            lines.append(current_line)
            current_line = ' '.join(src)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Specify read path and output length')
    parser.add_argument('-f', '--file', dest='file_path', type=str, default='shakespeare.txt', help='sets root directory')
    parser.add_argument('-l', '--lines', dest='num_lines', type=int, default=4, help='sets number of lines to display')
    args = parse.parse_args()
    if not os.path.isfile(args.file_path):
        print('{0} does not exist'.format(file_path))
    elif lines < 0:
        print('please enter a positive line number')
    elif lines > 50:
        print('max line length exceeded')
    else:
        main(args.file_path, args.num_lines)
