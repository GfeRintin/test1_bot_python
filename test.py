from selenium import webdriver
import telebot
from telebot import types
import time





bot = telebot.TeleBot("5261331248:AAFoCVFVo41-crHgKcTTLdROF-AcVLjeYgs")


# Доступные команды
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Список доступных команд\n"
                                      "📲 /network - связь с нами\n"
                                      "📲 /help - Справка")


# help - справка
@bot.message_handler(commands=['help'])
def help(message):
    help_me = types.InlineKeyboardMarkup()
    help_Button = types.InlineKeyboardButton(text="Вот ссылки на связь с ним:", callback_data='info_about_me')
    help_me.add(help_Button)
    bot.send_message(message.chat.id, "Я помочь ничем не могу(\n"
                                      "Уж так меня запрограммировал мой создатель, но вы можете узнать у него что вам нужно",
                     reply_markup=help_me)


# start - таблица с информации о разных людях
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
            options = webdriver.ChromeOptions()

            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_argument("--disable-blink-features=AutomationControlled")

            options.add_argument(
                '--user-data-dir=C:/Users/Слава/AppData/Local/Google/Chrome/User Data')  # Тут изменить 'Слава' на ваше имя пользователя
            options.add_argument(
                '--profile-directory=Profile 1')  # Тут указывается профиль гугл хрома; по умолчанию - 1
            driver = webdriver.Chrome(executable_path=r"C:\Users\Слава\neptunemutual\chromedriverwin\chromedriver.exe",
                                      chrome_options=options)
            driver.get('https://vk.com/mrgferintin')
            time.sleep(30)
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            #                       text="Связь с создателем\n""Лучше не связывайся с ним.", reply_markup=info_me_markup)
            # # НАЗАД в меню старт
        elif call.data == 'cancel':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            return network(call.message)


# echo bot
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)


if __name__ == '__main__':
    bot.infinity_polling()
