import json


class JsonLoader(object):
    def __init__(self):
        with open('tokens.json', 'r', encoding='utf-8') as read_file:
            self.data = json.load(read_file)
        self.oauth_token = self.data['token']
        self.org_id = self.data['org_id']

    def get_yatracker_tokens(self):
        return self.oauth_token, self.org_id

    def get_telegram_token(self, mode):
        token_type = 'telegram_token' if mode == '--prod' else 'telegram_token_test'
        return self.get(token_type)

    def get(self, name):
        try:
            return self.data[name]
        except:
            return None
