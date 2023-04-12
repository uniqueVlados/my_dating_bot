from cities import Cities
from database import Database
from read_tags import Read_tags

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "6167157380:AAEBoL1PRfL4HlauT1MOyTPHlbos_E9C9Sg"
cities_obj = Cities("other/russia.json")
CITIES = cities_obj.get_cities()
db = Database("user.db")


# FUNCTION
def correct_name(name):
    if len(name) <= 10 and name[0].isupper():
        return True
    return False


def correct_mbti(ans):
    if len(ans) == 3:
        for s in ans:
            if not (s == "Д" or s == "Н"):
                return False
        return True
    else:
        return False


def right_letter(ans):
    if ans.count("Д") >= 2:
        return True
    return False


def get_profile(user_id):
    profile_list = db.get_my_profile(user_id)
    return f"Ваша анкета\n--------\n{profile_list[2]}\n{profile_list[3]}\n{profile_list[4]}\n{profile_list[5]}\n" \
           f"{profile_list[6]}\nТеги\n-------------\n{profile_list[7]}"


def correct_input_tags(ans, rd, user_id):
    ans_list = ans.split(", ")
    rd_list = list(map(lambda s: s.replace("\n", ""), rd.get_tags_list()))
    print(ans_list)
    print(rd_list)
    for tag in ans_list:
        if tag not in rd_list:
            return False
    return True


def profile_kb(user1, user2, user3, user4, user5):
    profile_1 = InlineKeyboardButton(user1, callback_data='user1')
    profile_2 = InlineKeyboardButton(user2, callback_data='user2')
    profile_3 = InlineKeyboardButton(user3, callback_data='user3')
    profile_4 = InlineKeyboardButton(user4, callback_data='user4')
    profile_5 = InlineKeyboardButton(user5, callback_data='user5')

    CHECK_PROFILES_KB = InlineKeyboardMarkup(row_width=1)
    CHECK_PROFILES_KB.add(profile_1, profile_2, profile_3, profile_4, profile_5)

    return CHECK_PROFILES_KB



# BUTTONS
FORM_BTN = KeyboardButton("Заполнить анкету")
# ----
EDIT_NAME_BTN = KeyboardButton("Имя")
EDIT_CITY_BTN = KeyboardButton("Город")
EDIT_AGE_BTN = KeyboardButton("Возраст")
EDIT_DESC_BTN = KeyboardButton("Описание")
EDIT_MBTI_BTN = KeyboardButton("MBTI")
MBTI_AGAIN_BTN = KeyboardButton("Пройти тест")
EDIT_TAGS_BTN = KeyboardButton("Теги")
# ----
SEARCH_BTN = KeyboardButton("Поиск🔎")
PROFILE_BTN = KeyboardButton("Профиль📝")
MATCH_BTN = KeyboardButton("Match👥")
HELP_BNT = KeyboardButton("Помощь💬")
# ----
INTERESTS_BTN = KeyboardButton("Интересы")
LIFESTYLE_BTN = KeyboardButton("Образ жизни")
LIFEPOS_BTN = KeyboardButton("Жизненная позиция")
NEEDS_BTN = KeyboardButton("Потребности")
MUSIC_BTN = KeyboardButton("Музыка")
FILMS_BTN = KeyboardButton("Фильмы")
BOOKS_BTN = KeyboardButton("Книги")
GAMES_BTN = KeyboardButton("Игры")
FOOD_BTN = KeyboardButton("Еда")
DEL_TAGS = KeyboardButton("Удалить тег")

# ----
BACK_BTN = KeyboardButton("Назад🔙")
# ----
LIKE_BTN = KeyboardButton("❤")
SKIP_BTN = KeyboardButton("❌")

# KEYBOARDS
FORM_KB = ReplyKeyboardMarkup(resize_keyboard=True)
FORM_KB.add(FORM_BTN)
MENU_KB = ReplyKeyboardMarkup(resize_keyboard=True)
MENU_KB.add(SEARCH_BTN, MATCH_BTN, HELP_BNT, PROFILE_BTN)
CHECK_USERS = ReplyKeyboardMarkup(resize_keyboard=True)
EDIT_PROFILE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
EDIT_PROFILE_KB.add()

