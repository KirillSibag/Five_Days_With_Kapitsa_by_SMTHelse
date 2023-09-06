import telebot           # для бота
import pickle            # для открытия файла с цветами поля
from pathlib import Path # для удаления неугодного файла
import time              # для высчитывания времени межу изменениями цвета
from telebot import types
from random import choice as ch

score = {}

try:
    with open("data.pickle", "rb") as f:
        score = pickle.load(f)
except Exception:
    with open("data.pickle", "wb") as f:
        pickle.dump(score, f, protocol=pickle.HIGHEST_PROTOCOL)


bot = telebot.TeleBot('ТОКЕН')
moderId = #id модератора

sended = {}

@bot.message_handler(commands=['start']) # отслеживание команды
def any_msg(message):
    #global score
    try:
        n = score[message.chat.id]
    except KeyError:
        score[message.chat.id] = 0

    sended[message.chat.id] = 0

    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="получить квест", callback_data="quest")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "получи квест", reply_markup=keyboard)


tasks =  ["Найди в школе фото Капицы.", "Напиши 20 раз 'Люблю Капицу'", "Прыгни со скалы", "Воткни одну ручку в другую", "Собери 3 чужих талончика на еду"]
tasks += ["Нарисуй цветок так круто, как только можешь", "Изобрази гуся", "Скушай школьный обед или завтрак полностью", "Найди резистор на 220Ом"]
tasks += ["Сложи два восьмеричных числа длиной не менее 5 символов", "Напиши решение уравнения 3 степени по теореме безе", "Сделай 10 бумажных корабликов", "Реши 3 квадратных уравнения"]

nowQuest = ""

def sending(send_ID):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="квест", callback_data="quest")
    callback_button1 = types.InlineKeyboardButton(text="очки", callback_data="score")
    keyboard.add(callback_button)
    keyboard.add(callback_button1)
    bot.send_message(send_ID, "получи квест", reply_markup=keyboard)

# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "quest":
            keyboard = types.InlineKeyboardMarkup()
            global nowQuest
            nowQuest = ch(tasks)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "твой квест: "+nowQuest, reply_markup=keyboard)
            sended[call.message.chat.id] = 0

        if call.data == "score":
            #global score
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "у вас " + str(score[call.message.chat.id]) + " очков")
            except KeyError:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "у вас 0 очков")
                score[call.message.chat.id] = 0

            sending(call.message.chat.id)

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

                    sending(call.message.chat.id)

                else:
                    Id = int(call.data)
                    try:
                        score[Id] += 5
                    except KeyError:
                        score[Id] = 5

                    bot.send_message(call.message.chat.id, "у вас " + str(score[Id]) + " очков, квест засчитан")

                    sending(call.message.chat.id)

            except ValueError:
                print("VE")

        # удаляем файл с устаревшими данными
        file= Path("data.pickle")
        file.unlink()

        # обновляем файл
        try:
            with open("data.pickle", "wb") as f:
                pickle.dump(score, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)



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

        sending(message.chat.id)

bot.polling(none_stop=True)
