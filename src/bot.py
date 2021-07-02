# just empty template
import os
import logging
import pymongo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from db import add_user, user_status, clear_data, clear_route
from preprocessing import parse_userdata


TG_TOKEN = os.getenv('TG_TOKEN')
DB_URL = os.getenv('DB_URL')


def start(update, context):
    pass

def help(update, context):
    update.message.reply_text('apua!!')

def init(update, context):
    data = parse_userdata(update.message, context.bot)
    status_data = user_status(data['username'], context.bot_data['db'])
    if not status_data['user_info']:
        add_user(data, context.bot_data['db'])
    else:
        update.message.reply_text('User already in db')

def status(update, context):
    userName = update.message['from_user']['username']
    status_data = user_status(userName, context.bot_data['db'])
    if status_data['user_info']:
        update.message.reply_text('User found with {} datapoints'.format(status_data['locations']))
    else:
        update.message.reply_text('No user information in db')

def clear(update, context):
    userName = update.message['from_user']['username']
    clear_route(userName, context.bot_data['db'])

def clearData(update, context):
    userName = update.message['from_user']['username']
    clear_data(userName, context.bot_data['db'])

    status_data = user_status(userName, context.bot_data['db'])
    if not status_data['user_info']:
        update.message.reply_text('All user information deleted')
    else:
        update.message.reply_text('Clearing user information failed')

def main():
    updater = Updater(TG_TOKEN, use_context=True)
    dp = updater.dispatcher

    client = pymongo.MongoClient(os.getenv(DB_URL))
    db = client.routedata
    dp.bot_data['db'] = db

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("init", init))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("clear", clear))
    dp.add_handler(CommandHandler("clearData", clearData))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
