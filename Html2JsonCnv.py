import glob, re, html, string
from bs4 import BeautifulSoup
from Html2Json import HTMLtoJSONParser

reCURRSTR = '[A-Z][A-Z][A-Z][\s\d][,\d]'

def title_crunch(title_text):
    title_split = title_text.split(':')
    t_artist = re.sub('\(.*\)', '',title_split[0]).strip()
    t_title  = re.sub(t_artist, '', title_text).strip()
    if t_title[:2] == ': ':
        t_title = t_title[2:]
    return (t_artist, t_title)

def getCurrencies(fnm="./currencies.txt"):
    with open("currencies.txt", 'r') as fc:
        return [c.split('\t')[0] for c in fc.read().split('\n')]

def parseFile(f):
    artist, title, price = None, None, None
    with open(f) as fp:
        lns = fp.read()
        soup = BeautifulSoup(lns, "html.parser")
        div = [tg.text for tg in soup.findAll('div')]
        price  = [ d for d in div if re.match(reCURRSTR, d) != None][0]
    artist, title = title_crunch(soup.title.text.strip())
    if not artist: raise ValueError('artist was not found by the title_crunch function!')
    return artist, title, price

if __name__ == '__main__':
    #fileDict = {}
    #soupDict = {}
    currencies = getCurrencies()
    jsonList = []
    htmlFiles = [f for dir in glob.glob('data/*') for f in glob.glob(dir+'/*')]
    for fnm in htmlFiles:
        artist_name, title_work, prc = (parseFile(fnm))
        artists = [x['artist'] for x in jsonList]
        if artist_name not in artists:
            jsonList.append({ 'artist': artist_name, 'works': [{'title': title_work, 'price': prc}] })
        else:
            jsonList[artists.index(artist_name)]['works'].append({'title': title_work, 'price': prc})
    for j in jsonList: print(j)


[x['artist'] for x in jsonList]

jsonList
