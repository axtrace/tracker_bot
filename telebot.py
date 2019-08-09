from telegram.ext import Updater
from token_loader import TokenLoader
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import telebot

t = TokenLoader()
token = t.get('telegram_token')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


bot.polling()
