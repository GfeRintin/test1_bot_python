import telebot
from telebot import types
import time
import sqlite3

import sys

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, r"C:\Users\Слава\test1_bot_python\DB")

from SQLDateBase import SQLighter
import TOKEN

bot = telebot.TeleBot(TOKEN.Token)

# инициализируем соединение с БД
db = SQLighter(TOKEN.DB)


# Доступные команды
@bot.message_handler(commands=['start'])
def start(message):
    # Регистрируем пользователя
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        bot.send_message(message.chat.id, 'Привет, ' + str(message.from_user.first_name) + '!')
        db.add_subscriber(message.from_user.id, username=message.from_user.username,
                          first_name=message.from_user.first_name)

    bot.send_message(message.chat.id, "Список доступных команд\n"
                                      "📲 /network - связь с нами\n"
                                      "📲 /help - Справка\n"
                                      "/sub - подписаться на уведомления\n"
                                      "/unsub - отписаться от уведомлений")


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
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы успешно отписаны от рассылки.")


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


# echo bot
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text + '. Я не знаю что мне с этим делать')


if __name__ == '__main__':  # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
    try:
        bot.polling(none_stop=True)  # запуск бота
    except Exception as ex:
        print(ex)  # или import traceback; traceback.print_exc() для печати полной информации
        # time.sleep(15)
