from flask import render_template
from random import randint
import pickle
from myapp import app

@app.route("/")
def main():

    j_clues = pickle.load(open("data/j_round.txt", "rb"))
    dj_clues = pickle.load(open("data/dj_round.txt", "rb"))
    j_cats = pickle.load(open("data/j_cats.txt", "rb"))
    dj_cats = pickle.load(open("data/dj_cats.txt", "rb"))
    finals = pickle.load(open("data/finals.txt", "rb"))

    def get_vars(n):

        game = randint(0, n)

        a = randint(0, 5)
        b = randint(0, 5)
        c = randint(0, 5)
        d = randint(0, 5)

        if j_cats[game][a] == None or j_clues[game][a][b][0] == None or \
            dj_cats[game][c] == None or dj_clues[game][c][d][0] == None:
            return get_vars(n)
        else:
            return a, b, c, d, game

    n = len(j_clues)
    a,b,c,d,game = get_vars(n)

    context = {"j_cat" : j_cats[game][a], "j_clue" : j_clues[game][a][b][0], \
		"j_answer" : j_clues[game][a][b][1], \
		"dj_cat" : dj_cats[game][c], "dj_clue" : dj_clues[game][c][d][0], \
                "dj_answer" : dj_clues[game][c][c][1], \
		"f_cat" : finals[game][0], "f_clue" : finals[game][1], \
		"f_answer" : finals[game][2]}  

    return render_template('base.html', **context )

