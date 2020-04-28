def get_tweet_type(tweet):
    if 'retweeted_status' in tweet:
        return 'retweet'
    elif 'quoted_status' in tweet:
        return 'quote'
    elif tweet.get('in_reply_to_status_id') is not None:
        return 'reply'

    return 'tweet'

