import requests as rq


class SiteTextExtractor(object):
    def __init__(self):
        pass

    def get_text(self, url):
        r = rq.get(url)
        r.encoding = 'utf-8'
        if r.status_code == 200:
            return r.text
        return None
