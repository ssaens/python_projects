import sys

class RSA():

    def __init__(self, p, q, e):
        self.N = p * q
        self.__p = p
        self.__q = q
        self.e = e
        self.__d = mulinv(e, (p - 1) * (q - 1))

    @property
    def publicKey(self):
        return '({0}, {1})'.format(self.N, self.e)

    def encrypt(self, message):
        return pow(message, self.e) % self.N

    def decrypt(self, emessage):
        return pow(emessage, self.d) % self.N


sys.setrecursionlimit(1000000)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mulinv(e, t):
    g, x, y = egcd(e, t)
    if g == 1:
        return x % t
    else:
        return 'e is not coprime to totient'
