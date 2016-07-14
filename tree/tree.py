import sys
import os
import functools
from argparse import ArgumentParser

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

def trace(directory, tabs, sort, list_size):
    items = os.listdir(directory)
    fullpaths = [os.path.join(directory, item) for item in items]
    zipped = zip(items, fullpaths)
    if sort:
        to_iter = sorted(zipped, key=functools.cmp_to_key(compare))
    else:
        to_iter = zipped
    for item, fullpath in to_iter:
        if item[0] != '.':
            space = '    ' * tabs
            if os.path.isdir(fullpath):
                print('{0}+ {1}{2}{3}'.format(space, bcolors.OKBLUE, item, bcolors.ENDC))
                trace(fullpath, tabs + 1, sort, list_size)
            else:
                if list_size:
                    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fullpath)
                    item += ' %d bytes'%size
                print('{0}|-{1}'.format(space, item))


if __name__ == '__main__':

    parser = ArgumentParser(description='Lists files and directories in tree structure')
    parser.add_argument('-s', '--sort', dest='sort', default=False, action='store_true', help='sorts the output')
    parser.add_argument('-l', '--filesize', dest='show_sizes', default=False, action='store_true', help='display file sizes')
    parser.add_argument('-d', '--directory', dest='directory', type=str, help='sets root directory')
    args = parser.parse_args()

    directory = os.getcwd()
    if args.directory:
        directory = args.directory

    if os.path.isdir(directory):
        trace(directory, 0, args.sort, args.show_sizes)
    else:
        print('{0} is not a valid directory')
