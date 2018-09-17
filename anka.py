#coding=utf-8
#A pure anka bot

#python lib
import os
#python telegram bot 
from telegram import Bot, Chat
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler

token = os.environ['TELEGRAM_TOKEN']
updater = Updater(token,workers=16)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

#COMMAND FUNCTION
def start(bot,update):
    #enable PM
    self_info=bot.get_me()
    self_intro='''
    Hi~~我是{}
    請直撥分機號碼，或按/help由總機為您服務~~
    '''
    self_intro=self_intro.format(self_info.first_name)
    bot.send_message(chat_id=update.message.chat_id,text=self_intro)

def new_anka(bot,update):
    #if get 'anka' ,pm command sender
    sender=update.message.from_user
    start_me=InlineKeyboardMarkup([[InlineKeyboardButton(text='start me in PM',url='https://telegram.me/Chiahayabot?start=hello')]])
    try:
        bot.send_message(chat_id=sender.id,text='')
    except:
        bot.send_message(chat_id=update.message.chat_id,text='start me!')





def main():
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    #Bot Command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("newanka", new_anka))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(clean=True)

    # IDLE
    updater.idle()

if __name__ == '__main__':
    main()