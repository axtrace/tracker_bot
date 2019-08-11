import re
from bs4 import BeautifulSoup

from site_text_extractor import SiteTextExtractor as STE


class Avito(object):
    def __init__(self):
        pass

    def extract_info(self, url):
        ste = STE()
        text = ste.get_text(url)
        if text is None:
            return text
        self.soup = BeautifulSoup(text, features="lxml")
        self.text = self.soup.text
        res = dict()
        res['title'] = self.get_title()
        res['phone'] = self.get_digits_by_key('offerPhone', '\+\d+')
        res['price'] = self.get_digits_by_key('price')
        res['adv_id'] = self.get_digits_by_key('avito.item.id')

        res['build_year'] = self.get_digits_by_key('buildYear')
        return res

    def get_title(self):
        found = self.soup.find('meta', {
            'property': 'og:title'})
        if found:
            return found.get('content')
        return ''

    def get_digits_by_key(self, key, digit_regex='\d+'):
        text = self.text

        middle_parts = ('\":\"?', ' = \'')
        for mpart in middle_parts:
            regex = re.compile(key + mpart + digit_regex)
            found = re.search(regex, text)
            if found is not None:
                break
        if found is None:
            return ''
        found = found.group(0)
        regex2 = re.compile(digit_regex)
        found = re.search(regex2, found)
        if found is None:
            return ''
        return found.group(0)


if __name__ == "__main__":
    avito_url = r'https://www.avito.ru/moskovskaya_oblast_krasnogorsk/kvartiry/2-k_kvartira_70.7_m_1422_et._1785177086?utm_campaign=native&utm_medium=item_page_android&utm_source=soc_sharing'
    c = Avito()
    print(c.extract_info(avito_url))
