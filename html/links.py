from urllib.request import urlopen
import re

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
        m = '(?i)<a([^>]+)>(.+?)</a>'
        links = re.findall(m, htmlSource)
    return links
