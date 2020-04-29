from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class SentimentType(BaseEnum):

    POS = 'pos'
    NEG = 'neg'
    NEU = 'neu'
    UNK = 'unk'


class SourceType(BaseEnum):

    TWITTER = 'twitter'
    INSTAGRAM = 'instagram'

