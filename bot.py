from cities import Cities
from database import Database

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove
from PIL import Image
import os
from datetime import datetime

TOKEN = ""
cities_obj = Cities("other/russia.json")
CITIES = cities_obj.get_cities()
db = Database("user.db")

TAGS_STR = "Меломан0\nЛюбитель кино0\nГик0\nГеймер0\nЛюбитель аниме0\nКнижный червь0\nГурман0\nЛюбитель искусства0\n" \
           "Творческий человек0\nЛюбитель технологий0\nЛюбитель науки0\nПредприниматель0\nЛюбитель спорта0\n" \
           "Путешественник0\nМодник0\nЛюбитель кошек0\nЛюбитель собак0\nСтудент0\nТрудоголик0\nМемолог0\nБудущий полиглот0\n" \
           "Духовный искатель0\nДиванный политолог0\nКурю0\nПою0\nИду к цели0"

MBTI1 = "Гриша:\n" \
        "Общительный и активный\n" \
        "Ориентирован на внешний мир и события\n" \
        "Быстро адаптируется к новым ситуациям и людям\n" \
        "Извлекает энергию из взаимодействия с окружающими\n\n" \
        "Влад:\n" \
        "Предпочитает маленькие группы и интимные обстановки\n" \
        "Тратит время на размышления и самоанализ\n" \
        "Может быть тихой и сдержанной в общении\n" \
        "Нуждается в личном пространстве для восстановления энергии\n\n"

MBTI2 = "Гриша:\n" \
        "Ориентирован на общие идеи и возможности\n" \
        "При принятии решений полагается на интуицию и воображение\n" \
        "Размышляет о будущем и том, что могло бы быть\n" \
        "Предпочитает теории и абстрактные понятия\n\n" \
        "Влад:\n" \
        "Фокусируется на реальном мире и конкретных деталях\n" \
        "Опирается на опыт и здравый смысл при принятии решений\n" \
        "Предпочитает практичность и конкретные действия\n" \
        "Имеет наслаждаться моментом\n\n"

MBTI3 = "Гриша:\n" \
        "Принимает решения, исходя из личных ценностей и чувств\n" \
        "Чуткий к эмоциям других людей\n" \
        "Старается создать гармоничную атмосферу вокруг себя\n" \
        "Дипломатичен и умеет находить компромиссы\n\n" \
        "Влад:\n" \
        "Делает выбор на основе логики и объективного анализа" \
        "\nЦенит честность и прямоту" \
        "\nТрудности и противоречия видит как вызовы, а не препятствия" \
        "\nИщет наиболее эффективные и практичные решения\n\n"

MBTI4 = "Гриша:" \
        "\nГибкий и адаптивный к переменам" \
        "\nОценивает разные варианты перед принятием решения" \
        "\nПредпочитает открытость и возможность изменить планы" \
        "\nКомфортно чувствует себя в менее структурированных ситуациях\n\n" \
        "Влад:\n" \
        "Планирует и ставит цели на будущее" \
        "\nПредпочитает четкие рамки и порядок" \
        "\nОрганизована и ответственна" \
        "\nСтарается доводить начатое дело до конца\n\n"

MBTI5 = "Гриша:" \
        "\nСклонен к переживаниям и самокритике" \
        "\nБеспокоится о том, что другие могут о нем думать" \
        "\nВосприимчив к стрессу и изменениям" \
        "\nСтремится к совершенству и работает над улучшением своих недостатков\n\n" \
        "Влад:\n" \
        "Обладает высоким уровнем самоуверенности и спокойствия" \
        "\nМеньше заботится о мнении окружающих" \
        "\nЛегко преодолевает стресс и быстро восстанавливается после неудач" \
        "\nПринимает свои сильные и слабые стороны, считая их нормальными\n\n"


# FUNCTION
def get_current_time():
    return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())


def correct_name(name):
    if len(name) <= 10:
        return True
    return False


def get_profile(user_id):
    profile_list = db.get_my_profile(user_id)
    tags_list = []
    for s in profile_list[8].split("\n"):
        if s[-1] == '1':
            tags_list.append(s[:len(s) - 1])
    return f"{profile_list[2]}\n{profile_list[4]}\n{profile_list[5]}\n{profile_list[6]}\n" \
           f"{profile_list[7]}\n{', '.join(tags_list)}"


