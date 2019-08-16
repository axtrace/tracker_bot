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
        default_info = {'title': 'Квартира',
                        'url': url}
        if type == ut.cian_type:
            return extractor_cian.Cian().extract_info(url)
        elif type == ut.yandex_type:
            return yareal.YandexRealty().extract_info(url)
        elif type == ut.avito_type:
            return extractor_avito.Avito().extract_info(url)
        return default_info


if __name__ == "__main__":
    pass
