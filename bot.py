from typing import Any

import telebot
from telebot import types
import time
import sqlite3

import sys

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, r"C:\Users\Слава\test1_bot_python\DB")
sys.path.insert(1, r"C:\Users\Слава\test1_bot_python")
from SQLDateBase import SQLighter
import TOKEN

bot = telebot.TeleBot(TOKEN.Token)

# инициализируем соединение с БД
db = SQLighter(TOKEN.DB)


# Доступные команды
@bot.message_handler(commands=['start'])
def start(message):
    # Регистрируем пользователя
    if not bool(len(db.subscriber_exists(message.from_user.id))):
        # если юзера нет в базе, добавляем его
        bot.send_message(message.chat.id, 'Привет, ' + str(message.from_user.first_name) + '!')
        db.add_subscriber(message.from_user.id, username=message.from_user.username,
                          first_name=message.from_user.first_name, last_name=message.from_user.last_name)

    bot.send_message(message.chat.id, "Список доступных команд\n"
                                      "/network - связь с нами\n"
                                      "/help - Справка\n"
                                      "/sub - подписаться на уведомления\n"
                                      "/unsub - отписаться от уведомлений\n"
                                      "/delete_user - Удалить себя из базы данных\n"""
                                      "/getsub - Вывести список всех подписчиков\n"
                                      "/getuser - Вывести список всех пользователей\n"""
                                      "/referral - Реферальная система\n"
                                      "/Hello\n"""
                                      "/list_users - Все кто пользовался ботом")


# help - справка
@bot.message_handler(commands=['help'])
def help(message):
    help_me = types.InlineKeyboardMarkup()
    help_Button = types.InlineKeyboardButton(text="Вот ссылки на связь с ним:", callback_data='info_about_me')
    help_me.add(help_Button)
    bot.send_message(message.chat.id, "Я помочь ничем не могу(\n"
                                      "Уж так меня запрограммировал мой создатель, но вы можете узнать у него что вам нужно",
                     reply_markup=help_me)


# network - таблица с информации о разных людях
@bot.message_handler(commands=['network'])
def network(message):
    markup = types.InlineKeyboardMarkup()
    item = [
        types.InlineKeyboardButton("Софа", callback_data='test'),
        types.InlineKeyboardButton("Слава", callback_data='info_about_me'),
        types.InlineKeyboardButton("🍑жопа", url="https://vk.com/ivanyshka4"),
        types.InlineKeyboardButton("🤞", url="https://vk.com/russellmoore"),
        types.InlineKeyboardButton("🤙🏽", url="https://vk.com/yumaguzhin_ddd"),
        types.InlineKeyboardButton("🤘", url="https://vk.com/vovanchoyt")
    ]
    markup.add(*item)
    bot.send_message(message.chat.id, "Лучше не связывайся с нами😈", reply_markup=markup)


# callbacki от главного меню
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # инфо о Соф
    if call.message:
        if call.data == 'test':
            a = types.InlineKeyboardMarkup()
            b = types.InlineKeyboardButton(text="⏮Назад", callback_data="cancel")
            a.add(b)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Пока нет доступной информации", reply_markup=a)
            # инфо обо мне
        elif call.data == 'info_about_me':
            info_me_markup = types.InlineKeyboardMarkup()
            item_info_about_me = [
                types.InlineKeyboardButton(text="VK", url='https://vk.com/mrgferintin'),
                types.InlineKeyboardButton(text="t.me", url='https://t.me/GFE_rin'),
                types.InlineKeyboardButton(text="WhatsApp", url='https://wa.me/+79049473690'),
                types.InlineKeyboardButton(text="⏮Назад", callback_data="cancel")
            ]
            info_me_markup.add(*item_info_about_me)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Связь с создателем\n""Лучше не связывайся с ним.", reply_markup=info_me_markup)
            # НАЗАД в меню старт
        elif call.data == 'cancel':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            return network(call.message)


