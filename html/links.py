from urllib.request import urlopen
import re
import sys
from pprint import pprint as pp

def getHtml(url):
    sock = urlopen(url)
    htmlSource = str(sock.read())
    sock.close()
    return htmlSource

def findLinks(url, regex=False):
    htmlSource = getHtml(url)
    if not regex:
        links = []
        lines = htmlSource.split('<a')
        for line in lines:
            links.append(line.split('>')[0])
    else:
        m = '(?i)<a href="(https:\/\/|http:\/\/|\/)(.+?)"\s*'
        links = re.findall(m, htmlSource)
    return links

if __name__ == '__main__':
    website = sys.argv[1]
    pp(findLinks(website, True))
