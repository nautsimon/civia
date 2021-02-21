from flask import Flask, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from comm import *
from datetime import date

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Note: Pass in time since I can't access the user's time zone here.
@app.route('/newpost', methods=["POST"])
def newpost():
    locationId = request.form.get('locationId', None)
    postText = request.form.get('postText', None)
    posterId = request.form.get('posterId', None)
    time = request.form.get('time', None)
    arg_dict = {
        "locationId": locationId,
        "postText": postText,
        "posterId": posterId,
        "time": time
    }
    err = create_new_post(arg_dict)
    return redirect(request.referrer)

@app.route('/like/<int:postId>/<int:likerId>')
def like(postId, likerId):
    err = like_or_dislike(postId=postId, like=1, likerId=likerId)
    return redirect(request.referrer)

@app.route('/dislike/<int:postId>/<int:likerId>')
def dislike(postId, likerId):
    err = like_or_dislike(postId=postId, like=-1, likerId=likerId)
    return redirect(request.referrer)

"""
The post return json structure should be as follows:

Highest level: list of posts
In each post: information, as well as list of replies
In each reply: reply text, with id

"""
@app.route('/getposts', methods=["GET"])
def getposts():
    locationId = request.args.get(locationId, None)
    posterId = request.args.get(posterId, None)
    likerId = request.args.get(likerId, None)
    tags = request.args.get(tags, None)
    sort_on = request.args.get(sort_on, None)

    posts = get_all_posts(locationId=locationId, posterId=posterId, likerId=likerId, tags=tags, sort_on=sort_on)

    for post in posts:
        replies = get_all_replies(post['replies'])
        post['replies'] = replies

    return jsonify({"posts": posts})

@app.route('/deletepost/<int:postId>')
def deletepost(postId:int):
    delete_post(postId=postId)
    return redirect(request.referrer)

@app.route('/deletereply/<int:replyId>')
def deletereply(replyId:int):
    delete_reply(replyId=replyId)
    return redirect(request.referrer)

@app.route('/addreply', methods=["POST"])
def addreply(postId:int, userId:int, replyText:str):
    add_reply(postId=postId, userId=userId, replyText=replyText)
    return redirect(request.referrer)
