import random

class MarkovBot:

    def __init__(self):
        self.chain = dict()

    def feed_file(self, file_path):
        with open(file_path) as fh:
            self.feed_str(fh.read())

    def feed_str(self, string):
        tokens = string.split()
        for i in range(len(tokens) - 2):
            a, b = tokens[i], tokens[i + 1]
            c = tokens[i + 2]
            if (a, b) in self.chain:
                self.chain[(a, b)].append(c)
            else:
                self.chain[(a, b)] = [c]

    def out(self, l):
        start = random.choice(list(self.chain.keys()))
        out = start[0] + ' ' + start[1]
        for i in range(l):
            nxt = random.choice(self.chain[start])
            out += ' ' + nxt
            start = (start[1], nxt)
        return out

    def reset(self):
        self.chain = dict();
