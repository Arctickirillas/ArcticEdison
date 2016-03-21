import time
import telebot
import getIP
from main import c,startThreads,stateTitle

# -- Telegram Bot
token = '192564123:AAGRl-UZkjcre5a6DvdFtnmkxyEqL6CMdTg'
def listener(messages):
    info = 'Hello! My name is arcticEdisonBot!\n'\
    'You can type:\n'\
    '/status - to get the last status,\n'\
    '/rushStatus - to get status immediately,\n'\
    '/estStates - to get the estimated state,\n'\
    '/getWiFiIP - to get wifi ip adress,\n'\
    '/info - to get help.\n\n'\
    '@arcticEdisonBot'
    for message in messages:
        if message.text == '/status':
            status = 'Light: '+str(c.light)+' Sound: '+str(c.mic)+ \
            ' Motion: '+str(c.motion)+' Vibrtion: '+str(c.vibration)
            bot.reply_to(message, status)
        elif message.text == '/rushStatus':
            bot.send_message(message.chat.id, 'Please, wait...')
            startThreads()
            status = 'Light: '+str(c.light)+' Sound: '+str(c.mic)+ \
            ' Motion: '+str(c.motion)+' Vibrtion: '+str(c.vibration)
            bot.reply_to(message, status)
        elif message.text == '/estStates':
            bot.reply_to(message, stateTitle)
        elif message.text == '/info':
            bot.reply_to(message, info)
        elif message.text == '/getWiFiIP':
            bot.reply_to(message, getIP.getIP('wlan0'))
        else:
            bot.reply_to(message, 'Type /info for help!')

bot = telebot.TeleBot(token)
bot.set_update_listener(listener)
bot.polling(none_stop=True, interval=True)