def get_profiles(user_id):
    profiles_list = db.get_all_profiles(user_id)
    new_list = []
    for user in profiles_list:
        match_pr = db.get_match_pr(db.get_mbti(user_id)[:4], db.get_mbti(user[0])[:4])
        if match_pr is None:
            match_pr = db.get_match_pr(db.get_mbti(user[0])[:4], db.get_mbti(user_id)[:4])[0]
        else:
            match_pr = match_pr[0]
        new_user = list(user)
        new_user.append(match_pr)
        new_list.append(tuple(new_user))
    return new_list


def sort_profiles(profiles_list, user_id):
    user_list = []
    my_profile = db.get_my_profile(user_id)
    my_mbti = db.get_mbti(user_id)
    my_tags = str_tags_to_list(db.get_tags(user_id))
    my_tags = [tag[0] for tag in my_tags if tag[1] == 1]
    for user in profiles_list:
        user_id = user[0]
        user_tags = user[8].split("\n")
        user_tags = [tag[:len(tag) - 1] for tag in user_tags if tag[-1] == "1"]
        count_common_tags = len(set(my_tags) & set(user_tags))
        user_mbti = user[7]
        pr = db.get_match_pr(my_mbti[:4], user_mbti[:4])
        if pr is None:
            pr = db.get_match_pr(user_mbti[:4], my_mbti[:4])[0]
        else:
            pr = pr[0]
        common_pr = pr / 2.5 + count_common_tags
        if my_mbti[-1] == user_mbti[-1]:
            common_pr += 1
        else:
            common_pr -= 1
        user_list.append((common_pr, user_id, pr))
    user_list = sorted(user_list, reverse=True)
    return user_list


def sort_by_age_city(user_id, el):
    s_age = db.get_s_age(user_id)
    end_age = db.get_end_age(user_id)
    city = db.get_sort_city(user_id)
    new_list = []
    if el[4] == city and s_age <= int(el[5]) <= end_age:
        return True
    return False


def sort_by_age(user_id, el):
    s_age = db.get_s_age(user_id)
    end_age = db.get_end_age(user_id)
    new_list = []
    if s_age <= int(el[5]) <= end_age:
        return True
    return False


def sort_by_city(user_id, el):
    city = db.get_sort_city(user_id)
    new_list = []
    if el[4] == city:
        return True
    return False


def profile_kb(user_id):
    global search_list
    CHECK_PROFILES_KB = InlineKeyboardMarkup(row_width=1)
    profiles_list = get_profiles(user_id)

    list_ = []
    profiles_list = sort_profiles(profiles_list, user_id)
    i = 0
    for cpr, id, pr in profiles_list:
        profile = list(db.get_my_profile(id))
        s_age = db.get_s_age(user_id)
        city = db.get_sort_city(user_id)
        if city is None and s_age is None:
            profile.append(pr)
            list_.append(profile)

        elif city is None:
            if sort_by_age(user_id, profile):
                profile.append(pr)
                list_.append(profile)

        elif s_age is None:
            if sort_by_city(user_id, profile):
                profile.append(pr)
                list_.append(profile)
        else:
            if sort_by_age_city(user_id, profile):
                profile.append(pr)
                list_.append(profile)

        i += 1

    if len(list_) == 0:
        return None, list_[:10]
    else:
        for profile in list_[:10]:
            CHECK_PROFILES_KB.add(
                InlineKeyboardButton(profile[2] + " " + profile[4] + " " + str(profile[5]) + f" {profile[-1]}%",
                                     callback_data=f'user{profile[0]}'))

        return CHECK_PROFILES_KB, list_[:10]


def get_tags(tags_list):
    TAGS_KB = InlineKeyboardMarkup(row_width=4)

    list_btn = []
    for tag_tuple in tags_list:
        if tag_tuple[1] == 0:
            list_btn.append(InlineKeyboardButton(tag_tuple[0], callback_data=tag_tuple[0]))
        else:
            list_btn.append(InlineKeyboardButton("✅" + tag_tuple[0], callback_data=tag_tuple[0]))

    for i in range(0, len(list_btn), 2):
        TAGS_KB.row(list_btn[i], list_btn[i + 1])

    return TAGS_KB


def list_tags_to_str(tags_list):
    tags = ""
    for t in tags_list:
        if t[0] != "Иду к цели":
            tags += t[0] + str(t[1]) + "\n"
        else:
            tags += t[0] + str(t[1])
    return tags


