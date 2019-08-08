import telebot
from token_loader import TokenLoader

t = TokenLoader()
token = t.get('telegram_token')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


bot.polling()
