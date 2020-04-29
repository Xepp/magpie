from datetime import datetime
from elasticsearch import Elasticsearch

from app.vo import ElasticsearchDocVO
from app.util.enumeration import SentimentType


class ElasticsearchAdapter:

    def __init__(self):
        self.es = Elasticsearch()

    def insert_doc(self, index, elastic_id, source, content):
        doc = {
            ElasticsearchDocVO.TIMESTAMP: datetime.now(),
            ElasticsearchDocVO.UPDATED_AT: datetime.now(),
            ElasticsearchDocVO.SOURCE: source,
            ElasticsearchDocVO.CONTENT: content,
            ElasticsearchDocVO.TOPICS: [],
            ElasticsearchDocVO.SENTIMENT: SentimentType.UNK.value
        }

        return self.es.create(
            index=index,
            id=elastic_id,
            body=doc
        )

