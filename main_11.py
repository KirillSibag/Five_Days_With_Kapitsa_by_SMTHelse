import telebot           # для бота
import pickle            # для открытия файла с 
from pathlib import Path # для удаления неугодного файла
from PIL import Image    # для отправки фото пользователю
import time              # для высчитывания времени межу изменениями цвета
from telebot import types

st = time.time() - 100 # переменная измерения времени и его ограничения

data = []

bot = telebot.TeleBot('ТОКЕН')
moderId = # ID модератора, число

score = {}
sended = {}

@bot.message_handler(commands=['start']) # отслеживание команды
def any_msg(message):
    #global score
    score[message.chat.id] = 0
    sended[message.chat.id] = 0

    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="получить квест", callback_data="quest")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "получи квест", reply_markup=keyboard)


tasks = ["Поцелуй фото Капицы.", "Напиши 100 раз 'Люблю Капицу'", "Прыгни со скалы", "просто халявные очки", "сыграй 'К Элизе' на школьном рояле в ре-мажоре", "Спой Гимн Школы наизусть", "Станцуй Шведскую польку"]
from random import choice as ch
nowQuest = "что?"

# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "quest":
            keyboard = types.InlineKeyboardMarkup()
            #callback_button = types.InlineKeyboardButton(text="выполнен!", callback_data="ready")
            #keyboard.add(callback_button)
            global nowQuest
            nowQuest = ch(tasks)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "твой квест: "+nowQuest, reply_markup=keyboard)
            sended[call.message.chat.id] = 0

        if call.data == "ready":
            #global score
            try:
                score[call.message.chat.id] += 5
            except KeyError:
                score[call.message.chat.id] = 5

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "вам начислено 5 очков")
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="получить квест", callback_data="quest")
            callback_button1 = types.InlineKeyboardButton(text="очки", callback_data="score")
            keyboard.add(callback_button)
            keyboard.add(callback_button1)
            bot.send_message(call.message.chat.id, "получи квест", reply_markup=keyboard)

        if call.data == "score":
            #global score
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "у вас " + str(score[call.message.chat.id]) + " очков")
            except KeyError:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "у вас 0 очков")
                score[call.message.chat.id] = 0

            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="получить квест", callback_data="quest")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, "получи квест", reply_markup=keyboard)

        if call.message.chat.id == moderId:
            try:
                Id = int(call.data)
                if Id == -1:
                    #global score
                    try:
                        bot.send_message(chat_id=call.message.chat.id, text= "у вас " + str(score[call.message.chat.id]) + " очков, квест не засчитан")
                    except KeyError:
                        bot.send_message(chat_id=call.message.chat.id, text= "у вас 0 очков")
                        score[call.message.chat.id] = 0

                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="получить квест", callback_data="quest")
                    keyboard.add(callback_button)
                    bot.send_message(call.message.chat.id, "получи квест", reply_markup=keyboard)

                else:
                    Id = int(call.data)
                    #global score
                    try:
                        score[Id] += 5
                    except KeyError:
                        score[Id] = 5

                    bot.send_message(call.message.chat.id, "у вас " + str(score[Id]) + " очков, квест засчитан")

                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="получить квест", callback_data="quest")
                    keyboard.add(callback_button)
                    bot.send_message(call.message.chat.id, "получи квест", reply_markup=keyboard)

            except ValueError:
                print("VE")

@bot.message_handler(content_types=['photo'])
def photo(message):
    if message.photo and sended[message.chat.id] == 0:
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="подтвердить", callback_data= str(message.chat.id))
        callback_button1 = types.InlineKeyboardButton(text="опровергнуть", callback_data="-1")
        keyboard.add(callback_button)
        keyboard.add(callback_button1)

        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_photo(moderId, downloaded_file, caption="по квесту: " + nowQuest, reply_markup=keyboard, parse_mode="HTML")
        sended[message.chat.id] = 1

bot.polling(none_stop=True)
