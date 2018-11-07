import os
import sys
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram import MessageEntity
from telegram.ext import BaseFilter
from telegram.ext import CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging


def open_images():
	try:
		foto = open("fenixLogo.png",'rb')
		return foto
	except IOError:
		return -1




class FilterTwitch(BaseFilter):
    def filter(self, message):
        return 'twitch.tv' in message.text

class FilterAlguienPara(BaseFilter):
	def filter(self, message):
		if('alguien para' in message.text):
			return True
		if('Alguien para' in message.text):
			return True
		return False




def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def delete_spam(bot, update):
	print(update.message.chat)

	chat_id = update.message.chat_id
	usuario = update.message.from_user
	estado = bot.getChatMember(chat_id,usuario.id).status

	if(estado=="member"):

		print("Spam detected:"+usuario.username+" ("+estado+")")

		mensaje = "Veo que te gusta publicar spam, pues aqui no puedes muajajaja."
		bot.send_message(chat_id=chat_id, text=mensaje)

		bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)


def alguien_para_function(bot,update):
	chat_id = update.message.chat_id
	message_id = update.message.message_id
	usuario = update.message.from_user

	text_from_user = "**"
	text_from_user = text_from_user + update.message.text
	text_from_user = text_from_user + "**"

	#bot.delete_message(chat_id=chat_id, message_id=message_id)

	button_list = [[InlineKeyboardButton("Me apunto",callback_data='IamIn')]]
	reply_markup = InlineKeyboardMarkup(button_list)
	bot.send_message(chat_id=chat_id, text=text_from_user, reply_markup=reply_markup)


def alguien_para_menu_function(bot,update):
	print("")
	print("Someone press a button")
	print(update.callback_query)

	callback = update.callback_query
	callback_query_id = callback.id
	chat_id = callback.message.chat.id
	message_id = callback.message.message_id
	usuario = callback.from_user.first_name

	if('**' in update.callback_query.message.text):
		text = update.callback_query.message.text
	else:
		text = '**' + update.callback_query.message.text + '**'
	text = text + '\n \t \t \t - ' + usuario

	button_name = update.callback_query.data

	button_list = [[InlineKeyboardButton("Me apunto",callback_data='IamIn')]]
	reply_markup = InlineKeyboardMarkup(button_list)

	if(button_name == 'IamIn' and usuario not in update.callback_query.message.text):
		bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
		bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
		bot.answer_callback_query(callback_query_id=callback_query_id, text="Te has apuntado")
	else:
		bot.answer_callback_query(callback_query_id=callback_query_id, text="Ya estabas apuntado")



def fotosexy(bot, update):
	chat_id = update.message.chat_id
	foto = open_images()
	bot.send_photo(chat_id, foto, caption="mira que sexy soy")

def version(bot,update):
	chat_id = update.message.chat_id
	version_text = 'version 1.3'
	bot.send_message(chat_id=chat_id,text=version_text)







# get the token
if os.path.isfile('token.txt'):
        file = open('token.txt','r')
        print("TOKEN FILE FIND")
        tokenFromFile = file.readline()
else:
        print("couldn't find the file token file .... looking for token in env variables...")
        if os.environ['TOKEN'] is None:
        	sys.exit(1)
        tokenFromFile = os.environ['TOKEN']

foto = open_images()
# la clase updater es la que realiza las actualizaciones de contenido
# para iniciar la clase se necesita el token del bot
updater = Updater(token=tokenFromFile)

# el dispatcher es la clase que se encarga de responder a las updates
# se crea por defecto al iniciar el updater, la recogemos en una variable
dispatcher = updater.dispatcher

# informacion de errores
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# los handlers se asocian al dispatcher, se puede crear un handler desde cero
# o usar los que ya hay creado como commandhandle y messagehandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


filter_twitch = FilterTwitch()
twitch_handler = MessageHandler(filter_twitch, delete_spam)
dispatcher.add_handler(twitch_handler)

sexy_handler = CommandHandler('sexy', fotosexy, pass_args=False)
foto_handler = CommandHandler('foto', fotosexy, pass_args=False)
dispatcher.add_handler(sexy_handler)
dispatcher.add_handler(foto_handler)

alguien_para_filter = FilterAlguienPara()
alguien_para_handler = MessageHandler(alguien_para_filter, alguien_para_function)
dispatcher.add_handler(alguien_para_handler)
alguien_para_menu_handler = CallbackQueryHandler(alguien_para_menu_function)
dispatcher.add_handler(alguien_para_menu_handler)

version_handler = CommandHandler('version',version,pass_args=False)
dispatcher.add_handler(version_handler)

updater.start_polling()
