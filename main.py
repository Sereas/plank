import requests
import telebot


bot = telebot.TeleBot('1088985217:AAHXJF3KofCRj1rkgpRURce8pYl4Ow1Zlu8')

#proxy
login = 'olegdylevich'
pwd = '	W1o7SqQ'
ip = '89.191.230.201'
port = '65233'


telebot.apihelper.proxy = {
  'https': 'https://{}:{}@{}:{}'.format(login, pwd, ip, port)
}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


bot.polling()
