import time

import telebot
from threading import Thread
from time import sleep
import base

bot = telebot.TeleBot('5548062264:AAHnEhootMDvYJ15n_Svg9yolnKrMa--Dns')
#bd = base.Base("mongodb")
bd = base.Base("mongodb://Roooasr:sedsaigUG12IHKJhihsifhaosf@mongodb:27017/")

def bans(usrId,group,minutes):
    bd.setBan(usrId=usrId,group=group,ban=True)
    sleep(minutes*60)
    bd.setBan(usrId=usrId, group=group, ban=False)

### Comands

@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.id)
    if bd.getUser(message.from_user.id,message.chat.id) is None:
        bd.regUser(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Ты зареган")

    if bd.getUser(message.from_user.id,message.chat.id) is None:
        bd.regUser(message.from_user.id,message.chat.id)

@bot.message_handler(commands=['ban'])
def ban(message):
    if bd.getUser(message.from_user.id, message.chat.id)['admin'] is True:
        usrId = message.json['reply_to_message']['from']['id']
        group = message.chat.id
        timess = message.text.split(" ")
        if len(timess) > 0:
            tr = Thread(target=bans,args=(usrId,group,int(timess[1])))
            tr.start()
        else:
            bot.reply_to(message, "Введи время в минутах на сколько забанить")
    else:
        bot.reply_to(message, "Только для админов")



@bot.message_handler(commands=['restart'])
def restart(message):
    if bd.getUser(message.from_user.id,message.chat.id) is None:
        bd.regUser(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Ты зареган")

    try:
        admns = bot.get_chat_administrators(message.chat.id)

        for a in admns:
            bd.setAdmin(a.user.id,message.chat.id)
    except:
        pass


@bot.message_handler(commands=['me'])
def me(message):
    if bd.getUser(message.from_user.id,message.chat.id) is None:
        bd.regUser(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Ты зареган")

    try:
        usr = bd.getUser(message.from_user.id,message.chat.id)
        txt = f"Уровень: {usr['lvl']}\nКол-во балов: {usr['balCount']}\nАдминка: {usr['admin']}"
        print(txt)
        bot.reply_to(message,txt)
    except:
        pass

@bot.message_handler(commands=['help'])
def help(message):
    if bd.getUser(message.from_user.id,message.chat.id) is None:
        bd.regUser(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Ты зареган")

    bot.send_message(message.chat.id,f"/me Личная информация\n/all (Для админов) позвать всех\n/restart перезапустить бота\n/ban (Присылать в ответ на сообщение пользователю обязательно указывать время)")

@bot.message_handler(commands=['all'])
def all(message):
    if bd.getUser(message.from_user.id,message.chat.id) is None:
        bd.regUser(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Ты зареган")

    if bd.getUser(message.from_user.id,message.chat.id)['admin'] is True:
        curs = bd.getAllUser(message.chat.id)
        mcg = []
        for c in curs:
            print(c)
            mcg.append(f"[.](tg://user?id={c['usrId']})")
        bot.send_message(message.chat.id,"".join(mcg),parse_mode='Markdown')
    else:
        bot.reply_to(message, "Только для админов")


@bot.message_handler(content_types = ['new_chat_members'])
def new_chat_members(message):
    if bd.getUser(message.from_user.id, message.chat.id) is None:
        bd.regUser(message.from_user.id, message.chat.id)
    bot.delete_message(message.chat.id, message.message_id)

## Obrabotka message

@bot.message_handler(content_types = ['video_note'])
def video_note(message):
    try:
        if bd.getUser(message.from_user.id, message.chat.id) is None:
            bd.regUser(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, "Ты зареган")
        if bd.getUser(message.from_user.id,message.chat.id)['ban'] is True:
            bot.delete_message(message_id=message.message_id,chat_id=message.chat.id)
        else:
            bd.addBall(message.from_user.id,3)
            wtf = bd.checkLvl(message.from_user.id, message.chat.id)
            if wtf == 1:
                bot.reply_to(message,"Ты получил новый уровень!")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))

@bot.message_handler(content_types = ['photo'])
def photo(message):
    try:
        if bd.getUser(message.from_user.id, message.chat.id) is None:
            bd.regUser(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, "Ты зареган")
        if bd.getUser(message.from_user.id,message.chat.id)['ban'] is True:
            bot.delete_message(message_id=message.message_id,chat_id=message.chat.id)
        else:
            bd.addBall(message.from_user.id,5,message.chat.id)
            wtf = bd.checkLvl(message.from_user.id, message.chat.id)
            if wtf == 1:
                bot.reply_to(message,"Ты получил новый уровень!")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))

@bot.message_handler(content_types = ['video'])
def video(message):
    try:
        if bd.getUser(message.from_user.id, message.chat.id) is None:
            bd.regUser(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, "Ты зареган")
        if bd.getUser(message.from_user.id,message.chat.id)['ban'] is True:
            bot.delete_message(message_id=message.message_id,chat_id=message.chat.id)
        else:
            bd.addBall(message.from_user.id,5, message.chat.id)
            wtf = bd.checkLvl(message.from_user.id, message.chat.id)
            if wtf == 1:
                bot.reply_to(message,"Ты получил новый уровень!")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))

@bot.message_handler(content_types = ['voice'])
def voice(message):
    try:
        if bd.getUser(message.from_user.id, message.chat.id) is None:
            bd.regUser(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, "Ты зареган")
        if bd.getUser(message.from_user.id,message.chat.id)['ban'] is True:
            bot.delete_message(message_id=message.message_id,chat_id=message.chat.id)
        else:
            bd.addBall(message.from_user.id,2, message.chat.id)
            wtf = bd.checkLvl(message.from_user.id, message.chat.id)
            if wtf == 1:
                bot.reply_to(message,"Ты получил новый уровень!")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))


@bot.message_handler(content_types=['text','sticker'])
def text(message):
    try:
        if bd.getUser(message.from_user.id, message.chat.id) is None:
            bd.regUser(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, "Ты зареган")
        if bd.getUser(message.from_user.id,message.chat.id)['ban'] is True:
            bot.delete_message(message_id=message.message_id,chat_id=message.chat.id)
        else:
            bd.addBall(message.from_user.id,1, message.chat.id)
            wtf = bd.checkLvl(message.from_user.id, message.chat.id)
            if wtf == 1:
                bot.reply_to(message,"Ты получил новый уровень!")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))

## Obrabotka message

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)