# /sub - подписаться
@bot.message_handler(commands=['sub'])
def subscribe(message: types.Message):
    # если он уже есть, то просто обновляем ему статус подписки
    db.update_subscription(message.from_user.id, True)
    bot.send_message(message.chat.id,
                     "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# /unsub - отписаться
@bot.message_handler(commands=['unsub'])
def unsubscribe(message: types.Message):
    if not bool(len(db.subscriber_exists(message.from_user.id))):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы успешно отписаны от рассылки.")


# /getsub - получение всех подписчиков
@bot.message_handler(commands=['getsub'])
def getsub(message: types.Message):
    bot.send_message(message.chat.id, " \n".join(map(str, db.get_subscriptions())))


# /getuser - получение всех ПОЛЬЗОВАТЕЛЕЙ
@bot.message_handler(commands=['getuser'])
def getsub(message: types.Message):
    i = 0
    try:
        while 1:
            if bool(db.get_user()[i][5]):
                bot.send_message(message.chat.id, str(i+1) + ". " + "".join(map(str, db.get_user()[i][4])) + ' ' + "".join(map(str, db.get_user()[i][5])))
            else:
                bot.send_message(message.chat.id, str(i+1) + ". " + "".join(map(str, db.get_user()[i][4])))
            i += 1
    except Exception as e:
        print(e)
    finally:
        if i:
            bot.send_message(message.chat.id, "Все кто был здесь)")
        else:
            bot.send_message(message.chat.id, "Пользователей нет в базе данных, либо какая-то ошибка")


# /delete_user
@bot.message_handler(commands=['delete_user'])
def delete_user(message: types.Message):
    if bool(len(db.subscriber_exists(message.from_user.id))):
        db.delete_subscription(message.from_user.id)
        db.commit_subscription()
        bot.send_message(message.chat.id, "Пользователь удалён из базы данных")


# /referral
@bot.message_handler(commands=['referral'])
def referral(message):
    if not int(db.subscriber_exists(message.from_user.id)[0][6]):
        msg = bot.send_message(message.chat.id, "Введите реферальный код друга, если у вас нет кода введите 6:\n")
        bot.register_next_step_handler(msg, start_2)
    else:
        bot.send_message(message.chat.id, "Вы уже вводили реферальный код")
        bot.send_message(message.chat.id, "Ваш реферальный код - " + str(db.subscriber_exists(message.from_user.id)[0][0]))


def start_2(message):
    if bool(len(db.subscriber_exists_id(message.text))):
        db.referral_code_1(message.text, message.from_user.id)  # Добавляем реферальный код
        db.referral_code_2(message.text)  # Увеличиваем число подписчиков
        db.commit_subscription()
        bot.send_message(message.chat.id, 'Ваш друг успешно найден: \n' + " ".join(
            map(str, db.subscriber_exists_id(message.text))) + "\n Код подтверждён")
    else:
        bot.send_message(message.chat.id, "Пользователя с данным кодом не существует")


# /Вывод участников
@bot.message_handler(commands=['list_users'])
def getsub(message: types.Message):
    i = 0
    listUsers = types.InlineKeyboardMarkup()
    try:
        while 1:
            listUsers.add(types.InlineKeyboardButton(text=str("".join(map(str, db.get_user()[i][4]))), url=str('https://t.me/' + "".join(map(str, db.get_user()[i][3])))))
            # bot.send_message(message.chat.id, '@' + "".join(map(str, db.get_user()[i][3])))
            i+=1
    except Exception as e:
        print(e)
    finally:
        # bot.send_message(message.chat.id, "Все участники розыгрыша")
        bot.send_message(message.chat.id, "Ссылки на участников", reply_markup=listUsers)


# echo bot
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text + '. Я не знаю что мне с этим делать')


# очистка чата
# def clear(self, update, context):
#     new_message_id = message.message_id
#     while new_message_id > 1:
#         try:
#             context.bot.delete_message(chat_id=message.chat_id, message_id=new_message_id)
#         except Exception as error:
#             print(f'Message_id does not exist: {new_message_id} - {error}')
#         new_message_id = new_message_id - 1

if __name__ == '__main__':  # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
    try:
        bot.polling(none_stop=True)  # запуск бота
    except Exception as ex:
        print(ex)  # или import traceback; traceback.print_exc() для печати полной информации
        # time.sleep(15)
