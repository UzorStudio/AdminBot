import telebot

import base

bot = telebot.TeleBot('5548062264:AAHnEhootMDvYJ15n_Svg9yolnKrMa--Dns')
#bd = base.Base("mongodb")
bd = base.Base("mongodb://Roooasr:sedsaigUG12IHKJhihsifhaosf@mongodb:27017/")

@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.id)
    if bd.getUser(message.from_user.id) is None:
        bd.regUser(message.from_user.id,message.chat.id)

@bot.message_handler(commands=['restart'])
def restart(message):
    try:
        admns = bot.get_chat_administrators(message.chat.id)

        for a in admns:
            bd.setAdmin(a.user.id)
    except:
        pass


@bot.message_handler(commands=['all'])
def all(message):
    if bd.getUser(message.from_user.id)['admin'] is True:
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
        if bd.getUser(message.from_user.id) is None:
            bd.regUser(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id,"Ты зареган")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))



if __name__ == "__main__":
    while True:
        bot.polling()