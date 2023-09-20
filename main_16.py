import telebot           # для бота
import pickle            # для открытия файла
from pathlib import Path # для удаления файла
from telebot import types# клавиатура
from random import choice as ch
from random import randint as r
import math as m

score = {}

try:
    with open("data.pickle", "rb") as f:
        score = pickle.load(f)
except Exception:
    with open("data.pickle", "wb") as f:
        pickle.dump(score, f, protocol=pickle.HIGHEST_PROTOCOL)


bot = telebot.TeleBot('TOKEN')
moderId = #ID модератора

sended = {}

@bot.message_handler(commands=['start']) # отслеживание команды
def any_msg(message):
    try:
        n = score[message.chat.id]
    except KeyError:
        score[message.chat.id] = 0

    sended[message.chat.id] = 0
    global nowQuests
    nowQuests = []
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="получить квест", callback_data="quest")
    keyboard.add(callback_button)
    callback_button1 = types.InlineKeyboardButton(text="быстрый квест", callback_data="fquest")
    keyboard.add(callback_button1)
    bot.send_message(message.chat.id, "получи квест\nквестов нет.", reply_markup=keyboard)


tasks =  [f'Напиши неправильную расшифровку аббревиатуры {ch(["МЖК","ГБОУ","ДМШ","ВОШ","ИИ","МГУ","МФТИ","СКБ (Союз Капибарейцев)"])}']
tasks += ["Найди в школе фото Капицы.", "Напиши 20 раз 'Люблю Капицу'", "Прыгни со скалы", "Воткни одну ручку в другую", "Собери 3 чужих талончика на еду"]
tasks += ["Нарисуй цветок так круто, как только можешь", "Изобрази гуся", "Скушай школьный обед или завтрак полностью", "Найди резистор на 220Ом"]
tasks += ["Сложи два восьмеричных числа длиной не менее 5 символов", "Напиши решение уравнения 3 степени по теореме безе", "Сделай 10 бумажных корабликов", "Реши 3 квадратных уравнения"]


tasks += ["Попроси у случайного человека автограф."]
tasks += ["Принеси пять монет разных стран."]
tasks += ["Сделай фото, где кажется, что ты летишь."]
tasks += ["Принеси пять разных видов листьев."]
tasks += ["Узнай у человека, насколько он(а) счастлив(а) от 1 до 10 и почему."]
tasks += ["Попроси прохожего нарисовать тебя."]
tasks += ["Сделай селфи с собакой."]
tasks += ["Сделай фото с животным."]
tasks += [f"Найди пять предметов, которые начинаются на букву '{ch(['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У'])}'."]

nowQuests = []
fq = []

def sending(send_ID):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="квест", callback_data="quest")
    callback_button2 = types.InlineKeyboardButton(text="быстрый квест", callback_data="fquest")
    callback_button1 = types.InlineKeyboardButton(text="очки", callback_data="score")
    keyboard.add(callback_button)
    keyboard.add(callback_button2)
    keyboard.add(callback_button1)
    bot.send_message(send_ID, "получи квест", reply_markup=keyboard)

def ku():
    try:
        inn = r(0, 30)
        fir = r(0, 30)
        res = r(-20, 20)

        c = (2*inn*res)*(2*inn*res + (2*fir))/((0-4)*inn)
        res = (fir*(-1) + m.sqrt(fir**2 - (4*inn*c))) / (2*inn)  + (fir*(-1) - m.sqrt(fir**2 - (4*inn*c))) / (2*inn)

        if c == int(c) and res == int(res):
            if c >= 0:
                que = f"реши уравнение: {inn}x^2 + {fir}x + {c}"
            else:
                que = f"реши уравнение: {inn}x^2 + {fir}x - {c*(-1)}"

            return que, int(res)

        else:
            return ku()


    except ZeroDivisionError:
        return ku()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    update(score)

    if call.message:
        if call.data == "fquest":
            keyboard = types.InlineKeyboardMarkup()

            que, res = ku()

            global fq
            fq = [res]

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= f"твой квест:\n{que}", reply_markup=keyboard)
            sended[call.message.chat.id] = 2

        if call.data == "quest":
            keyboard = types.InlineKeyboardMarkup()
            global nowQuests
            global tasks

            que = ch(tasks)
            nowQuests.append(que)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= f"твой квест:\n{que}", reply_markup=keyboard)
            sended[call.message.chat.id] = 1

        if call.data == "score":
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "у вас " + str(score[call.message.chat.id]) + " очков")
            except KeyError:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "у вас 0 очков")
                score[call.message.chat.id] = 0

            sending(call.message.chat.id)

        if call.message.chat.id == moderId:
            try:
                Id = call.data
                if " -1" in Id:
                    Id = int(Id.replace(" -1", ""))
                    try:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "отвергнуто")

                    except:
                        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media = types.InputMediaPhoto(open("s.png", "rb")))

                    try:
                        bot.send_message(chat_id=Id, text= f"у вас {score[Id]} очков, квест не засчитан")

                    except KeyError:
                        bot.send_message(chat_id=Id, text= "у вас 0 очков, квест не засчитан")
                        score[Id] = 0

                else:
                    Id = int(call.data)
                    try:
                        score[Id] += 5
                    except KeyError:
                        score[Id] = 5

                    update(score)
                    try:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "подтверждено")
                    except:
                        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media = types.InputMediaPhoto(open("s.png", "rb")))

                    bot.send_message(Id, "у вас " + str(score[Id]) + " очков, квест засчитан")




            except ValueError:
                print("VE")

