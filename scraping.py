
from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
import pickle
import re

def get_info(url):

    sock = urlopen(url)
    lines = sock.read()
    sock.close()
    soup = bs(str(lines))

    return soup

def get_jclue(soup, clue, level):

    try:
        return soup.find(id = 'clue_J_{0}_{1}'.format(clue, level)).get_text()
    except AttributeError:
        return None

def get_djclue(soup, clue, level):

    try:
        return soup.find(id = 'clue_DJ_{0}_{1}'.format(clue, level)).get_text()
    except AttributeError:
        return None

def get_janswer(soup, clue, level):

    try:
        result = soup.find("div", {"onclick":"togglestick('clue_J_{0}_{1}_stuck')".format(clue, level)})
        res = result.prettify().encode("utf-8")
        start = re.search(r'correct_response&quot;&gt;', res).end()
        end = re.search(r'&lt;/em&gt;&lt;br', res).start()
        return res[start : end]
    except AttributeError:
        return None

def get_djanswer(soup, clue, level):

    try:
        result = soup.find("div", {"onclick":"togglestick('clue_DJ_{0}_{1}_stuck')".format(clue, level)})
        res = result.prettify().encode("utf-8")
        start = re.search(r'correct_response&quot;&gt;', res).end()
        end = re.search(r'&lt;/em&gt;&lt;br', res).start()
        return res[start : end]
    except AttributeError:
        return None

def get_finalclue(soup):

    try:
        return soup.find(id = 'clue_FJ').get_text()
    except AttributeError:
        return None

def get_finalanswer(soup):

    try:
        result = soup.find("div", {"onclick":"togglestick('clue_FJ_stuck')"})
        res = result.prettify().encode("utf-8")
        start = re.search(r'correct_response', res).end()
        try:
            end = re.search(r'&lt;/i&gt;', res).start()
        except AttributeError:
            end = re.search(r'&lt;/em&gt;', res).start()
        return res[start + 11: end]
    except AttributeError:
        return None

def get_cats(soup):

    catsoup = soup.find_all("td", {"class":"category_name"})
    cats = [catsoup[i].get_text() for i in range(len(catsoup))]
    jcats = cats[:6]; djcats = cats[6:12]; fcat = cats[12]
    return jcats, djcats, fcat

def extract(soup):

    j_round = [[[] for i in range(6)] for j in range(6)]
    dj_round = [[[] for i in range(6)] for j in range(6)]

    for i in range(1,7):
        for j in range(1,7):
            j_round[i-1][j-1] = [get_jclue(soup, i, j), get_janswer(soup, i, j)]
            dj_round[i-1][j-1] = [get_djclue(soup, i, j), get_djanswer(soup, i, j)]

    jcats, djcats, fcat = get_cats(soup)

    final = [fcat, get_finalclue(soup), get_finalanswer(soup)]

    return j_round, dj_round, final, jcats, djcats


def save(j, dj, final, jc, djc):

    pickle.dump(j, open("j_round.txt", "wb"))
    pickle.dump(dj, open("dj_round.txt", "wb"))
    pickle.dump(final, open("finals.txt", "wb"))
    pickle.dump(jc, open("j_cats.txt", "wb"))
    pickle.dump(djc, open("dj_cats.txt", "wb"))

urls = ["http://www.j-archive.com/showgame.php?game_id=" + str(i) for i in xrange(1, 100)]

j = []; dj = []; final = []
jc = []; djc = []

for i, u in enumerate(urls):
    print i, u
    soup = get_info(u)
    j_round, dj_round, final_round, jcats, djcats = extract(soup)
    j.append(j_round)
    dj.append(dj_round)
    final.append(final_round)
    jc.append(jcats)
    djc.append(djcats)

save(j, dj, final, jc, djc)


