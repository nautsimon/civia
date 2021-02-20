from flask import Flask, redirect, url_for
from flask_cors import CORS, cross_origin
from .comm import create_new_post, like_or_dislike, get_all_posts

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route('')
# def new_post():
    