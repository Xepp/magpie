import os
from dotenv import load_dotenv
from argparse import ArgumentParser

from app.util.enumeration import SourceType
from app.process.twitter_stream_process import TwitterStreamProcess


def run_twitter():
    twitter_consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    twitter_consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    twitter_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    process = TwitterStreamProcess(
        consumer_key=twitter_consumer_key,
        consumer_secret=twitter_consumer_secret,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret
    )

    process.run()


def run_instagram():
    raise NotImplementedError


if __name__ == '__main__':
    load_dotenv()

    parser = ArgumentParser()
    parser.add_argument(
        '-s',
        '--source',
        required=True,
        choices=SourceType.list(),
        help='select source'
    )
    
    args = parser.parse_args()

    if args.source == SourceType.TWITTER.value:
        run_twitter()
    elif args.source == SourceType.INSTAGRAM.value:
        run_instagram()

