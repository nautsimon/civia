import datetime
import dns
import os 

from datetime import datetime as dt
from flask import Flask, Response, request
from pymongo import MongoClient

# Need to move this bc it has password. Temporariy remove for now.
client = MongoClient("mongodb+srv://ryanz:<>@cluster0.3fgry.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.forum
posts = db.post

"""
Help:
    Creates a new post.
Arguments: 
    postInfo: Dict, with fields
        locationId, String
        postId, Integer
        postText, String
        posterId, Integer
        time, String
            Must be in format %Y-%m-%d %H:%M:%S, or YYYY-mm-dd HH:MM:SS
Returns:
    -1 if an error is thrown, the id of the inserted post otherwise.
"""
def create_new_post(postInfo:dict):
    post = { "locationId": postInfo["locationId"],
             "_id": postInfo["postId"],
             "postText": postInfo["postText"],
             "posterId":  postInfo["posterId"],
             "time": postInfo["time"],
             "tags": [],
             "likes": 0,
             "likers": [],
             "dislikers": [],
             "replies": ""
    }

    try:
        posts.insert_one(post)
        return postInfo["posterId"] 
    except Exception as e:
        print(e)
        return -1

"""
Help:
    Adds a like or dislike to a post, saving the person who did so.
Arguments: 
    postId: Integer
        ID of the post
    like: Integer
        1 if like, -1 if dislike
    likeId: Integer
        ID of the user liking the post
Returns:
    None
"""
def like_or_dislike(postId:int, like:int, likerId:int):
    post = posts.find_one({"_id": postId})
    num_likes = post['likes']
    likers = post['likers']
    dislikers = post['dislikers']

    if like == 1:
        likers.append(likerId)
    elif like == -1:
        dislikers.append(likerId)

    post = posts.update_one({
        "_id": postId },
        { '$set': {
            'likes': num_likes + like,
            'likers': likers,
            'dislikers': dislikers
        }
    }, upsert=False)

"""
Help:
    Returns a [list] of all posts, queried on either the locationId, posterId, or likerId.
    Calling without arguments should be equivalent to getting all posts from the DB.
Arguments: 
    locationId: String
        Location ID of the post, if not provided will not query on location.
    posterId: Integer
        Poster ID, if not provided will not query by poster.
    likerId: Integer
        Liker ID, if not provided will not query by a user's liked posts.
    sortOn: String
        Can take values "likes", "time"
Returns:
    List of posts.
"""
def get_all_posts(locationId:str = None, posterId:int = None, likerId:int = None, tags:list = None, sort_on:str = None):
    argsDict = {}
    if locationId is not None:
        argsDict['locationId'] = locationId 
    if posterId is not None:
        argsDict['posterId'] = posterId 

    temp = []
    for post in posts.find(argsDict):
        if likerId is not None:
            if likerId in post['likers']:
                temp.append(post)
        else:
            temp.append(post)
    ret = []
    for post in temp:
        if tags is not None:
            if all(x in post['tags'] for x in tags):
                ret.append(post)
        else:
            ret.append(post)
    
    if sort_on == 'likes':
        ret = sorted(ret, key=lambda x:x['likes'], reverse=True)
    elif sort_on == 'time':
        ret = sorted(ret, key=lambda x:dt.strptime(x['time'], '%Y-%m-%d %H:%M:%S'), reverse=True)

    return ret