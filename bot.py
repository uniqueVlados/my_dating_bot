from cities import Cities
from database import Database

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "6167157380:AAEBoL1PRfL4HlauT1MOyTPHlbos_E9C9Sg"
cities_obj = Cities("other/russia.json")
CITIES = cities_obj.get_cities()
db = Database("user.db")
TAGS_STR = "Меломан0\nЛюбитель кино0\nГик0\nГеймер0\nЛюбитель аниме0\nКнижный червь0\nГурман0\nЛюбитель искусства0\n" \
           "Творческий человек0\nЛюбитель технологий0\nЛюбитель науки0\nПредприниматель0\nЛюбитель спорта0\n" \
           "Путешественник0\nМодник0\nЛюбитель кошек0\nЛюбитель собак0\nСтудент0\nТрудоголик0\nМемолог0\nБудущий полиглот0\n" \
           "Духовный искатель0\nДиванный политолог0\nКурю0\nПью0"
MBTI1 = "Гриша:\n" \
        "Общительный и активный\n" \
        "Ориентирован на внешний мир и событияБыстро адаптируется к новым ситуациям и людям\n" \
        "Извлекает энергию из взаимодействия с окружающими\n\n" \
        "Саша:\nПредпочитает маленькие группы и интимные обстановки\n" \
        "Тратит время на размышления и самоанализ\n" \
        "Может быть тихой и сдержанной в общении\n" \
        "Нуждается в личном пространстве для восстановления энергии\n\n"

MBTI2 = "Гриша:\n" \
        "Ориентирован на общие идеи и возможности\n" \
        "При принятии решений полагается на интуицию и воображение\n" \
        "Размышляет о будущем и том, что могло бы быть\n" \
        "Предпочитает теории и абстрактные понятия\n\n" \
        "Саша:\n" \
        "Фокусируется на реальном мире и конкретных деталях\n" \
        "Опирается на опыт и здравый смысл при принятии решений\n" \
        "Предпочитает практичность и конкретные действия\n" \
        "Имеет наслаждаться моментом\n\n"

MBTI3 = "Гриша:\n" \
        "Принимает решения, исходя из личных ценностей и чувств\n" \
        "Чуткий к эмоциям других людей\n" \
        "Старается создать гармоничную атмосферу вокруг себя\n" \
        "Дипломатичен и умеет находить компромиссы\n\n" \
        "Саша:\n" \
        "Делает выбор на основе логики и объективного анализа" \
        "\nЦенит честность и прямоту" \
        "\nТрудности и противоречия видит как вызовы, а не препятствия" \
        "\nИщет наиболее эффективные и практичные решения\n\n"

MBTI4 = "Гриша:" \
        "\nГибкий и адаптивный к переменам" \
        "\nОценивает разные варианты перед принятием решения" \
        "\nПредпочитает открытость и возможность изменить планы" \
        "\nКомфортно чувствует себя в менее структурированных ситуациях" \
        "\n\nСаша:" \
        "\nПланирует и ставит цели на будущее" \
        "\nПредпочитает четкие рамки и порядок" \
        "\nОрганизована и ответственна" \
        "\nСтарается доводить начатое дело до конца\n\n"

MBTI5 = "•Склонен к переживаниям и самокритике" \
        "\nБеспокоится о том, что другие могут о нем думать" \
        "\nВосприимчив к стрессу и изменениям" \
        "\nСтремится к совершенству и работает над улучшением своих недостатков" \
        "\n\nСаша:" \
        "\nОбладает высоким уровнем самоуверенности и спокойствия" \
        "\nМеньше заботится о мнении окружающих" \
        "\nЛегко преодолевает стресс и быстро восстанавливается после неудач" \
        "\nПринимает свои сильные и слабые стороны, считая их нормальными\n\n"

# FUNCTION
def correct_name(name):
    if len(name) <= 10 and name[0].isupper():
        return True
    return False


