import re

import url_types as ut


class UrlManager(object):
    def __init__(self):
        self.url_regex = re.compile(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        pass

    def get_url_type(self, url):
        type_dict = ut.type_dict
        for key in type_dict:
            if type_dict[key] in url:
                return key
        return None

    def extract_url(self, text):
        url = text.split('?')[0]
        url = re.search(self.url_regex, url)
        if url is None:
            return None
        return url.group(0)


if __name__ == '__main__':
    um = UrlManager()
    text = r'https://www.avito.ru/moskovskaya_oblast_krasnogorsk/kvartiry/2-k_kvartira_70.7_m_1422_et._1785177086?utm_campaign=native&utm_medium=item_page_android&utm_source=soc_sharing'
    # text = 'https://www.avito.ru/moskovskaya_oblast_krasnogorsk/kvartiry/2-k_kvartira_70.7_m_1422_et._1785177086'
    print(um.extract_url(text))
    print(um.get_url_type(um.extract_url(text)))
