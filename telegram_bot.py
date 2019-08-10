import telebot
import time
import pytz
from dateutil.parser import parse
from datetime import datetime
from telebot import apihelper
from token_loader import TokenLoader
from url_manager import UrlManager
from tracker import Tracker
from adv_info_extractor import AdvInfoExtractor

# apihelper.proxy = {'http': 'http://10.10.1.10:3128'}

t = TokenLoader()
token = t.get('telegram_token')
bot = telebot.TeleBot(token)
um = UrlManager()
tr = Tracker()
adv_ex = AdvInfoExtractor()

allowed_ids = set([214777789, 35846529])


def prepare_info(adv_info, url):
    res = dict()
    res['title'] = adv_info.get('title', 'Квартира')
    res['price'] = 0 if adv_info.get('price', 0) == '' else int(
        adv_info.get('price', 0)) / 1000
    res['phone'] = adv_info.get('phone', '')
    res['adv_id'] = adv_info.get('adv_id', '')
    res['build_year'] = adv_info.get('build_year', '')
    res['url'] = url
    return res


def prepare_msg_by_issue(issue):
    msg = issue.summary + '\n'
    msg += tr.tracker_url + issue.key + '\n'
    if issue.address is not None:
        msg += issue.address + '\n'
    if issue.phone is not None:
        msg += issue.phone + '\n'
    if issue.agentname is not None:
        msg += issue.agentname + '\n'
    if issue.datetimeview is not None and issue.datetimeview != '':
        utc_datetime = datetime.strptime(issue.datetimeview,
                                         '%Y-%m-%dT%H:%M:%S.%f%z')
        msc_datetime = utc_datetime.astimezone(pytz.timezone('Europe/Moscow'))
        msg += 'Дата и время просмотра: '
        msg += msc_datetime.strftime(
            "%d.%m.%Y %H:%M") + '\n'
    if issue.ad_url is not None:
        msg += issue.ad_url + '\n'
    return msg


def send_issues_list(chat_id, found_issues, ):
    for issue in found_issues:
        bot.send_message(chat_id, prepare_msg_by_issue(issue))


def create_task(inf):
    tr.create_task(summary=inf['title'], description=inf['url'],
                   ad_url=inf['url'], price=inf['price'],
                   phone=inf['phone']
                   )


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, присылай ссылки на объявления, я их добавлю в Tracker')


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id, 'Достунпые команды' + '\n'
                     + 'Назначены просмотры: ' + '/nearest')


@bot.message_handler(commands=['nearest'])
def command_help(message):
    filter = {'status': 'assignedtoview'}
    found_issues = tr.find(request='', filter=filter, order=['datetimeview'])
    send_issues_list(message.chat.id, found_issues)


@bot.message_handler(func=lambda message: True,
                     content_types=['text'])
def command_default(message):
    if not message.chat.id in allowed_ids:
        bot.send_message(message.chat.id,
                         'Извините, вы не в списке доверенных лиц :(')
        return 0
    url = um.extract_url(message.text)
    if not url is None:
        inf = prepare_info(adv_ex.get_info(url), url)
        found_issues = tr.find(inf['adv_id'])
        if found_issues:
            bot.send_message(message.chat.id,
                             'Кажется, уже что-то похожее есть')
            send_issues_list(message.chat.id, found_issues)
        else:
            create_task(inf)
            bot.send_message(message.chat.id, 'Добавил:')
            found_issues = tr.find(inf['adv_id'])
            send_issues_list(message.chat.id, found_issues)
    else:
        bot.send_message(message.chat.id,
                         'Не похоже на урл. Попробую поискать в трекере. /help')
        found_issues = tr.find(message.text)
        if found_issues:
            bot.send_message(message.chat.id,
                             'Вот что удалось найти')
            send_issues_list(message.chat.id, found_issues)
        bot.send_message(message.chat.id, '-------')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(15)