def get_profile(user_id):
    profile_list = db.get_my_profile(user_id)
    return f"{profile_list[2]}\n{profile_list[3]}\n{profile_list[4]}\n{profile_list[5]}\n" \
           f"{profile_list[6]}\n{profile_list[7]}"


def profile_kb(user_id):
    CHECK_PROFILES_KB = InlineKeyboardMarkup(row_width=1)

    for i in range(1, 11):
        profile = db.get_random_profile(user_id)
        CHECK_PROFILES_KB.add(InlineKeyboardButton(profile[1] + " " + profile[6], callback_data=f'user{i}'))

    return CHECK_PROFILES_KB


def get_tags(tags_list):
    TAGS_KB = InlineKeyboardMarkup(row_width=2)

    for tag_tuple in tags_list:
        if tag_tuple[1] == 0:
            TAGS_KB.add(InlineKeyboardButton(tag_tuple[0], callback_data=tag_tuple[0]))
        else:
            TAGS_KB.add(InlineKeyboardButton(tag_tuple[0] + "✅", callback_data=tag_tuple[0]))

    return TAGS_KB


def list_tags_to_str(tags_list):
    tags = ""
    for t in tags_list:
        tags += t[0] + t[1] + "\n"
    return tags


def str_tags_to_list(tags_str):
    l = tags_str.split("\n")
    list_ = []
    for s in l:
        list_.append((s[:len(s)-1], int(s[-1])))
    return list_


# BUTTONS
FORM_BTN = KeyboardButton("Заполнить анкету")
EDIT_NAME_BTN = KeyboardButton("Имя")
EDIT_CITY_BTN = KeyboardButton("Город")
EDIT_AGE_BTN = KeyboardButton("Возраст")
EDIT_DESC_BTN = KeyboardButton("Описание")
EDIT_MBTI_BTN = KeyboardButton("MBTI")
MBTI_AGAIN_BTN = KeyboardButton("Пройти тест")
EDIT_TAGS_BTN = KeyboardButton("Теги")
SEARCH_BTN = KeyboardButton("Поиск🔎")
PROFILE_BTN = KeyboardButton("Профиль📝")
MATCH_BTN = KeyboardButton("Match👥")
HELP_BNT = KeyboardButton("Помощь💬")
ONE_BTN = KeyboardButton("1️⃣")
TWO_BTN = KeyboardButton("2️⃣")
BACK_BTN = KeyboardButton("Назад🔙")
LIKE_BTN = KeyboardButton("❤")
SKIP_BTN = KeyboardButton("❌")
END_TAGS_BTN = KeyboardButton("Выбрал")

# KEYBOARDS
FORM_KB = ReplyKeyboardMarkup(resize_keyboard=True)
FORM_KB.add(FORM_BTN)
MENU_KB = ReplyKeyboardMarkup(resize_keyboard=True)
MENU_KB.add(SEARCH_BTN, MATCH_BTN, HELP_BNT, PROFILE_BTN)
CHECK_USERS = ReplyKeyboardMarkup(resize_keyboard=True)
EDIT_PROFILE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
EDIT_PROFILE_KB.add()

HELP_KB = ReplyKeyboardMarkup(resize_keyboard=True)
HELP_KB.add(BACK_BTN)

PROFILE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
PROFILE_KB.add(EDIT_NAME_BTN, EDIT_CITY_BTN, EDIT_AGE_BTN, EDIT_DESC_BTN, EDIT_MBTI_BTN)

EDIT_MBTI_KB = ReplyKeyboardMarkup(resize_keyboard=True)
EDIT_MBTI_KB.add(MBTI_AGAIN_BTN, BACK_BTN)

RATE_PROFILE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
RATE_PROFILE_KB.add(LIKE_BTN, SKIP_BTN)
MBTI_KB = ReplyKeyboardMarkup(resize_keyboard=True)
MBTI_KB.add(ONE_BTN, TWO_BTN)