def update(score):
    # удаляем файл с устаревшими данными
    file= Path("data.pickle")
    file.unlink()

    # обновляем файл
    try:
        with open("data.pickle", "wb") as f:
            pickle.dump(score, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)



@bot.message_handler(content_types=['video', 'photo', 'text'])
def photo(message):
    try:
        if sended[message.chat.id] == 1 and len(nowQuests)>0:
            if message.photo:
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="подтвердить", callback_data= str(message.chat.id))
                callback_button1 = types.InlineKeyboardButton(text="опровергнуть", callback_data=str(message.chat.id)+" -1")
                keyboard.add(callback_button)
                keyboard.add(callback_button1)

                photo = message.photo[-1]
                file_id = photo.file_id
                file_info = bot.get_file(file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                bot.send_photo(moderId, downloaded_file, caption="по квесту: " + nowQuests[0], reply_markup=keyboard, parse_mode="HTML")
                nowQuests.remove(nowQuests[0])
                sended[message.chat.id] = 0

                sending(message.chat.id)

            elif message.video:
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="подтвердить", callback_data= str(message.chat.id))
                callback_button1 = types.InlineKeyboardButton(text="опровергнуть", callback_data=str(message.chat.id)+" -1")
                keyboard.add(callback_button)
                keyboard.add(callback_button1)

                video = message.video
                file_id = video.file_id
                file_info = bot.get_file(file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                bot.send_video(moderId, downloaded_file, caption="по квесту: " + nowQuests[0], reply_markup=keyboard, parse_mode="HTML")
                nowQuests.remove(nowQuests[0])
                sended[message.chat.id] = 0

                sending(message.chat.id)

            elif message.text:
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="подтвердить", callback_data= str(message.chat.id))
                callback_button1 = types.InlineKeyboardButton(text="опровергнуть", callback_data=str(message.chat.id)+" -1")
                keyboard.add(callback_button)
                keyboard.add(callback_button1)

                bot.send_message(moderId, text= f"Письменный ответ:\n{message.text}\nПо квесту:\n{nowQuests[0]}", reply_markup=keyboard)
                nowQuests.remove(nowQuests[0])
                sended[message.chat.id] = 0

                sending(message.chat.id)

        global fq
        if sended[message.chat.id] == 2 and len(fq)>0:
            if message.text:
                if str(fq[0]) in message.text:
                    try:
                        score[message.chat.id] += 5
                    except KeyError:
                        score[message.chat.id] = 5

                    bot.send_message(message.chat.id, "у вас " + str(score[message.chat.id]) + " очков, квест засчитан")

                else:
                    try:
                        bot.send_message(chat_id=message.chat.id, text= f"у вас {score[message.chat.id]} очков, квест не засчитан")
                    except KeyError:
                        bot.send_message(chat_id=message.chat.id, text= "у вас 0 очков, квест не засчитан")
                        score[message.chat.id] = 0

                fq = []

                sended[message.chat.id] = 0

                sending(message.chat.id)

            update(score)

    except Exception as EX:
        print(EX)
        bot.send_message(chat_id=message.chat.id, text= "выполните /start")

bot.polling(none_stop=True)