def str_tags_to_list(tags_str):
    l = tags_str.split("\n")
    list_ = []
    for s in l:
        list_.append([s[:len(s) - 1], int(s[-1])])
    return list_


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def write_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)


def get_center_x(img):
    return int(img.size[0] / 2)


def get_height(img):
    return int(img.size[1])


# BUTTONS
FORM_BTN = KeyboardButton("Заполнить анкету")
EDIT_NAME_BTN = KeyboardButton("Имя")
EDIT_CITY_BTN = KeyboardButton("Город")
EDIT_AGE_BTN = KeyboardButton("Возраст")
EDIT_DESC_BTN = KeyboardButton("Описание")
EDIT_MBTI_BTN = KeyboardButton("MBTI")
MBTI_AGAIN_BTN = KeyboardButton("Пройти тест")
EDIT_TAGS_BTN = KeyboardButton("Теги")
SEARCH_BTN = KeyboardButton("Анкеты📒")
PROFILE_BTN = KeyboardButton("Профиль📝")
MATCH_BTN = KeyboardButton("Match👥")
HELP_BNT = KeyboardButton("Помощь💬")
ONE_BTN = KeyboardButton("1️⃣")
TWO_BTN = KeyboardButton("2️⃣")
BACK_BTN = KeyboardButton("Назад🔙")
LIKE_BTN = KeyboardButton("❤")
SKIP_BTN = KeyboardButton("❌")
MENU_BTN = KeyboardButton("Главная")
END_TAGS_BTN = KeyboardButton("Выбрал")
MAN_BTN = KeyboardButton("Мужской")
WOMAN_BTN = KeyboardButton("Женский")
AGE_BTN = KeyboardButton("Возраст")
CITY_BTN = KeyboardButton("Город")
GET_PROFILES_BTN = KeyboardButton("Получить")

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
RATE_PROFILE_KB.add(LIKE_BTN, MENU_BTN, SKIP_BTN)
MBTI_KB = ReplyKeyboardMarkup(resize_keyboard=True)
MBTI_KB.add(ONE_BTN, TWO_BTN)

TAGS_KB = ReplyKeyboardMarkup(resize_keyboard=True)
TAGS_KB.add(END_TAGS_BTN)

SEX_KB = ReplyKeyboardMarkup(resize_keyboard=True)
SEX_KB.add(MAN_BTN, WOMAN_BTN)