TAGS_KB = ReplyKeyboardMarkup(resize_keyboard=True)
TAGS_KB.add(END_TAGS_BTN)

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
        await message.reply("Введите имя: ", reply_markup=types.ReplyKeyboardRemove())
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
    elif db.get_state(user_id) == "edit_mbti" and message.text == "Назад🔙":
        db.replace_state(user_id, "edit")
        await message.reply(f"Выберите, что хотите изменить:  ", reply_markup=PROFILE_KB)
    elif db.get_state(user_id) == "description" or db.get_state(user_id) == "edit_mbti":
        if message.text != "Пройти тест":
            db.replace_description(user_id, message.text)
        db.replace_state(user_id, "mbti_ans1")
        db.replace_mbti(user_id, "")
        await message.reply(MBTI1 + "1️⃣Экстраверт  🆚  Интроверт2️⃣\n", reply_markup=MBTI_KB)
    elif db.get_state(user_id) == "mbti_ans1":
        ans = message.text
        db.replace_state(user_id, "mbti_ans2")
        if ans == "1️⃣":
            db.replace_mbti(user_id, "E")
        elif ans == "2️⃣":
            db.replace_mbti(user_id, "I")
        await message.reply(MBTI2 + "1️⃣Интуит  🆚  Сенсорик2️⃣\n\n", reply_markup=MBTI_KB)
    elif db.get_state(user_id) == "mbti_ans2":
        ans = message.text
        db.replace_state(user_id, "mbti_ans3")
        if ans == "1️⃣":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "N")
        elif ans == "2️⃣":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "S")
        await message.reply(MBTI3 + "1️⃣Чувства  🆚  Логика2️⃣\n\n", reply_markup=MBTI_KB)
    elif db.get_state(user_id) == "mbti_ans3":
        ans = message.text
        db.replace_state(user_id, "mbti_ans4")
        if ans == "1️⃣":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "F")
        elif ans == "2️⃣":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "T")
        await message.reply(MBTI4 + "1️⃣Импровизация  🆚  Планирование2️⃣\n\n", reply_markup=MBTI_KB)
    elif db.get_state(user_id) == "mbti_ans4":
        ans = message.text
        db.replace_state(user_id, "mbti_ans5")
        if ans == "1️⃣":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "P")
        elif ans == "2️⃣":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "J")
        await message.reply(MBTI5 + "1️⃣Turbulent  🆚  Assertive2️⃣\n\n", reply_markup=MBTI_KB)
    elif db.get_state(user_id) == "mbti_ans5":
        ans = message.text
        db.replace_state(user_id, "tags")
        if ans == "1️⃣":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "T")
        elif ans == "2️⃣":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "A")
        db.add_tags_str(user_id, TAGS_STR)
        l = str_tags_to_list(db.get_tags(user_id))
        print(l)
        await message.reply("Выберите всевозможные теги из списка", reply_markup=get_tags(l))
        await message.reply("Как выберете, нажмите кнопку", reply_markup=TAGS_KB)
    elif db.get_state(user_id) == "tags" and message.text == "Выбрал":
        db.replace_state(user_id, "wait")
        db.replace_active(user_id, "True")
        await message.reply(get_profile(user_id), reply_markup=MENU_KB)


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

    # HELP
    elif db.get_state(user_id) == "wait" and message.text == "Помощь💬":
        db.replace_state(user_id, "help")
        await message.reply(f"Отвечу на все вопросы\n@gregoryexmachina", reply_markup=HELP_KB)
    elif db.get_state(user_id) == "help" and message.text == "Назад🔙":
        db.replace_state(user_id, "wait")
        await message.reply(f"Вернулись в главное меню", reply_markup=MENU_KB)

    # CHECK PROFILES
    elif db.get_state(user_id) == "wait" and message.text == "Поиск🔎":
        await message.reply(f"Сегодня вам доступны анкеты", reply_markup=profile_kb(user_id))


@dp.callback_query_handler()
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data
    if code == "user1":
        await bot.send_message(callback_query.from_user.id, text=str(code), reply_markup=RATE_PROFILE_KB)


if __name__ == '__main__':
    executor.start_polling(dp)
