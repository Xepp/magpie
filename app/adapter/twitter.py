import os
from tweepy import StreamListener

from app.adapter.elasticsearch import ElasticsearchAdapter
from app.util.enumeration import SourceType
from app.util.helper import get_tweet_type
from app.util.helper import normalize_text


class TwitterStreamListener(StreamListener):

    def __init__(self):
        super().__init__()
        self.es_adapter = ElasticsearchAdapter()

    def on_status(self, status):
        tweet = getattr(status, '_json')

        tweet_type = get_tweet_type(tweet)

        if tweet_type in ['tweet', 'reply']:
            text = tweet.get('extended_tweet', {}).get('full_text', tweet.get('text', ''))
            content = normalize_text(text)
            tweet_id = tweet.get('id')

            elastic_id = f'twitter://{tweet_id}'

            res = self.es_adapter.insert_doc(
                index=os.getenv('ELASTIC_INDEX'),
                elastic_id=elastic_id,
                source=SourceType.TWITTER.value,
                content=content
            )

            result = res.get('result')
            print(f'{result} {elastic_id}')

