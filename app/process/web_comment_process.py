import os
import time

from app.adapter.elasticsearch import ElasticsearchAdapter
from app.adapter.web import KhabarFooriAdapter
from app.util.enumeration import SourceType
from app.util.helper import get_news_id


class KhabarFooriCommentProcess:

    def __init__(self):
        self.web_adapter = KhabarFooriAdapter()
        self.es_adapter = ElasticsearchAdapter()

    def run(self, url):
        comments = self.web_adapter.get_page_comments(url)
        news_id = get_news_id(url)

        for comment in comments:
            author = comment.get('author')
            date = comment.get('date')
            content = comment.get('text')
            elastic_id = f'web://{news_id}/{author}/{date}'

            res = self.es_adapter.insert_doc(
                index=os.getenv('ELASTIC_INDEX'),
                elastic_id=elastic_id,
                source=SourceType.WEB.value,
                content=content
            )

            result = res.get('result')
            print(f'{result} {elastic_id}')

