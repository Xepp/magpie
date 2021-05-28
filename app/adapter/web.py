import re
import requests

from bs4 import BeautifulSoup


class KhabarFooriAdapter:

    def parse_comment(self, tag):
        head = tag.find('div', { 'class': 'head' })
        body = tag.find('div', { 'class': 'body' })
        author = head.find('span', { 'class': 'pull-right' }).text
        info = head.find_all('span', { 'class': 'pull-left' })
        text = body.p.text
        date = re.sub('-', '', info[-1].text)
        date = re.sub('\n', '', date)
        date = re.sub(' +', ' ', date)
        pos = info[0].text if len(info) == 4 else '-'
        neg = info[1].text if len(info) == 4 else '-'

        return {
            'author': author,
            'date': date,
            'text': text,
            'pos': pos,
            'neg': neg,
            'replays': []
        }

    def get_page_comments(self, url):
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'html.parser')

        result = []
        comments = soup.find('div', { 'class': 'comments-content' })
        rows = comments.find_all('div', { 'class': 'comment' })
        for row in rows:
            if 'comment-replay' in row.attrs['class']:
                continue
            
            comment = self.parse_comment(row)

            replays = row.find_all('div', { 'class': 'comment-replay' })
            for replay in replays:
                comment['replays'].append(self.parse_comment(replay))

            result.append(comment)

        return result

