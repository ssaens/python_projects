#!/Users/Min/anaconda3/bin/python

from argparse import ArgumentParser
import sys
import os
import functools

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def compare(s1, s2):
    s1 = s1[1]
    s2 = s2[1]
    if os.path.isfile(s1) and os.path.isdir(s2):
        return -1
    elif os.path.isfile(s2) and os.path.isdir(s1):
        return 1
    elif s1.lower() < s2.lower():
        return -1
    elif s2.lower() < s1.lower():
        return 1
    else:
        return 0

def trace(directory, tabs, order, list_size, depth, color):
    items = os.listdir(directory)
    fullpaths = [os.path.join(directory, item) for item in items]
    to_iter = zip(items, fullpaths)
    if order:
        to_iter = sorted(to_iter, key=functools.cmp_to_key(compare))
    for item, fullpath in to_iter:
        if item[0] != '.':
            space = '   ' * tabs
            if os.path.isdir(fullpath):
                if color:
                    print('{0}+- {1}{2}{3}'.format(space, bcolors.OKBLUE, item, bcolors.ENDC))
                else:
                    print('{0}+- {1}'.format(space, item))
                if depth > 0:
                    trace(fullpath, tabs + 1, order, list_size, depth - 1, color)
            else:
                if list_size:
                    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fullpath)
                    item = '[{0}] {1}'.format(size, item)
                print('{0}|-- {1}'.format(space, item))


if __name__ == '__main__':

    parser = ArgumentParser(description='Lists files and directories in tree structure')
    parser.add_argument('-o', '--order', dest='order', default=False, action='store_true', help='outputs by files first')
    parser.add_argument('-s', '--filesize', dest='show_sizes', default=False, action='store_true', help='display file sizes in bytes')
    parser.add_argument('-r', '--root', dest='root', type=str, default=os.getcwd(), help='sets root directory')
    parser.add_argument('-d', '--depth', dest='depth', type=int, default=50, help='sets max recursive depth to display')
    parser.add_argument('-c', '--color', dest='color', default=True, action='store_false', help='turns off colored directories')
    args = parser.parse_args()

    if os.path.isdir(args.root):
        trace(args.root, 0, args.order, args.show_sizes, args.depth, args.color)
    else:
        print('{0} is not a valid directory'.format(args.root))
