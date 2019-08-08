import requests as rq


class AddInfoExtractor(object):
    def __init__(self):
        pass

    def get_add_info(self, url):
        r = rq.get(url)
        return r.content

if __name__ == "__main__":
    cian_url = r'https://krasnogorsk.cian.ru/sale/flat/213886732/'
    avito_url = r'https://www.avito.ru/moskovskaya_oblast_krasnogorsk/kvartiry/3-k_kvartira_80.6_m_1017_et._1114532904'
    yandex_realty_url = r'https://realty.yandex.ru/offer/9132688428970246657/'

    a = AddInfoExtractor()
    print(a.get_add_info(cian_url))
