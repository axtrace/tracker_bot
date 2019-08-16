import sys
import telebot
import time
import pytz
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from json_loader import JsonLoader
from url_manager import UrlManager
from tracker import Tracker
from adv_info_extractor import AdvInfoExtractor

# apihelper.proxy = {'http': 'http://10.10.1.10:3128'}


t = JsonLoader()
mode = '--prod' if '--prod' in sys.argv else 'test'
token = t.get_telegram_token(mode)
bot = telebot.TeleBot(token)
um = UrlManager()
tr = Tracker()
adv_ex = AdvInfoExtractor()

allowed_ids = set([214777789, 35846529])
current_message = dict()


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Добавить все равно", callback_data="add_anyway"))
    return markup


def prepare_info(adv_info, url):
    res = dict()
    res['title'] = adv_info.get('title', 'Квартира')
    res['price'] = 0 if adv_info.get('price', 0) == '' else int(
        adv_info.get('price', 0)) / 1000
    res['phone'] = adv_info.get('phone', '')
    res['adv_id'] = adv_info.get('adv_id', '')
    res['build_year'] = adv_info.get('build_year', '')
    res['url'] = url
    res['description'] = url
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
    if issue.price is not None:
        msg += 'Стоимость: ' + str(issue.price) + '\n'
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


def send_issues_list(chat_id, found_issues, count_limit):
    cl = count_limit
    for issue in found_issues:
        bot.send_message(chat_id, prepare_msg_by_issue(issue))
        cl -= 1
        if cl == 0:
            return
    bot.send_message(chat_id, '-------')


def add_issue_if_no_exists(url):
    inf = prepare_info(adv_ex.get_info(url), url)
    found_issues = tr.find_existing(inf)
    is_already_exists = False
    if found_issues:
        is_already_exists = True
    else:
        create_task(inf)
        # found_issues = tr.find(inf['adv_id'])
        time.sleep(1)
        found_issues = tr.find('Created: >= now()  - "1m" and Author: me() ')
    return is_already_exists, found_issues


def create_task(inf):
    tr.create_task(summary=inf['title'], description=inf['description'],
                   ad_url=inf['url'], price=inf['price'],
                   phone=inf['phone']
                   )


def url_add_handler(chat_id, url):
    already_exist, found_issues = add_issue_if_no_exists(url)
    if already_exist:
        bot.send_message(chat_id, 'Кажется, уже что-то похожее есть:')
        send_issues_list(chat_id, found_issues, 3)
        # todo: Add ADV anyway
    else:
        bot.send_message(chat_id, 'Добавил:')
        send_issues_list(chat_id, found_issues, 1)


def try_to_find_handler(chat_id, text):
    bot.send_message(chat_id,
                     'Не похоже на урл. Попробую поискать в трекере. /help')
    found_issues = tr.find(text)
    if found_issues:
        bot.send_message(chat_id, 'Вот что удалось найти',
                         reply_markup=gen_markup())
        send_issues_list(chat_id, found_issues, 0)
    else:
        bot.send_message(chat_id, 'Ничего похожего не нашел',
                         reply_markup=gen_markup())


def is_user_allowed(message):
    return message.from_user.id in allowed_ids


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "add_anyway":
        inf = {'title': 'Квартира XXX'}
        inf['description'] = current_message.get(call.message.from_user.id, '')
        inf['price'] = 0
        inf['phone'] = ''
        inf['url'] = 'https://tracker.yandex.ru/'
        create_task(inf)
        time.sleep(1)
        found_issues = tr.find('Created: >= now()  - "1m" and Author: me() ')
        bot.answer_callback_query(call.id, "Добавил")
        send_issues_list(call.message.chat.id, found_issues, 3)


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
    send_issues_list(message.chat.id, found_issues, 3)


@bot.message_handler(func=lambda message: True,
                     content_types=['text'])
def command_default(message):
    if not is_user_allowed(message):
        bot.send_message(message.chat.id, 'Вы не в списке доверенных лиц :(')
        return 0
    url = um.extract_url(message.text)
    current_message[message.from_user.id] = message.text
    if url is not None:
        url_add_handler(message.chat.id, url)
    else:
        try_to_find_handler(message.chat.id, message.text)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(15)
