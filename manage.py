import os
from dotenv import load_dotenv
from argparse import ArgumentParser

from app.util.enumeration import SourceType
from app.process.twitter_stream_process import TwitterStreamProcess
from app.process.instagram_comment_process import InstagramCommentProcess
from app.process.web_comment_process import KhabarFooriCommentProcess


def run_web_comment(args):
    url = args.url

    process = KhabarFooriCommentProcess()

    process.run(url)


def run_twitter_stream(args):
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


def run_instagram_comment(args):
    shortcode = args.shortcode

    process = InstagramCommentProcess()

    process.run(shortcode)


if __name__ == '__main__':
    load_dotenv()

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='source')

    parser_twitter = subparsers.add_parser('twitter')
    parser_twitter.set_defaults(func=run_twitter_stream)

    parser_instagram = subparsers.add_parser('instagram')
    parser_instagram.add_argument(
        '-s',
        '--shortcode',
        required=True,
        help='instagram media shortcode'
    )
    parser_instagram.set_defaults(func=run_instagram_comment)

    parser_web = subparsers.add_parser('web')
    parser_web.add_argument(
        '-u',
        '--url',
        required=True,
        help='web (Khabar Foori) url'
    )
    parser_web.set_defaults(func=run_web_comment)

    args = parser.parse_args()
    args.func(args)

