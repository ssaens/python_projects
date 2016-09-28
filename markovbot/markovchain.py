import random
from sys import argv

class MarkovChain:
    def __init__(self):
        self.nodes = dict()

    def add_link(self, val, link):
        if val in self.nodes:
            self.nodes[val].append(link)
        else:
            self.nodes[val] = [link]

    def get_rand_start(self):
        return random.choice(list(self.nodes))

    def get_next(self, start):
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
    start = m.get_rand_start()
    retstr = start[0] + ' ' + start[1]
    for _ in range(40):
        new = m.get_next(start)
        retstr += ' ' + new
        start = (start[1], new)
    print(retstr)
# class Node:
#
#     def __init__(self, val):
#         self.val = val
#         self.out_deg = 0
#         self.links = dict()
#
#     def add_link(self, node, freq):
#         self.links[node].append(node)
#
#     def get_neighbor(self):
#         choice = random.randInt(0, tot_out_freq):
#         start_range = 0
#         end_range = 0
#         for node, freq in self.links:
#             end_range += freq
#             if start_range <= choice < end_range:
#                 return node
#             start_range = end_range
