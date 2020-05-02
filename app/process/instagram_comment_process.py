import os
import time

from app.adapter.elasticsearch import ElasticsearchAdapter
from app.adapter.instagram import InstagramWebAdapter
from app.util.enumeration import SourceType
from app.util.helper import normalize_text


class InstagramCommentProcess:

    def __init__(self):
        self.ig_adapter = InstagramWebAdapter()
        self.es_adapter = ElasticsearchAdapter()

    def run(self, shortcode):
        end_cursor = None
        has_more = True

        while has_more:
            try:
                print(f'End Cursor: {end_cursor}')
                comments, end_cursor, has_more = self.ig_adapter.get_media_comments(
                    shortcode=shortcode,
                    end_cursor=end_cursor
                )

                for comment in comments:
                    comment_id = comment.get('id')
                    text = comment.get('text')
                    content = normalize_text(text)
                    elastic_id = f'instagram://{shortcode}/{comment_id}'

                    res = self.es_adapter.insert_doc(
                        index=os.getenv('ELASTIC_INDEX'),
                        elastic_id=elastic_id,
                        source=SourceType.INSTAGRAM.value,
                        content=content
                    )

                    result = res.get('result')
                    print(f'{result} {elastic_id}')

            except Exception as exc:
                if "HTTPError" not in str(exc):
                    raise exc

                print(f'Sleeping for 60 sec. {exc}')
                time.sleep(60)

