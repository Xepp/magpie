import os
import re
from tweepy import StreamListener

from app.adapter.elasticsearch import ElasticsearchAdapter
from app.util.helper import get_tweet_type
from app.util.enumeration import SourceType


class TwitterStreamListener(StreamListener):

    def __init__(self):
        super().__init__()
        self.es = ElasticsearchAdapter()

    def on_status(self, status):
        tweet = getattr(status, '_json')

        tweet_type = get_tweet_type(tweet)

        if tweet_type in ['tweet', 'reply']:
            content = tweet.get('extended_tweet', {}).get('full_text', tweet.get('text', ''))
            content = self._normalize(content)
            tweet_id = tweet.get('id')

            elastic_id = f'twitter://{tweet_id}'

            res = self.es.insert_doc(
                index=os.getenv('ELASTIC_INDEX'),
                elastic_id=elastic_id,
                source=SourceType.TWITTER.value,
                content=content
            )

            result = res.get('result')
            print(f'{result} {elastic_id}')

    @staticmethod
    def _normalize(text):
        return re.sub(r"(?:\@|https?\://)\S+", "", text).strip()

