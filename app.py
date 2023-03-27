import os

import praw
import torch
from flask import Flask
from transformers import pipeline

app = Flask(__name__)

classifier = pipeline('sentiment-analysis',
                      model='/Users/alex/Desktop/Development/distilbert-base-uncased-finetuned-sst-2-english/')

@app.route("/")
def core():
    return get_wallstreetbets_posts()

def get_wallstreetbets_posts():
    # Create a new Reddit instance
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT"),
        password=os.getenv("REDDIT_PASSWORD"),
        username=os.getenv("REDDIT_ACCOUNT")
    )

    # Retrieve the most recent posts from r/wallstreetbets
    subreddit = reddit.subreddit("wallstreetbets")
    new_posts = subreddit.new(limit=10)

    # Loop through the posts and print the title and content
    post_accumuluator = "Connected !<br><br>"
    for post in new_posts:
        post_body = (post.title + ". " + post.selftext)[0:512]
        sentiment = classifier(post_body)
        post_accumuluator += post.title + "<br>" + post.selftext + "<br><br>"
        post_accumuluator += "SENTIMENT: " + sentiment[0]['label'] + "<br>"
        post_accumuluator += "SCORE: " + '%.2f' % sentiment[0]['score'] + "<br><br>"

    return post_accumuluator

if __name__ == "__main__":
    app.run(debug=True)