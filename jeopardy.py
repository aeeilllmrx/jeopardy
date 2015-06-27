# code to scrape jeopardy games
# cmd: scrapy crawl jeopardy -o games.json (or .csv)

import scrapy
from bs4 import BeautifulSoup
#import requests


class Game(scrapy.Item):
    title = scrapy.Field()
    contestants = scrapy.Field()
    clues = scrapy.Field()
    final = scrapy.Field()
    categories = scrapy.Field()

class JeopardyGames(scrapy.Spider):
    name = 'jeopardy'

    start_urls = [
        "http://www.j-archive.com/showgame.php?game_id=4770",
        "http://www.j-archive.com/showgame.php?game_id=4771",
        "http://www.j-archive.com/showgame.php?game_id=4772"
    ]

    # loop later

    def parse(self, response):
       
        game = Game()
        # first turn html page into soup
        soup = BeautifulSoup(response.body)
        soup.prettify()
 
        # title
        title = soup.title.get_text()
        game['title'] = title
        
        # contestants
        c1 = soup.p.get_text()
        c2 = soup.p.next_sibling.next_sibling.get_text()
        c3 = soup.p.next_sibling.next_sibling.next_sibling.next_sibling.get_text()
        
        game['contestants'] = [c1,c2,c3]

        # clues
        # soon to include answers
        clues = []
        for i in range(1,7):
                for j in range(1,7):
                    try:
                        clues.append(soup.find(id = 'clue_J_' + str(i) + '_' + str(j)).get_text())
                        clues.append(soup.find(id = 'clue_DJ_' + str(i) + '_' + str(j)).get_text())
                    except AttributeError:
                        continue
                        
        game['clues'] = clues

        # categories
        cats = soup.find_all("td", class_="category_name")
        newsoup = BeautifulSoup(str(cats))
        game['categories'] = newsoup.get_text()

        # final
        final = soup.find(id = 'clue_FJ').get_text()
        game['final'] = final

        yield game
