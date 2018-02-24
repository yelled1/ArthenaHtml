import glob, re, html, string
from bs4 import BeautifulSoup
from Html2Json import HTMLtoJSONParser

reCURRSTR = '[A-Z][A-Z][A-Z][\s\d][,\d]'

def title_crunch(title_text):
    title_split = title_text.split(':')
    t_artist = re.sub('\(.*\)', '',title_split[0]).strip()
    t_title  = re.sub(t_artist, '', title_text).strip()
    return (t_artist, t_title)

def getCurrencies(fnm="./currencies.txt"):
    with open("currencies.txt", 'r') as fc:
        return [c.split('\t')[0] for c in fc.read().split('\n')]

def parseFile(f):
    with open(f) as fp:
        lns = fp.read()
        soup = BeautifulSoup(lns, "html.parser")
    artist, title = None, None
    artist, title = title_crunch(soup.title.text.strip())
    if not artist: raise ValueError('artist was not found by the title_crunch function!')
    return artist

if __name__ == '__main__':
    #fileDict = {}
    #soupDict = {}
    currencies = getCurrencies()
    artists = []
    htmlFiles = [f for dir in glob.glob('data/*') for f in glob.glob(dir+'/*')]
    for fnm in htmlFiles:
        artists.append(parseFile(fnm))
    print(artists)
