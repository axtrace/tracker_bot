import requests as rq

from token_loader import TokenLoader
from yandex_tracker_client import TrackerClient


class Tracker(object):
    def __init__(self):
        token_loader = TokenLoader()
        oauth_token, x_org_id = token_loader.get_tokens()
        # self.host = r'https://api.tracker.yandex.net'
        # self.headers = {'Authorization': 'OAuth ' + oauth_token,
        #                 'X-Org-Id': x_org_id}
        self.client = TrackerClient(token=oauth_token, org_id=x_org_id)

    def get_task(self, task_id):
        return self.client.issues[task_id]

    def create_task(self, summary, queue='FLAT', stype={'name': 'Flat'},
                    description='test description', ad_url="https:test.com"):
        self.client.issues.create(queue=queue, summary=summary, type=stype,
                                  description=description, ad_url=ad_url)


if __name__ == "__main__":
    t = Tracker()
    print(t.get_task('FLAT-20'))
    d = {'summary': 'test2', "queue": {"id": "7"}, "ad_url": "https:test.com"}
    t.create_task(summary='test2test')
