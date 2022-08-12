import random
import os
import time
import telebot
from telebot import types
import guess

# bot
TOKEN = os.environ.get("TOKEN", "")
bot = telebot.TeleBot(TOKEN)
    

# start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello *" + message.from_user.first_name + "*, I can guess your number. want to try? use \n*/play* to play default game *or\n/play 200* to set your limits",parse_mode="Markdown")


# play command
@bot.message_handler(commands=['play'])
def startgame(message):

    try:
        N = int(message.text.split("/play ")[1])
        if N > 1000:
            bot.reply_to(message,"*Not more than 1000*",parse_mode="Markdown")
            return
    except:
        N = 100

    size = len(bin(N).replace("0b", ""))
    bot.reply_to(message,f"_Take a Number between_ *1 - {N}*\n_I will guess it in_ *{size} steps*\n_are you_ *ready ?*",parse_mode="Markdown",
        reply_markup=types.InlineKeyboardMarkup(
            keyboard=[
                [
                    types.InlineKeyboardButton( text='Yes', callback_data='ready'),
                    types.InlineKeyboardButton( text='No', callback_data='not')
                ]
            ]
                ))


# not ready callback
@bot.callback_query_handler(func=lambda c: c.data == 'not')
def not_callback(call: types.CallbackQuery):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'*OK, No Problem.*', parse_mode="Markdown")


# ready calback
@bot.callback_query_handler(func=lambda c: c.data == 'ready')
def ready_callback(call: types.CallbackQuery):

    N = int(call.message.text.split(" - ")[1].split("\n")[0])
    size = len(bin(N).replace("0b", ""))
    binary = "0".zfill(size+1)

    nlist = list(range(0,size))
    random.shuffle(nlist)
    slist = ""
    for ele in nlist:
        slist = slist + str(ele)

    text = guess.generateNumbers(int(slist[0])+1, N, size)

    ydata = f'{N} {binary} {slist} 1'
    ndata = f'{N} {binary} {slist} 0'

    #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'*{text}*\n_is your number there ?_', parse_mode="Markdown")
    #time.sleep(0.5)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'*{text}*\n_is your number there ?_ *(1 / {size})*', parse_mode="Markdown",
       reply_markup=types.InlineKeyboardMarkup(
            keyboard=[
                [
                    types.InlineKeyboardButton( text='Yes', callback_data=ydata),
                    types.InlineKeyboardButton( text='No', callback_data=ndata)
                ]
            ]
                ))

# game response callback  
@bot.callback_query_handler(func=None)
def game_callback(call: types.CallbackQuery):

    data = call.data.split(" ")
    N = int(data[0])
    size = len(bin(N).replace("0b", ""))
    binary = data[1]
    slist = data[2]
    res = data[3]

    pos = int(slist[0])+1
    slist = slist[1:]
    binary = list(binary)
    binary[pos] = res
    binary = "".join(binary)

    if len(slist) != 0:

        text = guess.generateNumbers(int(slist[0])+1, N, size)
        ydata = f'{N} {binary} {slist} 1'
        ndata = f'{N} {binary} {slist} 0'

        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'*{text}*\n_is your number there ?_', parse_mode="Markdown")
        #time.sleep(0.5)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'*{text}*\n_is your number there ?_ *({size-len(slist)+1} / {size})*', parse_mode="Markdown",
                reply_markup=types.InlineKeyboardMarkup(
                    keyboard=[
                        [
                            types.InlineKeyboardButton( text='Yes', callback_data=ydata),
                            types.InlineKeyboardButton( text='No', callback_data=ndata)
                        ]
                    ]
                        ))
    
    else:

        number = guess.finalize(binary,N)
        if number == 0:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'_I said in between_ *1 - {N}*',parse_mode="Markdown")
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'_Your number is_ *{number}*',parse_mode="Markdown")


# server loop
#print("Bot Started")
bot.infinity_polling()