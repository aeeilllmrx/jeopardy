from flask import Flask
app = Flask(__name__)

#from app import views

from random import randint
import pickle

@app.route("/")
def basic():
    # this would go in a view
    
    j_clues = pickle.load(open("data/j_round.txt", "rb"))
    dj_clues = pickle.load(open("data/dj_round.txt", "rb"))
    j_cats = pickle.load(open("data/j_cats.txt", "rb"))
    dj_cats = pickle.load(open("data/dj_cats.txt", "rb"))
    finals = pickle.load(open("data/finals.txt", "rb"))

    n = len(j_clues)   
    game = randint(0, n)

    def get_vars(game):
        a = randint(0, 5)
        b = randint(0, 5)
        c = randint(0, 5)
        d = randint(0, 5)
            
        if j_cats[game][a] == None or j_clues[game][a][b][0] == None or \
            dj_cats[game][c] == None or dj_clues[game][c][d][0] == None:
            get_vars()
        else:
            return a, b, c, d
    
    def reset_text(game, a, b, c, d):
            text = ""
            text = text + "Let's play Jeopardy!" + "\n\n"
            text = text + "jeopardy round!" + "\n\n"
            text = text + "category: " + j_cats[game][a] + "\n\n"
            text = text + "clue: " + j_clues[game][a][b][0] + "\n\n"
            text = text + "answer: " + j_clues[game][a][b][1] + "\n\n"
            text = text + "double jeopardy round!" + "\n\n"
            text = text + "category: " + dj_cats[game][c] + "\n\n"
            text = text + "clue: " + dj_clues[game][c][d][0] + "\n\n"
            text = text + "answer: " + dj_clues[game][a][b][1] + "\n\n"
            text = text + "final jeopardy" + "\n\n"
            text = text + "category: " + finals[game][0] + "\n\n"
            text = text + "clue: " + finals[game][1] + "\n\n"
            text = text + "answer: " + finals[game][2] + "\n\n"
            return text
    
    a, b, c, d = get_vars(game)
    t = reset_text(game, a, b, c, d)
    
    return t

if __name__ == "__main__":
    app.run()
