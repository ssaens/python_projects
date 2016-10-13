from sys import argv
import random

class MarkovChain:
    def __init__(self):
        self.nodes = dict()

    def add_link(self, val, link):
        if val in self.nodes:
            self.nodes[val].append(link)
        else:
            self.nodes[val] = [link]

    def random(self):
        return random.choice(list(self.nodes))

    def next(self, start):
        return random.choice(self.nodes[start])


if __name__ == '__main__':
    if len(argv) > 1:
        source = argv[1]
    with open(source) as fh:
        text = fh.read()
    text = text.split()

    m = MarkovChain()
    for src1, src2, dst in zip(text, text[1:], text[2:]):
        m.add_link((src1, src2), dst)
    start = m.random()
    retstr = start[0] + ' ' + start[1]
    for _ in range(40):
        new = m.next(start)
        retstr += ' ' + new
        start = (start[1], new)
    print(retstr)
