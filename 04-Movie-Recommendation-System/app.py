import os
import sys
import time  # Import the time module

from flask import Flask, render_template, request
from src.constant import *
from src.utils import *
from src.pipeline.pipeline import Pipeline

app = Flask(__name__)

@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        raise Exception(e, sys)

@app.route('/process', methods=['GET'])
def get_posters():
    try:
        movie_name = request.args.get('search')
        movie_genre = request.args.get('genre')
        movie_posters = start_pipeline(movie_name=movie_name, movie_genre=movie_genre)
        return render_template("index.html", movie_posters=movie_posters, movie_genre=movie_genre)
    except Exception as e:
        raise Exception(e, sys) from e

def start_pipeline(movie_name, movie_genre):
    try:
        pipeline = Pipeline(movie_name=movie_name, movie_genre=movie_genre)
        model_generation = pipeline.run_pipeline()
        posters_url_list = model_generation.posters_url_list
        return posters_url_list
    except Exception as e:
        raise Exception(e, sys) from e

if __name__=="__main__":
    app.run(host='0.0.0.0', port='5000', debug=True, use_reloader=False)