# ----
HELP_KB = ReplyKeyboardMarkup(resize_keyboard=True)
HELP_KB.add(BACK_BTN)
# ----
PROFILE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
PROFILE_KB.add(EDIT_NAME_BTN, EDIT_CITY_BTN, EDIT_AGE_BTN, EDIT_DESC_BTN, EDIT_MBTI_BTN, EDIT_TAGS_BTN)
# ----
EDIT_MBTI_KB = ReplyKeyboardMarkup(resize_keyboard=True)
EDIT_MBTI_KB.add(MBTI_AGAIN_BTN, BACK_BTN)
# TAGS
TAGS_KB = ReplyKeyboardMarkup(resize_keyboard=True)
TAGS_KB.add(INTERESTS_BTN, LIFESTYLE_BTN, LIFEPOS_BTN, NEEDS_BTN, MUSIC_BTN, FILMS_BTN, BOOKS_BTN, GAMES_BTN, FOOD_BTN,
            DEL_TAGS, BACK_BTN)

RATE_PROFILE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
RATE_PROFILE_KB.add(LIKE_BTN, SKIP_BTN)

# ACTIVE_KB = ReplyKeyboardMarkup(resize_keyboard=True)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    db.add_user_state(user_id, "start", "False")
    db.add_user(user_id, username)
    await message.reply(f"Приветствуем, {message.from_user.username}!\nВ данном боте вы "
                        f"можете познакомиться", reply_markup=FORM_KB)


@dp.message_handler(commands=['menu'])
async def menu_(message: types.Message):
    user_id = message.from_user.id
    db.replace_state(user_id, "wait")
    await message.reply(f"Вернулись в главное меню", reply_markup=MENU_KB)


