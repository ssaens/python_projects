from sys import argv
import random
import argparse

class MarkovChain:
    def __init__(self):
        self.nodes = dict()

    def add_link(self, val, link):
        if val in self.nodes:
            self.nodes[val][link] += 1
        else:
            self.nodes[val] = {link : 1}

    def get_rand_start(self):
        return random.choice(list(self.nodes))

    def get_next(self, start):
        #return random.choice(self.nodes[start])
        node_total = sum([freq for link, freq in self.nodes[src]])
        if node_total = 0:
            return None
        selection = random.randint(0, node_total - 1)
        lower = 0
        for link, freq in self.nodes[src]:

class Node:

    def __init__(self, val):
        self.val = val
        self.out_deg = 0
        self.links = dict()

    def add_link(self, link):
        if link in self.links:
            self.links[link] += 1
        else:
            self.links[link] = 1

if __name__ == '__main__':
    if len(argv) > 1:
        source = argv[1]
    with open(source) as fh:
        text = fh.read()
    text = text.split()

    m = MarkovChain()
    for src1, src2, dst in zip(text, text[1:], text[2:]):
        m.add_link((src1, src2), dst)
    start = m.get_rand_start()
    retstr = start[0] + ' ' + start[1]
    for _ in range(40):
        new = m.get_next(start)
        retstr += ' ' + new
        start = (start[1], new)
    print(retstr)
