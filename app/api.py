from flask import Flask, redirect, url_for
from flask_cors import CORS, cross_origin
from comm import create_new_post, like_or_dislike, get_all_posts, get_latest_id
from datetime import date

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/newpost', methods=["POST"])
def new_post():
    latest_id = get_latest_id()
    locationId = request.form.get('locationId', None)
    postText = request.form.get('postText', None)
    posterId = request.form.get('posterId', None)
    arg_dict = {
        "locationId": locationId,
        "postId": latest_id + 1,
        "postText": postText,
        "posterId": posterId,
        "time": date.today().strftime("%Y-%m-%d %H:%M:%S")
    }
    err = create_new_post(arg_dict)
    return redirect(url_for("home.html"))

@app.route('/like/<int:postId>/<int:likerId>')
def like(postId, likerId):
    err = like_or_dislike(postId=postId, like=1, likerId=likerId)
    return redirect(request.referrer)

@app.route('/dislike/<int:postId>/<int:likerId>')
def dislike(postId, likerId):
    err = like_or_dislike(postId=postId, like=-1, likerId=likerId)
    return redirect(request.referrer)

@app.route('/getposts', methods=["GET"])
def getposts():
    locationId = request.args.get(locationId, None)
    posterId = request.args.get(posterId, None)
    likerId = request.args.get(likerId, None)
    tags = request.args.get(tags, None)
    sort_on = request.args.get(sort_on, None)

    get_all_posts(locationId=locationId, posterId=posterId, likerId=likerId, tags=tags, sort_on=sort_on)

    return redirect(request.referrer)