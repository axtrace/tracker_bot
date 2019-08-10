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
        url = re.search(self.url_regex, text)
        if url is None:
            return None
        return url.group(0)


if __name__ == '__main__':
    um = UrlManager()
    text = 'asdfasdsad https://www.cian.ru/sale/flat/202918034 asdf sad'
    # text = 'afdsfasdsdsfdadffdsaasf'
    print(um.extract_url(text))
    print(um.get_url_type(um.extract_url(text)))