SORT_KB = ReplyKeyboardMarkup(resize_keyboard=True)
SORT_KB.add(AGE_BTN, CITY_BTN, GET_PROFILES_BTN, BACK_BTN)

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
        await message.reply("Введите имя: ", reply_markup=ReplyKeyboardRemove())
    elif db.get_state(user_id) == "name":
        if correct_name(message.text):
            db.replace_state(user_id, "sex")
            db.replace_name(user_id, message.text)
            await message.reply("Ваше имя принято!\nВыберите пол", reply_markup=SEX_KB)
        else:
            await message.reply("Имя должно быть меньше 10 символов и начинаться с заглавной буквы")
    elif db.get_state(user_id) == "sex" and message.text == "Мужской":
        db.replace_state(user_id, "city")
        db.replace_sex(user_id, message.text.lower()[0])
        await message.reply("Запомнили!\nВ каком городе вы живёте?", reply_markup=ReplyKeyboardRemove())
    elif db.get_state(user_id) == "sex" and message.text == "Женский":
        db.replace_state(user_id, "city")
        db.replace_sex(user_id, message.text.lower()[0])
        await message.reply("Запомнили!\nВ каком городе вы живёте?", reply_markup=ReplyKeyboardRemove())

    elif db.get_state(user_id) == "city":
        if message.text in CITIES:
            db.replace_state(user_id, "age")
            db.replace_city(user_id, message.text);
            await message.reply("Ваш город принят!\nВведите теперь свой возраст")
        else:
            await message.reply(f"Город не обнаружен.\nДоступные города:\n{', '.join(CITIES)}")
    elif db.get_state(user_id) == "age":
        if message.text.isdigit() and 18 <= int(message.text) <= 80:
            db.replace_state(user_id, "mbti_ans1")
            db.replace_mbti(user_id, "")
            db.replace_age(user_id, message.text)
            await message.reply(MBTI1 + "1️⃣Экстраверт  🆚  Интроверт2️⃣\n", reply_markup=MBTI_KB)
    elif db.get_state(user_id) == "edit_mbti" and message.text == "Назад🔙":
        db.replace_state(user_id, "edit")
        await message.reply(f"Выберите, что хотите изменить:  ", reply_markup=PROFILE_KB)
    elif db.get_state(user_id) == "description":
        db.replace_description(user_id, message.text)
        db.replace_state(user_id, "wait")
        db.replace_active(user_id, "True")
        await message.reply("Анкета создана", reply_markup=MENU_KB)
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
        await message.reply("Выберите всевозможные теги из списка", reply_markup=get_tags(l))
        await message.reply("Как выберете, нажмите кнопку", reply_markup=TAGS_KB)

    elif db.get_state(user_id) == "tags" and message.text == "Выбрал":
        db.replace_state(user_id, "back")
        await bot.delete_message(chat_id=message.from_user.id, message_id=db.get_last_msg_id(user_id))
        await message.reply("Приступим к созданию вашего образа\nВыберете более подходящий для вас цвет и "
                            "введите его название!", reply_markup=ReplyKeyboardRemove())
        with open("img/backs.png", "rb") as backs:
            await bot.send_photo(chat_id=message.chat.id, photo=backs)

    elif db.get_state(user_id) == "back":
        ans = message.text
        if ans in ["aqua", "blue", "coral", "coralorange", "grey", "lavender", "lightblue", "mauve", "mint", "pale",
                   "peach", "periwinkle", "pinkdust", "rose", "rosegold", "sage", "teal", "warm_grey", "white",
                   "yellow"]:
            base_img = Image.open("img/back/" + ans + ".png")
            add_img = Image.open("img/person/тело.png")
            base_img.paste(add_img, (500 - get_center_x(add_img), 300), mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "eyes")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await message.reply("Выберите глаза и введите название")
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/eyes.png", "rb"))
        else:
            await message.reply("Введено неверное название фона. Введите ещё раз")

    elif db.get_state(user_id) == "eyes":
        ans = message.text
        if ans in ["eye" + str(i) for i in range(1, 6)]:
            base_img = Image.open(f"img/current_{user_id}.png")
            add_img = Image.open(f"img/person/{ans}.png")
            base_img.paste(add_img, (500 - get_center_x(add_img) - 5, 430), mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "brows")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await message.reply("Выберите брови и введите название. Если хотите без бровей - напишите\n'дальше'")
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/brows.png", "rb"))
        else:
            await message.reply("Введено неверное название глаз. Введите ещё раз")

    elif db.get_state(user_id) == "brows":
        ans = message.text
        if ans in ["brows" + str(i) for i in range(1, 6)]:
            base_img = Image.open(f"img/current_{user_id}.png")
            add_img = Image.open(f"img/person/{ans}.png")
            base_img.paste(add_img, (500 - get_center_x(add_img) - 5, 360), mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "mous")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await message.reply("Выберите рот и введите название")
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/mous.png", "rb"))
        elif ans == "дальше":
            db.replace_state(user_id, "mous")
            await message.reply("Выберите рот и введите название")
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/mous.png", "rb"))
        else:
            await message.reply("Введено неверное название бровей. Введите ещё раз")

    elif db.get_state(user_id) == "mous":
        ans = message.text
        if ans in ["mou" + str(i) for i in range(1, 6)]:
            base_img = Image.open(f"img/current_{user_id}.png")
            add_img = Image.open(f"img/person/{ans}.png")
            base_img.paste(add_img, (500 - get_center_x(add_img) - 5, 500 - get_height(add_img) + 140),
                           mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "hairs")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await message.reply("Выберите волосы и введите название. Если хотите без волос - напишите\n'дальше'")
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/hairs.png", "rb"))
        else:
            await message.reply("Введено неверное название рта. Введите ещё раз")

    elif db.get_state(user_id) == "hairs":
        ans = message.text
        if ans in ["hsv" + str(i) for i in range(1, 8)] or ans in ["nat" + str(i) for i in range(1, 8)] or \
                ["rad" + str(i) for i in range(1, 8)] or ["red" + str(i) for i in range(1, 8)] \
                or ["tem" + str(i) for i in range(1, 8)] or ["wh" + str(i) for i in range(1, 8)] \
                or ["yar7" + str(i) for i in range(1, 8)]:
            base_img = Image.open(f"img/current_{user_id}.png")
            add_img = Image.open(f"img/person/{ans}.png")
            base_img.paste(add_img, (500 - get_center_x(add_img) - 2, 300), mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "horns")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/horns.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        elif ans == "дальше":
            db.replace_state(user_id, "horns")
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/horns.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        else:
            await message.reply("Введено неверное название волос. Введите ещё раз")

    elif db.get_state(user_id) == "horns":
        ans = message.text
        if ans.lower() == "да":
            base_img = Image.open(f"img/current_{user_id}.png")
            add_img = Image.open(f"img/person/horns.png")
            base_img.paste(add_img, (500 - get_center_x(add_img) - 2, 268), mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "glasses")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/glasses.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        elif ans.lower() == "нет":
            db.replace_state(user_id, "glasses")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/glasses.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        else:
            await message.reply("Нет такого ответа. Введите ещё раз")

    elif db.get_state(user_id) == "glasses":
        ans = message.text
        if ans.lower() == "да":
            base_img = Image.open(f"img/current_{user_id}.png")
            add_img = Image.open(f"img/person/glasses.png")
            base_img.paste(add_img, (500 - get_center_x(add_img) - 2, 430), mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "beard")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/beard.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        elif ans.lower() == "нет":
            db.replace_state(user_id, "beard")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/beard.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        else:
            await message.reply("Нет такого ответа. Введите ещё раз")

    elif db.get_state(user_id) == "beard":
        ans = message.text
        if ans.lower() == "да":
            base_img = Image.open(f"img/current_{user_id}.png")
            add_img = Image.open(f"img/person/beard.png")
            base_img.paste(add_img, (500 - get_center_x(add_img) - 2, 600), mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "nose")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/nose.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        elif ans.lower() == "нет":
            db.replace_state(user_id, "nose")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/nose.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        else:
            await message.reply("Нет такого ответа. Введите ещё раз")

    elif db.get_state(user_id) == "nose":
        ans = message.text
        if ans.lower() == "да":
            base_img = Image.open(f"img/current_{user_id}.png")
            add_img = Image.open(f"img/person/nose.png")
            base_img.paste(add_img, (500 - get_center_x(add_img) - 5, 480), mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "cheeks")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/cheeks.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        elif ans.lower() == "нет":
            db.replace_state(user_id, "cheeks")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await bot.send_photo(chat_id=message.chat.id, photo=open("img/person/cheeks.png", "rb"))
            await message.reply("Добавить? Введите\nДа(Нет)")
        else:
            await message.reply("Нет такого ответа. Введите ещё раз")

    elif db.get_state(user_id) == "cheeks":
        ans = message.text
        if ans.lower() == "да":
            base_img = Image.open(f"img/current_{user_id}.png")
            add_img = Image.open(f"img/person/cheeks.png")
            base_img.paste(add_img, (500 - get_center_x(add_img) - 5, 520), mask=add_img.convert('RGBA'))
            base_img.save(f"img/current_{user_id}.png", quality=100)
            db.replace_state(user_id, "wait")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await message.reply("Ваш аватар готов", reply_markup=MENU_KB)
            db.replace_photo(convert_to_binary_data(f"img/current_{user_id}.png"), user_id)
            os.remove(f"img/current_{user_id}.png")
        elif ans.lower() == "нет":
            db.replace_state(user_id, "description")
            await bot.send_photo(chat_id=message.chat.id, photo=open(f"img/current_{user_id}.png", "rb"))
            await message.reply("Ваш аватар готов", reply_markup=MENU_KB)
            db.replace_photo(convert_to_binary_data(f"img/current_{user_id}.png"), user_id)
            os.remove(f"img/current_{user_id}.png")
            await message.reply("Введите пару слов о себе", reply_markup=ReplyKeyboardRemove())
        else:
            await message.reply("Нет такого ответа. Введите ещё раз")


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
        await message.reply(f"Прошлое описание: {profile_list[6]}\nВведите новое описание:")
    elif db.get_state(user_id) == "edit_desc":
        db.replace_state(user_id, "wait")
        db.replace_description(user_id, message.text)
        await message.reply(get_profile(user_id), reply_markup=MENU_KB)
    elif message.text == "MBTI" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_mbti")
        profile_list = db.get_my_profile(user_id)
        await message.reply(f"Ваш MBTI: {profile_list[7]}", reply_markup=EDIT_MBTI_KB)
    elif db.get_state(user_id) == "edit_mbti":
        db.replace_state(user_id, "wait")
        db.replace_description(user_id, message.text)
        await message.reply(get_profile(user_id), reply_markup=MENU_KB)

    # HELP
    elif db.get_state(user_id) == "wait" and message.text == "Помощь💬":
        db.replace_state(user_id, "help")
        await message.reply(f"Отвечу на все вопросы\n@gregoryexmachina", reply_markup=HELP_KB)
    elif db.get_state(user_id) == "help" and message.text == "Назад🔙":
        db.replace_state(user_id, "wait")
        await message.reply(f"Вернулись в главное меню", reply_markup=MENU_KB)

    # CHECK PROFILES
    elif db.get_state(user_id) == "sort" and message.text == "Получить":
        db.replace_state(user_id, "wait")
        p_kb = profile_kb(user_id)[0]
        if p_kb is None:
            await message.reply("Недостаточно анкет", reply_markup=MENU_KB)
        elif get_current_time() - db.get_time_end_get(user_id) > 24 * 3600:
            db.replace_time_end_get(user_id, get_current_time())
            await message.reply(f"⬇️⬇️⬇️⬇️⬇️", reply_markup=MENU_KB)
            msg = await message.reply(f"Сегодня вам доступны анкеты", reply_markup=p_kb)
            db.replace_last_msg_id(user_id, msg.message_id)
        else:
            await message.reply("Анкеты на сегодня израсходованы", reply_markup=MENU_KB)
    elif db.get_state(user_id) == "wait" and message.text == "Анкеты📒":
        await message.reply(f"Вы можете настроить выборку анкет", reply_markup=SORT_KB)
        db.replace_state(user_id, "sort")
    elif db.get_state(user_id) == "sort" and message.text == "Назад🔙":
        db.replace_state(user_id, "wait")
        await message.reply(f"Вернулись в главное меню", reply_markup=MENU_KB)
    elif db.get_state(user_id) == "sort_age":
        ans = message.text
        if ans.count("-"):
            s_age, end_age = ans.split("-")
            if s_age.isdigit() and end_age.isdigit():
                s_age = int(s_age)
                end_age = int(end_age)
                if s_age <= end_age and s_age >= 18 and end_age <= 80:
                    db.replace_start_age(user_id, s_age)
                    db.replace_end_age(user_id, end_age)
                    db.replace_state(user_id, "sort")
                    await message.reply(f"Возраст настроен", reply_markup=SORT_KB)
                else:
                    await message.reply(f"Возраст введён неверно или в неверном формате")
            else:
                await message.reply(f"Возраст введён неверно или в неверном формате")
        else:
            await message.reply(f"Возраст введён неверно или в неверном формате")
    elif db.get_state(user_id) == "sort" and message.text == "Возраст":
        db.replace_state(user_id, "sort_age")
        await message.reply(f"Введите диапазон возраста\nПример:\n18-23", reply_markup=ReplyKeyboardRemove())
    elif db.get_state(user_id) == "sort_city":
        ans = message.text
        if ans in CITIES:
            db.replace_sort_city(user_id, ans)
            db.replace_state(user_id, "sort")
            await message.reply(f"Город настроен", reply_markup=SORT_KB)
        else:
            await message.reply(f"Город введён неверно или его нет в списке")
    elif db.get_state(user_id) == "sort" and message.text == "Город":
        db.replace_state(user_id, "sort_city")
        await message.reply(f"Введите город", reply_markup=ReplyKeyboardRemove())

    elif db.get_state(user_id) == "check_profiles" and message.text == "❌":
        db.del_like(user_id, db.get_last_id_profile(user_id))
        db.replace_state(user_id, "wait")
        await bot.delete_message(chat_id=message.from_user.id, message_id=db.get_last_msg_id(user_id))
        await message.reply(f"Пропустили", reply_markup=MENU_KB)
    elif db.get_state(user_id) == "check_profiles" and message.text == "❤":
        db.add_like(user_id, db.get_last_id_profile(user_id))
        p = db.get_my_profile(user_id)
        db.replace_state(user_id, "wait")
        tags = p[8].split("\n")
        tags = [tag[:len(tag) - 1] for tag in tags if tag[-1] == "1"]
        my_tags = str_tags_to_list(db.get_tags(db.get_last_id_profile(user_id)))
        my_tags = [tag[0] for tag in my_tags if tag[1] == 1]
        common_tags = set(tags) & set(my_tags)
        pr = db.get_match_pr(db.get_mbti(user_id)[:4], db.get_mbti(db.get_last_id_profile(user_id))[:4])
        if pr is None:
            pr = db.get_match_pr(db.get_mbti(db.get_last_id_profile(user_id))[:4], db.get_mbti(user_id)[:4])[0]
        else:
            pr = pr[0]
        # await bot.send_message(str(db.get_last_id_profile(user_id)), text=f"Вами заинтересовались:\n{p[2]}\n@{p[1]}\nВозраст: {p[5]}\n{p[4]}"
        #                             f"\nВаша совместимость: {pr} %\nОбщее кол-во тегов: {len(common_tags)}\n"
        #                             f"{', '.join(common_tags)}\n\nВсе теги:\n{', '.join(tags)}\n\n{p[6]}")

        await bot.delete_message(chat_id=message.from_user.id, message_id=db.get_last_msg_id(user_id))
        await message.reply(f"Лайк поставлен", reply_markup=MENU_KB)
    elif db.get_state(user_id) == "check_profiles" and message.text == "Главная":
        db.replace_state(user_id, "wait")
        await bot.delete_message(chat_id=message.from_user.id, message_id=db.get_last_msg_id(user_id))
        await message.reply(f"Вернулись в главное меню", reply_markup=MENU_KB)
    elif db.get_state(user_id) == "wait" and message.text == "Match👥":
        liked_id_list = db.get_liked_id_by_user(str(user_id))
        for id in liked_id_list:
            p = db.get_my_profile(id)
            tags = p[8].split("\n")
            tags = [tag[:len(tag) - 1] for tag in tags if tag[-1] == "1"]
            my_tags = str_tags_to_list(db.get_tags(user_id))
            my_tags = [tag[0] for tag in my_tags if tag[1] == 1]
            common_tags = set(tags) & set(my_tags)
            pr = db.get_match_pr(db.get_mbti(user_id)[:4], db.get_mbti(id)[:4])
            if pr is None:
                pr = db.get_match_pr(db.get_mbti(id)[:4], db.get_mbti(user_id)[:4])[0]
            else:
                pr = pr[0]

            await bot.send_message(user_id,
                                   text=f"Вами заинтересовались:\n{p[2]}\n@{p[1]}\nВозраст: {p[5]}\n{p[4]}\nВаша совместимость: {pr} %\nОбщее кол-во тегов: {len(common_tags)}\n{', '.join(common_tags)}\n\nВсе теги:\n{', '.join(tags)}\n\n{p[6]}",
                                   reply_markup=MENU_KB)


