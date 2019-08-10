import extractor_cian
import extractor_yandex_realty as yareal
import extractor_avito
import url_manager
import url_types as ut


class AdvInfoExtractor(object):
    def __init__(self):
        pass

    def get_info(self, url):
        um = url_manager.UrlManager()
        type = um.get_url_type(url)
        if type == ut.cian_type:
            return extractor_cian.Cian().extract_info(url)
        elif type == ut.yandex_type:
            return yareal.YandexRealty().extract_info(url)
        elif type == ut.avito_type:
            return extractor_avito.Avito().extract_info(url)
        else:
            pass
        return ''


if __name__ == "__main__":
    cian_url = r'https://krasnogorsk.cian.ru/sale/flat/213886732/'
    avito_url = r'https://www.avito.ru/moskovskaya_oblast_krasnogorsk/kvartiry/3-k_kvartira_80.6_m_1017_et._1114532904'
    yandex_realty_url = r'https://realty.yandex.ru/offer/9132688428970246657/'

    a = AdvInfoExtractor()
    print(a.get_info(cian_url))
    print(a.get_info(avito_url))
    print(a.get_info(yandex_realty_url))
