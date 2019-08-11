import requests as rq

from json_loader import JsonLoader
from yandex_tracker_client import TrackerClient


class Tracker(object):
    def __init__(self):
        json_loader = JsonLoader()
        oauth_token, x_org_id = json_loader.get_yatracker_tokens()
        self.client = TrackerClient(token=oauth_token, org_id=x_org_id)
        self.tracker_url = r'https://tracker.yandex.ru/'

    def get_task(self, task_id):
        return self.client.issues[task_id]

    def create_task(self, summary, queue='FLAT', issue_type={'name': 'Flat'},
                    description='', ad_url='', price=0, phone=''):
        self.client.issues.create(queue=queue,
                                  summary=summary,
                                  type=issue_type,
                                  description=description,
                                  ad_url=ad_url,
                                  price=price,
                                  phone=phone)

    def find(self, request, filter='', order=''):
        if filter == '' and order == '':
            issues = self.client.issues.find(request)
        elif filter == '':
            issues = self.client.issues.find(order=order)
        elif order == '':
            issues = self.client.issues.find(filter=filter)
        else:
            issues = self.client.issues.find(filter=filter,
                                             order=order)
        return issues


if __name__ == "__main__":
    t = Tracker()
    cian_url = r'https://krasnogorsk.cian.ru/sale/flat/21388afds/'
    # task = t.get_task('FLAT-20')
    print(t.find('FLAT-38'))
    print(t.find(202918034))
    d = {'summary': 'test2', "queue": {"id": "7"}, "ad_url": "https:test.com"}
    # issue = t.create_task(summary='TestTestTest222', ad_url=cian_url)
    # print(issue)
