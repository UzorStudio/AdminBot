import time

import telebot

import base

bot = telebot.TeleBot('5548062264:AAHnEhootMDvYJ15n_Svg9yolnKrMa--Dns')
#bd = base.Base("mongodb")
bd = base.Base("mongodb://Roooasr:sedsaigUG12IHKJhihsifhaosf@mongodb:27017/")

@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.id)
    if bd.getUser(message.from_user.id,message.chat.id) is None:
        bd.regUser(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Ты зареган")

    if bd.getUser(message.from_user.id,message.chat.id) is None:
        bd.regUser(message.from_user.id,message.chat.id)

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
        txt = f"Уровень: {usr['lvl']}\nВсего сообщений: {usr['msgCount']}\nАдминка: {usr['admin']}"
        print(txt)
        bot.reply_to(message,txt)
    except:
        pass

@bot.message_handler(commands=['help'])
def help(message):
    if bd.getUser(message.from_user.id,message.chat.id) is None:
        bd.regUser(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Ты зареган")

    bot.send_message(message.chat.id,f"/me Личная информация\n/all (Для админов) позвать всех\n/restart перезапустить бота")

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


@bot.message_handler(content_types = ['new_chat_members', 'left_chat_member'])
def delete(message):
    bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(content_types=['text'])
def text(message):
    try:
        print(message)
        if bd.getUser(message.from_user.id,message.chat.id) is None:
            bd.regUser(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id,"Ты зареган")
        else:
            bd.addMsg(message.from_user.id)
            wtf = bd.checkLvl(message.from_user.id)
            if wtf == 1:
                bot.reply_to(message,"Ты получил новый уровень!")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))



if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)