@dp.message_handler()
async def info(message: types.Message):
    user_id = message.from_user.id

    # Input profile
    if message.text == "Заполнить анкету" and db.get_state(user_id) == "start":
        db.replace_state(user_id, "name")
        await message.reply("Введите имя: ")
    elif db.get_state(user_id) == "name":
        if correct_name(message.text):
            db.replace_state(user_id, "city")
            db.replace_name(user_id, message.text)
            await message.reply("Ваше имя принято!\nВведите теперь название города")
        else:
            await message.reply("Имя должно быть меньше 10 символов и начинаться с заглавной буквы")
    elif db.get_state(user_id) == "city":
        if message.text in CITIES:
            db.replace_state(user_id, "age")
            db.replace_city(user_id, message.text);
            await message.reply("Ваш город принят!\nВведите теперь свой возраст")
        else:
            await message.reply(f"Город не обнаружен.\nДоступные города:\n{', '.join(CITIES)}")
    elif db.get_state(user_id) == "age":
        if message.text.isdigit() and 18 <= int(message.text) <= 80:
            db.replace_state(user_id, "description")
            db.replace_age(user_id, message.text);
            await message.reply("Введите пару слов о себе")
    elif db.get_state(user_id) == "description" or db.get_state(user_id) == "edit_mbti":
        if message.text != "Пройти тест":
            db.replace_description(user_id, message.text)
        db.replace_state(user_id, "mbti_ans1")
        db.replace_mbti(user_id, "")
        await message.reply("Ответить на вопросы нужно в формате(ДНД/ДДД/ННД), где\nД - СОГЛАСИЕ\nН - НЕСОГЛАСИЕ")
        await message.reply("Экстраверт🔄Интроверт\n\n"
                            "1️⃣В компаниях вы любите быть в центре внимания\n\n"
                            "2️⃣Вы скорее предпочтете светское мероприятие, нежели время наедине с собой\n\n"
                            "3️⃣Вы чувствуете себя 'заряженным' энергией после времени, проведенного в группе людей")
    elif db.get_state(user_id) == "mbti_ans1":
        ans = message.text
        if correct_mbti(ans):
            db.replace_state(user_id, "mbti_ans2")
            if right_letter(ans):
                db.replace_mbti(user_id, "E")
            else:
                db.replace_mbti(user_id, "I")

            await message.reply("Интуит🔄Сенсорик\n\n"
                                "1️⃣Ваши мысли, как правило, сосредоточены на событиях реального мира, а не на гипотетических возможностях\n\n"
                                "2️⃣Вы часто тратите свое время на фантазии\n\n"
                                "3️⃣Вам не дают покоя неизведанные идеи и грандиозные планы")
        else:
            await message.reply("Вы ввели в  неферном формате!\n" +
                                "Ответить на вопросы нужно в формате(ДНД/ДДД/ННД), где\nД - СОГЛАСИЕ\nН - НЕСОГЛАСИЕ")
    elif db.get_state(user_id) == "mbti_ans2":
        ans = message.text
        if correct_mbti(ans):
            db.replace_state(user_id, "mbti_ans3")
            if right_letter(ans):
                db.replace_mbti(user_id, db.get_mbti(user_id) + "N")
            else:
                db.replace_mbti(user_id, db.get_mbti(user_id) + "S")
            await message.reply("Чувства🔄Логика\n\n"
                                "1️⃣Во время спора чувства других людей должны быть важнее правды\n\n"
                                "2️⃣Ваши эмоции контролируют вас больше, чем вы их\n\n"
                                "3️⃣Вы принимаете решения опираясь на логику, а не личные ценности или чувства")
        else:
            await message.reply("Вы ввели в  неферном формате!\n" +
                                "Ответить на вопросы нужно в формате(ДНД/ДДД/ННД), где\nД - СОГЛАСИЕ\nН - НЕСОГЛАСИЕ")
    elif db.get_state(user_id) == "mbti_ans3":
        ans = message.text
        if correct_mbti(ans):
            db.replace_state(user_id, "mbti_ans4")
            if right_letter(ans):
                db.replace_mbti(user_id, db.get_mbti(user_id) + "F")
            else:
                db.replace_mbti(user_id, db.get_mbti(user_id) + "T")
            await message.reply("Импровизация🔄Планирование\n\n"
                                "1️⃣Вы продумываете свои планы проведения досуга до мелочей\n\n"
                                "2️⃣Вы, вероятнее, будете импровизировать, нежели тратить время на разработку детального плана\n"
                                "3️⃣Для вас важнее наличие четкого списка дел, нежели сохранение возможности выбора")
        else:
            await message.reply("Вы ввели в  неферном формате!\n" +
                                "Ответить на вопросы нужно в формате(ДНД/ДДД/ННД), где\nД - СОГЛАСИЕ\nН - НЕСОГЛАСИЕ")
    elif db.get_state(user_id) == "mbti_ans4":
        ans = message.text
        if correct_mbti(ans):
            db.replace_state(user_id, "mbti_ans5")
            if right_letter(ans):
                db.replace_mbti(user_id, db.get_mbti(user_id) + "P")
            else:
                db.replace_mbti(user_id, db.get_mbti(user_id) + "J")
            await message.reply("Turbulent🔄Assertive\n\n"
                                "1️⃣Если кто-то сразу не ответил на ваше сообщение, вы начинаете волноваться, что написали что-то не то\n"
                                "2️⃣Вы сильно переживаете по поводу того, что думают о вас другие люди\n\n"
                                "3️⃣Вы часто сожалеете о своих ошибках")
        else:
            await message.reply("Вы ввели в  неферном формате!\n" +
                                "Ответить на вопросы нужно в формате(ДНД/ДДД/ННД), где\nД - СОГЛАСИЕ\nН - НЕСОГЛАСИЕ")
    elif db.get_state(user_id) == "mbti_ans5":
        ans = message.text
        if correct_mbti(ans):
            db.replace_state(user_id, "wait")
            db.replace_active(user_id, "True")
            if right_letter(ans):
                db.replace_mbti(user_id, db.get_mbti(user_id) + "T")
            else:
                db.replace_mbti(user_id, db.get_mbti(user_id) + "A")
            await message.reply(get_profile(user_id), reply_markup=MENU_KB)
        else:
            await message.reply("Вы ввели в  неферном формате!\n" +
                                "Ответить на вопросы нужно в формате(ДНД/ДДД/ННД), где\nД - СОГЛАСИЕ\nН - НЕСОГЛАСИЕ")



    # Edit Profile
    elif message.text == "Профиль📝" and db.get_state(user_id) == "wait":
        db.replace_state(user_id, "edit")
        await message.reply(get_profile(user_id) + f"\nВыберите, что хотите изменить:  ", reply_markup=PROFILE_KB)
    elif message.text == "Имя" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_name")
        await message.reply("Введите новое имя: ")
    elif db.get_state(user_id) == "edit_name":
        if correct_name(message.text):
            db.replace_state(user_id, "wait")
            db.replace_name(user_id, message.text)
            await message.reply("Ваше имя изменено!")
            await message.reply(get_profile(user_id), reply_markup=MENU_KB)
        else:
            await message.reply("Имя должно быть меньше 10 символов и начинаться с заглавной буквы")
    elif message.text == "Город" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_city")
        await message.reply("Введите новый город: ")
    elif db.get_state(user_id) == "edit_city" and message.text in CITIES:
        db.replace_state(user_id, "wait")
        db.replace_city(user_id, message.text)
        await message.reply("Ваш город изменен!")
        await message.reply(get_profile(user_id), reply_markup=MENU_KB)
    elif message.text == "Возраст" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_age")
        await message.reply("Введите новый возраст: ")
    elif db.get_state(user_id) == "edit_age":
        if message.text.isdigit() and 18 <= int(message.text) <= 80:
            db.replace_state(user_id, "wait")
            db.replace_age(user_id, message.text)
            await message.reply("Ваш возраст изменен!")
            await message.reply(get_profile(user_id), reply_markup=MENU_KB)
    elif message.text == "Описание" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_desc")
        profile_list = db.get_my_profile(user_id)
        await message.reply(f"Прошлое описание: {profile_list[5]}\nВведите новое описание:")
    elif db.get_state(user_id) == "edit_desc":
        db.replace_state(user_id, "wait")
        db.replace_description(user_id, message.text)
        await message.reply(get_profile(user_id), reply_markup=MENU_KB)
    elif message.text == "MBTI" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_mbti")
        profile_list = db.get_my_profile(user_id)
        await message.reply(f"Ваш MBTI: {profile_list[6]}", reply_markup=EDIT_MBTI_KB)
    elif db.get_state(user_id) == "edit_mbti" and message.text == "Назад🔙":
        db.replace_state(user_id, "edit")
        await message.reply(f"Выберите, что хотите изменить:  ", reply_markup=PROFILE_KB)

    # HELP
    elif db.get_state(user_id) == "wait" and message.text == "Помощь💬":
        db.replace_state(user_id, "help")
        await message.reply(f"Отвечу на все вопросы\n@gregoryexmachina", reply_markup=HELP_KB)
    elif db.get_state(user_id) == "help" and message.text == "Назад🔙":
        db.replace_state(user_id, "wait")
        await message.reply(f"Вернулись в главное меню", reply_markup=MENU_KB)

    # TAGS
    elif db.get_state(user_id) == "edit" and message.text == "Теги":
        db.replace_state(user_id, "tags")
        await message.reply(f"Выберите раздел", reply_markup=TAGS_KB)
    elif db.get_state(user_id) == "tags" and message.text == "Назад🔙":
        db.replace_state(user_id, "wait")
        await message.reply(f"Вернулись в главное меню", reply_markup=MENU_KB)
    # del tag
    elif db.get_state(user_id) == "tags" and message.text == "Удалить тег":
        db.replace_state(user_id, "del_tag")
        await message.reply(f"ТЕГИ:\n{db.get_my_profile(user_id)[7]}\n-----------------\n"
                            f"Введите тег, которые хотите удалить", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "del_tag":
        ans = message.text
        if ans in db.get_tags(user_id).split(", "):
            db.replace_state(user_id, "tags")
            tags_list = db.get_tags(user_id).split(", ")
            tags_list.remove(ans)
            db.add_tags(user_id, ", ".join(tags_list))
            await message.reply(f"Тег удалён\n---------------\n{get_profile(user_id)}", reply_markup=TAGS_KB)
        else:
            db.replace_state(user_id, "tags")
            await message.reply(f"Данного тега нет", reply_markup=TAGS_KB)
    # -----
    elif db.get_state(user_id) == "tags" and message.text == "Интересы":
        db.replace_state(user_id, "edit_interests")
        tags = Read_tags("other/interests.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_interests":
        ans = message.text
        tags = Read_tags("other/interests.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")

    elif db.get_state(user_id) == "tags" and message.text == "Музыка":
        db.replace_state(user_id, "edit_music")
        tags = Read_tags("other/music.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_music":
        ans = message.text
        tags = Read_tags("other/music.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")

    elif db.get_state(user_id) == "tags" and message.text == "Фильмы":
        db.replace_state(user_id, "edit_films")
        tags = Read_tags("other/films.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_films":
        ans = message.text
        tags = Read_tags("other/films.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")

    elif db.get_state(user_id) == "tags" and message.text == "Сериалы":
        db.replace_state(user_id, "edit_series")
        tags = Read_tags("other/series.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_films":
        ans = message.text
        tags = Read_tags("other/series.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")

    elif db.get_state(user_id) == "tags" and message.text == "Книги":
        db.replace_state(user_id, "edit_books")
        tags = Read_tags("other/books.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_books":
        ans = message.text
        tags = Read_tags("other/books.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")

    elif db.get_state(user_id) == "tags" and message.text == "Игры":
        db.replace_state(user_id, "edit_games")
        tags = Read_tags("other/games.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_games":
        ans = message.text
        tags = Read_tags("other/games.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")

    elif db.get_state(user_id) == "tags" and message.text == "Еда":
        db.replace_state(user_id, "edit_food")
        tags = Read_tags("other/food.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_food":
        ans = message.text
        tags = Read_tags("other/food.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")
    elif db.get_state(user_id) == "tags" and message.text == "Жизненная позиция":
        db.replace_state(user_id, "edit_lifepos")
        tags = Read_tags("other/lifepos.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_lifepos":
        ans = message.text
        tags = Read_tags("other/lifepos.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")

    elif db.get_state(user_id) == "tags" and message.text == "Потребности":
        db.replace_state(user_id, "edit_needs")
        tags = Read_tags("other/needs.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_needs":
        ans = message.text
        tags = Read_tags("other/needs.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")

    elif db.get_state(user_id) == "tags" and message.text == "Образ жизни":
        db.replace_state(user_id, "edit_lifestyle")
        tags = Read_tags("other/lifestyle.txt")
        await message.reply(f"Выберите любое количество из представленных тегов. Теги вводить через запятую.\n\n"
                            f"{''.join(tags.get_tags_list())}", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_state(user_id) == "edit_lifestyle":
        ans = message.text
        tags = Read_tags("other/lifestyle.txt")
        if correct_input_tags(ans, tags, user_id):
            db.replace_state(user_id, "wait")
            if db.get_tags(user_id) is not None:
                db.add_tags(user_id, db.get_tags(user_id) + ", " + ans)
            else:
                db.add_tags(user_id, ans)
            await message.reply(f"Теги добавлены", reply_markup=MENU_KB)
        else:
            await message.reply(
                f"Теги введены в неверном формате/введён несуществующий тэг/тэг уже есть\nПовторите попытку!")

    # CHECK PROFILES

    elif db.get_state(user_id) == "wait" and message.text == "Поиск🔎":
        db.replace_state(user_id, "search")
        p1 = db.get_random_profile(user_id)
        p2 = db.get_random_profile(user_id)
        p3 = db.get_random_profile(user_id)
        p4 = db.get_random_profile(user_id)
        p5 = db.get_random_profile(user_id)
        await message.reply(f"Сегодня вам доступны анкеты", reply_markup=profile_kb(p1[2] + " " + p1[6], "2", "3", "4", "5"))




    # freeze and active profile
    # elif db.get_state(user_id) == "wait" and message.text == "Скрыть анкету":
    #     db.replace_active(user_id, "False")
    #     await message.reply(f"Ваша анкета скрыта. Вы не можете смотреть других участников и поставленные лайки.\n"
    #                         f"Другие пользователи Вас не видят.\n"
    #                         f"Ваши данные сохранены, Вы всегда можете к нам вернуться.",
    #                         reply_markup=ACTIVE_KB)
    # elif db.get_state(user_id) == "wait" and message.text == "Активировать":
    #     db.replace_active(user_id, "True")
    #     await message.reply(f"Ваша анкета снова видна в поиске!", reply_markup=MENU_KB)



@dp.callback_query_handler()
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data
    print(code)
    if code == "user1":
        await bot.send_message(callback_query.from_user.id, reply_markup=RATE_PROFILE_KB)


if __name__ == '__main__':
    executor.start_polling(dp)
