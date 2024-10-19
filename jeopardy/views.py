from flask import render_template
from random import randint
import pickle
from jeopardy import app


def load_pickle(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f, encoding="utf-8")


@app.route("/")
def main():

    j_clues = load_pickle("data/j_round.pkl")
    dj_clues = load_pickle("data/dj_round.pkl")
    j_cats = load_pickle("data/j_cats.pkl")
    dj_cats = load_pickle("data/dj_cats.pkl")
    finals = load_pickle("data/finals.pkl")

    def get_vars(n):

        game = randint(0, n)

        a = randint(0, 5)
        b = randint(0, 5)
        c = randint(0, 5)
        d = randint(0, 5)

        if (
            j_cats[game][a] == None
            or j_clues[game][a][b][0] == None
            or dj_cats[game][c] == None
            or dj_clues[game][c][d][0] == None
        ):
            return get_vars(n)
        else:
            return a, b, c, d, game

    n = len(j_clues)
    a, b, c, d, game = get_vars(n)

    trebek_image = randint(1, 54)

    context = {
        "j_cat": j_cats[game][a],
        "j_clue": j_clues[game][a][b][0],
        "j_answer": j_clues[game][a][b][1],
        "dj_cat": dj_cats[game][c],
        "dj_clue": dj_clues[game][c][d][0],
        "dj_answer": dj_clues[game][c][c][1],
        "f_cat": finals[game][0],
        "f_clue": finals[game][1],
        "f_answer": finals[game][2],
        "image": trebek_image,
    }

    return render_template("base.html", **context)
