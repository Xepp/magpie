import re
import string
import random


def get_tweet_type(tweet):
    if 'retweeted_status' in tweet:
        return 'retweet'
    elif 'quoted_status' in tweet:
        return 'quote'
    elif tweet.get('in_reply_to_status_id') is not None:
        return 'reply'

    return 'tweet'


def get_news_id(url):
    try:
        id = re.findall('detail/(.+)/', url)[0]
    except Exception:
        id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    return id


def normalize_text(text):
    return re.sub(r"(?:\@|https?\://)\S+", "", text).strip()

