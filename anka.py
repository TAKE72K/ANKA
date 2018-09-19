#coding=utf-8
#A pure anka bot

#python lib
import os
import logging
#python telegram bot 
from telegram import Bot, Chat
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler
#self define module
import ankabase

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
    #if a private chat
    if update.message.chat_id>0:
        return
    self_info=bot.get_me()
    sender=update.message.from_user
    this_chat=bot.get_chat(chat_id=update.message.chat_id)
    start_me=InlineKeyboardMarkup([[InlineKeyboardButton(text='start me in PM',
                                    url='https://telegram.me/{}?start=hello'.format(self_info.username))]])
    #comfirm if there is a processing anka in this chat
    
    try:
        bot.send_message(chat_id=sender.id,text='{}開始安價囉'.format(this_chat.title))
    except:
        bot.send_message(chat_id=this_chat.id,text='start me!')
        return
    
    who_start=sender.id
    where_anka=this_chat.id
    new_anka_init(who_start,where_anka)
    
    keyboard=[[InlineKeyboardButton(text='設定標題',callback_data='set_title{}'.format(str(this_chat.id)))]]
    rplym=InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=sender.id,text='設個標題ㄅ',reply_markup=rplym)

def new_anka_init(userid,chatid):
    dic={}
    dic['host']=userid
    dic['place']=chatid
    dic['ankaid']=0
    #def 0 to be processing
    ankabase.insert_data('anka',dic)
    return

#callback reaction
def callback_re(bot,update):
    query = update.callback_query
    query_text=query.data
    query_sender=query.from_user
    
    def set_title():
        pass

def main():
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    #Bot Command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("newanka", new_anka))
    #recieve callback data
    db.add_handler(CallbackQueryHandler(callback_re))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(clean=True)

    # IDLE
    updater.idle()

if __name__ == '__main__':
    main()