from telegram.ext import Updater
from token_loader import TokenLoader
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

t = TokenLoader()
token = t.get('telegram_token')
updater = Updater(token=token)

dispatcher = updater.dispatcher


def start(update, context):
    print('get ', update.message)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=update.message.text)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