@dp.callback_query_handler()
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data
    all_id = db.get_all_id(callback_query.from_user.id)
    for find_id in all_id:
        if code == f"user{find_id[0]}":
            for el in profile_kb(callback_query.from_user.id)[1]:
                if el[0] == find_id[0]:
                    p = el
                    break
            db.replace_last_id_profile(callback_query.from_user.id, p[0])
            tags = p[8].split("\n")
            tags = [tag[:len(tag) - 1] for tag in tags if tag[-1] == "1"]
            my_tags = str_tags_to_list(db.get_tags(callback_query.from_user.id))
            my_tags = [tag[0] for tag in my_tags if tag[1] == 1]
            common_tags = set(tags) & set(my_tags)
            db.replace_state(callback_query.from_user.id, "check_profiles")
            msg = await bot.send_message(callback_query.from_user.id,
                                         text=f"{p[2]}\n{p[3]}\nВозраст: {p[5]}\nВаша совместимость: {p[-1]} %\nОбщее кол-во тегов: {len(common_tags)}\n{', '.join(common_tags)}\n\nВсе теги:\n{', '.join(tags)}\n\n{p[6]}",
                                         reply_markup=RATE_PROFILE_KB)
            db.replace_last_msg_id(callback_query.from_user.id, msg.message_id)

    list_ = str_tags_to_list(db.get_tags(callback_query.from_user.id))
    for i in range(len(list_)):
        if code == list_[i][0]:
            if list_[i][1] == 0:
                list_[i][1] = 1
            else:
                list_[i][1] = 0
            await callback_query.answer(
                show_alert=True
            )
            db.replace_last_msg_id(callback_query.from_user.id, callback_query.message.message_id)
            await bot.answer_callback_query(callback_query.id, text=list_[i][0])
            await callback_query.message.edit_reply_markup(reply_markup=get_tags(list_))
    db.add_tags_str(callback_query.from_user.id, list_tags_to_str(list_))


if __name__ == '__main__':
    executor.start_polling(dp)
