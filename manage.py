if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    from argparse import ArgumentParser


    load_dotenv()
    parser = ArgumentParser()
    parser.add_argument(
        '-t',
        '--twitter',
        action='store_true',
        help='gather twitter in stream mode'
    )
    args = parser.parse_args()

    if args.twitter:
        from app.process.twitter_stream_process import TwitterStreamProcess


        twitter_consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
        twitter_consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        twitter_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        twitter_stream_process = TwitterStreamProcess(
            consumer_key=twitter_consumer_key,
            consumer_secret=twitter_consumer_secret,
            access_token=twitter_access_token,
            access_token_secret=twitter_access_token_secret
        )
        twitter_stream_process.run()

