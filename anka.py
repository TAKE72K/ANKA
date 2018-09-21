#coding=utf-8
#A pure anka bot

#python lib
import os
import logging
#python telegram bot 
from telegram import Bot, Chat
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
#self define module
import ankabase as ak

token = os.environ['TELEGRAM_TOKEN']
updater = Updater(token,workers=16)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

#global arg
reply_dic={}
    
#FUNCTION
def check_hosting(chat_id):
    check=ak.get_doc(Collection='anka',
                pipeline={'place':chat_id})
    if check is None:
        return False
    for i in check:
        if i['ankaid']==0:
            return i['title']#there's a progressing anka
    return False

def check_host(userid):
    check=ak.get_doc(Collection='anka',
                    pipeline={'host':userid,'ankaid':0}
    )
    if check is not None:
        return check[0]['place']
    else:
        return False 

def new_anka_init(userid,chatid):
    dic={}
    dic['host']=userid
    dic['place']=chatid
    dic['ankaid']=0
    #def 0 to be processing
    ak.insert_data('anka',dic)
    return

def anka_title_init(title,chatid):
    ak.modify_doc('anka',{'place':chatid,'ankaid':0},'title',title)
    return

def anka_article_input(text,userid):
    doc=ak.get_doc(Collection='anka',
                    pipeline={'host':userid,'ankaid':0}
    )
    
    

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
    
    #check if there is a anka be hosting
    if check_hosting(update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id,
        text='本群已有正在進行的安價{}'.format(check_hosting(update.message.chat_id)))
        return
    
    #start a new one
    self_info=bot.get_me()
    sender=update.message.from_user
    this_chat=bot.get_chat(chat_id=update.message.chat_id)
    start_me=InlineKeyboardMarkup([[InlineKeyboardButton(text='start me!',
                                    url='https://telegram.me/{}?start=hello'.format(self_info.username))]])
    #comfirm if there is a processing anka in this chat
    
    try:
        bot.send_message(chat_id=sender.id,text='{}開始安價囉'.format(this_chat.title))
    except:
        bot.send_message(chat_id=this_chat.id,text='',reply_markup=start_me)
        return
    
    who_start=sender.id
    where_anka=this_chat.id
    new_anka_init(who_start,where_anka)
    '''
    keyboard=[[InlineKeyboardButton(text='設定標題',callback_data='set_title')]]
    rplym=InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=sender.id,text='設個標題~~',reply_markup=rplym)
    '''
    titleid=bot.send_message(chat_id=sender.id,text='設個標題~~',reply_markup=ForceReply())
    global reply_dic
    action={'host':who_start,'place':where_anka,'type':'set_title'}
    reply_dic[titleid.message_id]=action
    
def anka_article(bot,update):
    #check PM
    if update.message.chat_id<0:
        bot.send_message(chat_id=update.message.chat_id,text='這個指令只能在私訊使用')
        return
    #check host
    if check_host(update.message.from_user.id):
        input_article=bot.send_message(chat_id=update.message.from_user.id,text='請輸入內容',reply_markup=ForceReply())
        global reply_dic
        action={'host':update.message.from_user.id,
                'place':check_host(update.message.from_user.id),
                'type':'input_article'}
        reply_dic[input_article.message_id]=action
        return
    else:
        bot.send_message(chat_id=update.message.from_user.id,text='姆咪')
    
#message handlers
def message_callback(bot,update):
    global reply_dic
    
    msg=update.message
    if msg.reply_to_message is not None:
        action=reply_dic[msg.reply_to_message.message_id]
        if action['type']=='set_title':
            title=msg.text
            anka_title_init(title,action['place'])
            bot.send_message(chat_id=action['host'],text='標題{}已設置， /article-來輸入文章'.format(title))
            bot.send_message(chat_id=action['place'],text='{}開始了安價:{}'.format(msg.from_user.first_name,title))
            del reply_dic[msg.reply_to_message.message_id]
        
        if action['type']=='input_article':
            article=msg.text
            

#callback reaction
def callback_re(bot,update):
    query = update.callback_query
    query_text=query.data
    query_sender=query.from_user
    
    def set_title(place):
        bot.edit_message_text(text="請輸入標題",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=ForceReply())
    if query_text.find('title')!=-1:
        set_title(0)

def main():
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    #Bot Command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("newanka", new_anka))
    dp.add_handler(CommandHandler("article", anka_article))
    #recieve callback data
    dp.add_handler(CallbackQueryHandler(callback_re))
    #recieve message
    dp.add_handler(MessageHandler(Filters.all,message_callback))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(clean=True)

    # IDLE
    updater.idle()

if __name__ == '__main__':
    main()