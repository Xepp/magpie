from tweepy import OAuthHandler
from tweepy import Stream

from app.adapter.twitter import TwitterStreamListener


class TwitterStreamProcess:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def _get_oauth_handler(self):
        auth = OAuthHandler(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret
        )
        auth.set_access_token(
            key=self.access_token,
            secret=self.access_token_secret
        )

        return auth

    @staticmethod
    def _get_track_list():
        _track = [
            'از',
            'به',
            'با',
            'چرا',
            'که',
            'هم',
            'یه',
            'این',
            'تو'
        ]

        return _track or None

    @staticmethod
    def _get_language_list():
        _languages = [
            'fa'
        ]

        return _languages or None

    def run(self):
        stream_listener = TwitterStreamListener()
        auth = self._get_oauth_handler()
        stream = Stream(
            auth=auth,
            listener=stream_listener,
            tweet_mode='extended'
        )
        track = self._get_track_list()
        languages = self._get_language_list()

        stream.filter(
            track=track,
            languages=languages
        )

