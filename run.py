import telebot
import sqlite3
from telebot import types
from storage.config import TOKEN  # импорт токена
import random

bot = telebot.TeleBot(TOKEN)

# Функция для создания таблицы и добавления недостающих столбцов
def create_table():
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    # Создание таблицы, если она не существует
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        photo TEXT,
        cours TEXT,
        gender TEXT,
        description TEXT,
        owner_id INTEGER,
        liked_by TEXT,
        free_time TEXT,
        preference TEXT,
        dream_place TEXT,
        desired_skill TEXT,
        memorable_experience TEXT,
        historical_question TEXT,
        memorable_gift TEXT,
        change_rule TEXT,
        superpower TEXT,
        qa1_question TEXT,
        qa1_answer TEXT,
        qa2_question TEXT,
        qa2_answer TEXT,
        qa3_question TEXT,
        qa3_answer TEXT
    )''')

    # Добавление недостающих столбцов, если они отсутствуют
    cur.execute('PRAGMA table_info(users)')
    columns = cur.fetchall()
    column_names = [column[1] for column in columns]

    if 'age' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN age TEXT')
    if 'photo' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN photo TEXT')
    if 'cours' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN cours TEXT')
    if 'gender' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN gender TEXT')
    if 'description' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN description TEXT')
    if 'owner_id' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN owner_id INTEGER')
    if 'liked_by' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN liked_by TEXT')
    if 'free_time' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN free_time TEXT')
    if 'preference' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN preference TEXT')
    if 'dream_place' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN dream_place TEXT')
    if 'desired_skill' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN desired_skill TEXT')
    if 'memorable_experience' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN memorable_experience TEXT')
    if 'historical_question' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN historical_question TEXT')
    if 'memorable_gift' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN memorable_gift TEXT')
    if 'change_rule' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN change_rule TEXT')
    if 'superpower' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN superpower TEXT')
    if 'qa1_question' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN qa1_question TEXT')
    if 'qa1_answer' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN qa1_answer TEXT')
    if 'qa2_question' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN qa2_question TEXT')
    if 'qa2_answer' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN qa2_answer TEXT')
    if 'qa3_question' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN qa3_question TEXT')
    if 'qa3_answer' not in column_names:
        cur.execute('ALTER TABLE users ADD COLUMN qa3_answer TEXT')

    conn.commit()
    cur.close()
    conn.close()

def safe_delete_message(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error deleting message {message_id} in chat {chat_id}: {e}")

# Создание таблицы при запуске бота
create_table()

#   /start
@bot.message_handler(commands=['start'])
def start_chat(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_about = types.KeyboardButton('О боте')
    btn_yes = types.KeyboardButton('Начать')
    btn_no = types.KeyboardButton('Я ещё не готов')
    markup.row(btn_about)
    markup.row(btn_yes, btn_no)
    bot.send_message(message.chat.id,
                     f"<b>Привет, {message.from_user.first_name}!</b>\n"
                     f"это бот для тренировки твоих софт скиллов и просто для знакомств с другими студентами😃 Заполняй анкету и начинай общаться!",
                     parse_mode='html', reply_markup=markup)
    safe_delete_message(message.chat.id, message.message_id)

@bot.message_handler(func=lambda message: message.text in ['О боте', 'Начать', 'Я ещё не готов'])
def start_menu(message):
    if message.text == "Я ещё не готов":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Готов'))
        bot.send_message(message.chat.id, 'Когда будешь готов, нажми кнопку ниже:', reply_markup=markup)
        safe_delete_message(message.chat.id, message.message_id)
        safe_delete_message(message.chat.id, message.message_id - 1)

    elif message.text == "Начать":
        safe_delete_message(message.chat.id, message.message_id - 1)
        check_and_create_profile(message)

    elif message.text == "О боте":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Назад'))
        bot.send_message(message.chat.id, 'Информация о боте и об авторах', reply_markup=markup)
        safe_delete_message(message.chat.id, message.message_id)
        safe_delete_message(message.chat.id, message.message_id - 1)

@bot.message_handler(func=lambda message: message.text == 'Готов')
def ready(message):
    safe_delete_message(message.chat.id, message.message_id - 1)
    check_and_create_profile(message)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def about_us(message):
    safe_delete_message(message.chat.id, message.message_id - 1)
    start_chat(message)

# Check if the user already has a profile
def check_and_create_profile(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE owner_id = ?', (message.from_user.id,))
    user_profile = cur.fetchone()
    cur.close()
    conn.close()

    print(f"User Profile: {user_profile}")  # Debugging information

    if user_profile:
        show_user_profile(message, user_profile)
    else:
        create_profil(message)

# Show the user's existing profile
def show_user_profile(message, user_profile):
    print(f"User Profile: {user_profile}")  # Debugging information
    if len(user_profile) < 24:
        bot.send_message(message.chat.id, "Ошибка: недостаточно данных в профиле.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    start = types.KeyboardButton('Начать смотреть анкеты')
    edit = types.KeyboardButton('Редактировать анкету')
    markup.row(start, edit)
    bot.send_photo(message.chat.id, user_profile[3], caption=f'{user_profile[1]}, {user_profile[2]} лет\n{user_profile[4]}\nПол: {user_profile[5]}\nОписание: {user_profile[6]}\nВопрос-ответ 1: {user_profile[18]}\nОтвет: {user_profile[19]}\nВопрос-ответ 2: {user_profile[20]}\nОтвет: {user_profile[21]}\nВопрос-ответ 3: {user_profile[22]}\nОтвет: {user_profile[23]}', reply_markup=markup)

# заполнение анкеты
def create_profil(message, user_profile=None):
    safe_delete_message(message.chat.id, message.message_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if user_profile:
        markup.add(types.KeyboardButton(user_profile[1]))
    else:
        markup.add(types.KeyboardButton(message.from_user.first_name))
    bot.send_message(message.chat.id, 'Для начала давай заполним тебе анкету')
    bot.send_message(message.chat.id, 'Как тебя зовут?', reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: user_name(msg, user_profile))

# получение имени
def user_name(message, user_profile):
    name = message.text.strip()
    safe_delete_message(message.chat.id, message.message_id)
    safe_delete_message(message.chat.id, message.message_id - 1)
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Сколько тебе лет?', reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: user_age(msg, name, user_profile))

# получение возраста
def user_age(message, name, user_profile):
    if message.text.strip().isdigit():
        age = message.text.strip()
        safe_delete_message(message.chat.id, message.message_id - 1)
        safe_delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Отправь фото для анкеты')
        bot.register_next_step_handler(message, lambda msg: user_icon(msg, name, age, user_profile))
    else:
        bot.send_message(message.chat.id, 'Введи корректный возраст, только цифры')
        bot.register_next_step_handler(message, lambda msg: user_age(msg, name, user_profile))

# получение фото
def user_icon(message, name, age, user_profile):
    if message.content_type == 'photo':
        photo = message.photo[-1].file_id
        safe_delete_message(message.chat.id, message.message_id - 1)
        safe_delete_message(message.chat.id, message.message_id)
        choose_cours(message, name, age, photo, user_profile)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте фотографию')
        safe_delete_message(message.chat.id, message.message_id)
        bot.register_next_step_handler(message, lambda msg: user_icon(msg, name, age, user_profile))

def choose_cours(message, name, age, photo, user_profile):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    first = types.KeyboardButton('1 курс/10 класс')
    second = types.KeyboardButton('2 курс')
    third = types.KeyboardButton('3 курс')
    markup.add(first)
    markup.row(second, third)
    bot.send_message(message.chat.id, 'Выбери свой курс', reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: user_cours(msg, name, age, photo, user_profile))

# определение курса
def user_cours(message, name, age, photo, user_profile):
    cours = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    male = types.KeyboardButton('Мужской')
    female = types.KeyboardButton('Женский')
    markup.row(male, female)
    safe_delete_message(message.chat.id, message.message_id - 1)
    safe_delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Выбери свой пол', reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: user_gender(msg, name, age, photo, cours, user_profile))

def user_gender(message, name, age, photo, cours, user_profile):
    gender = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton('Пропустить'))
    safe_delete_message(message.chat.id, message.message_id - 1)
    bot.send_message(message.chat.id, 'Добавь описание к анкете:', reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: user_discription(msg, name, age, photo, cours, gender, user_profile))

def user_discription(message, name, age, photo, cours, gender, user_profile):
    if message.text == 'Пропустить':
        description = ''
    else:
        description = message.text

    questions = [
        'Если бы вы могли выбрать любое место на Земле для жизни на год, где бы это было и почему?',
        'Какой навык или умение вы всегда хотели освоить, но еще не успели, и что вас останавливает?',
        'Какой самый необычный или запоминающийся опыт вы пережили, и что он вам дал?',
        'Если бы у вас была возможность задать один вопрос любому человеку в истории, кто бы это был и какой вопрос вы бы задали?',
        'Какой самый необычный или запоминающийся подарок вы когда-либо получали, и что он для вас значил?',
        'Если бы вы могли изменить одно правило или закон в мире, что бы это было и почему?',
        'Если бы вы могли обладать любой суперсилой, что бы это было и как бы вы ее использовали?'
    ]
    selected_questions = random.sample(questions, 3)
    bot.send_message(message.chat.id, f'{selected_questions[0]}')
    bot.register_next_step_handler(message, lambda msg: user_qa1(msg, name, age, photo, cours, gender, description, selected_questions[0], selected_questions[1], selected_questions[2], user_profile))

def user_qa1(message, name, age, photo, cours, gender, description, qa1, qa2, qa3, user_profile):
    qa1_answer = message.text
    bot.send_message(message.chat.id, f'{qa2}')
    bot.register_next_step_handler(message, lambda msg: user_qa2(msg, name, age, photo, cours, gender, description, qa1, qa1_answer, qa2, qa3, user_profile))

def user_qa2(message, name, age, photo, cours, gender, description, qa1, qa1_answer, qa2, qa3, user_profile):
    qa2_answer = message.text
    bot.send_message(message.chat.id, f'{qa3}')
    bot.register_next_step_handler(message, lambda msg: user_qa3(msg, name, age, photo, cours, gender, description, qa1, qa1_answer, qa2, qa2_answer, qa3, user_profile))

def user_qa3(message, name, age, photo, cours, gender, description, qa1, qa1_answer, qa2, qa2_answer, qa3, user_profile):
    qa3_answer = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    start = types.KeyboardButton('Начать смотреть анкеты')
    edit = types.KeyboardButton('Редактировать анкету')
    markup.row(start, edit)
    safe_delete_message(message.chat.id, message.message_id - 1)
    bot.send_photo(message.chat.id, photo, caption=f'{name}, {age} лет\n{cours}\nПол: {gender}\nОписание: {description}\nВопрос-ответ 1: {qa1}\nОтвет: {qa1_answer}\nВопрос-ответ 2: {qa2}\nОтвет: {qa2_answer}\nВопрос-ответ 3: {qa3}\nОтвет: {qa3_answer}', reply_markup=markup)

    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    if user_profile:
        cur.execute("UPDATE users SET name = ?, age = ?, photo = ?, cours = ?, gender = ?, description = ?, qa1_question = ?, qa1_answer = ?, qa2_question = ?, qa2_answer = ?, qa3_question = ?, qa3_answer = ? WHERE owner_id = ?",
                     (name, age, photo, cours, gender, description, qa1, qa1_answer, qa2, qa2_answer, qa3, qa3_answer, message.from_user.id))
    else:
        cur.execute("INSERT INTO users (name, age, photo, cours, gender, description, owner_id, liked_by, free_time, preference, historical_question, memorable_gift, change_rule, qa1_question, qa1_answer, qa2_question, qa2_answer, qa3_question, qa3_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     (name, age, photo, cours, gender, description, message.from_user.id, '', '', '', '', '', '', qa1, qa1_answer, qa2, qa2_answer, qa3, qa3_answer))
    conn.commit()
    cur.close()
    conn.close()

# Edit existing profile
def edit_profile(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE owner_id = ?', (message.from_user.id,))
    user_profile = cur.fetchone()
    cur.close()
    conn.close()

    print(f"User Profile: {user_profile}")  # Debugging information

    if user_profile:
        create_profil(message, user_profile)
    else:
        bot.send_message(message.chat.id, 'Ваша анкета не найдена.')

#   /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Это окно ты можешь вызвать повторно с помощью команды\n/help"
                     f"\nЗдесь ты можешь отправить нам баги/ошибки, и мы их обязательно исправим🙃"
                     f"\n@Ssserpentine - сюда отправлять отчет о багах")

#   /clear_db
@bot.message_handler(commands=['clear_db'])
def clear_db(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute("DELETE FROM users")
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'База данных очищена.')

#   /view_profiles
@bot.message_handler(commands=['view_profiles'])
def view_profiles(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    if users:
        current_index = 0
        show_profile(message, users, current_index)
    else:
        bot.send_message(message.chat.id, 'Нет анкет для просмотра.')

    cur.close()
    conn.close()

def show_profile(message, users, current_index):
    user = users[current_index]
    if user[7] == message.from_user.id:
        current_index += 1
        if current_index < len(users):
            show_profile(message, users, current_index)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            back = types.KeyboardButton('Назад')
            markup.add(back)
            bot.send_message(message.chat.id, 'Больше анкет нет.', reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    like = types.KeyboardButton(text='Лайк')
    skip = types.KeyboardButton(text='Пропустить')
    stop = types.KeyboardButton(text='Прекратить просмотр')
    markup.row(like, skip)
    markup.add(stop)
    bot.send_photo(message.chat.id, user[3], caption=f'{user[1]}, {user[2]} лет\n{user[4]}\nПол: {user[5]}\nОписание: {user[6]}\nВопрос-ответ 1: {user[18]}\nОтвет: {user[19]}\nВопрос-ответ 2: {user[20]}\nОтвет: {user[21]}\nВопрос-ответ 3: {user[22]}\nОтвет: {user[23]}', reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: handle_profile_actions(msg, users, current_index))

def handle_profile_actions(message, users, current_index):
    if message.text == 'Лайк':
        user = users[current_index]
        owner_id = user[7]
        liker_id = message.from_user.id

        # Проверяем, лайкнул ли владелец анкеты в ответ
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute('SELECT liked_by FROM users WHERE owner_id = ?', (owner_id,))
        liked_by = cur.fetchone()[0]

        if liked_by and str(liker_id) in liked_by.split(','):
            # Если владелец анкеты лайкнул в ответ, отправляем им обоим никнеймы
            cur.execute('SELECT name FROM users WHERE owner_id = ?', (owner_id,))
            owner_name = cur.fetchone()[0]
            cur.execute('SELECT name FROM users WHERE owner_id = ?', (liker_id,))
            liker_name = cur.fetchone()[0]

            bot.send_message(owner_id, f'Вы и {liker_name} лайкнули друг друга! Никнейм {liker_name}: @{message.from_user.username}')
            bot.send_message(liker_id, f'Вы и {owner_name} лайкнули друг друга! Никнейм {owner_name}: @{user[1]}')
        else:
            # Если владелец анкеты еще не лайкнул в ответ, отправляем ему анкету лайкера
            cur.execute('SELECT * FROM users WHERE owner_id = ?', (liker_id,))
            liker_profile = cur.fetchone()
            bot.send_photo(owner_id, liker_profile[3], caption=f'{liker_profile[1]}, {liker_profile[2]} лет\n{liker_profile[4]}\nПол: {liker_profile[5]}\nОписание: {liker_profile[6]}\nВопрос-ответ 1: {liker_profile[18]}\nОтвет: {liker_profile[19]}\nВопрос-ответ 2: {liker_profile[20]}\nОтвет: {liker_profile[21]}\nВопрос-ответ 3: {liker_profile[22]}\nОтвет: {liker_profile[23]}')

            # Обновляем поле liked_by для владельца анкеты
            if liked_by:
                liked_by += f',{liker_id}'
            else:
                liked_by = f'{liker_id}'
            cur.execute('UPDATE users SET liked_by = ? WHERE owner_id = ?', (liked_by, owner_id))
            conn.commit()

            # Notify the liker
            notify_liker(message, owner_id, user)

        cur.close()
        conn.close()

        current_index += 1
        if current_index < len(users):
            show_profile(message, users, current_index)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            back = types.KeyboardButton('Назад')
            markup.add(back)
            bot.send_message(message.chat.id, 'Больше анкет нет.', reply_markup=markup)
    elif message.text == 'Пропустить':
        current_index += 1
        if current_index < len(users):
            show_profile(message, users, current_index)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            back = types.KeyboardButton('Назад')
            markup.add(back)
            bot.send_message(message.chat.id, 'Больше анкет нет.', reply_markup=markup)
    elif message.text == 'Прекратить просмотр':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        edit = types.KeyboardButton('Редактировать анкету')
        continue_viewing = types.KeyboardButton('Продолжить просмотр')
        delete_profile = types.KeyboardButton('Отключить анкету')
        markup.row(edit, continue_viewing)
        markup.add(delete_profile)
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
        bot.register_next_step_handler(message, handle_menu_actions)

def handle_menu_actions(message):
    if message.text == 'Редактировать анкету':
        edit_profile(message)
    elif message.text == 'Продолжить просмотр':
        view_profiles(message)
    elif message.text == 'Отключить анкету':
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE owner_id = ?", (message.from_user.id,))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, 'Ваша анкета удалена.')

def notify_liker(message, owner_id, user):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    view = types.KeyboardButton('Посмотреть')
    skip = types.KeyboardButton('Пропустить')
    markup.row(view, skip)
    bot.send_message(message.chat.id, f'Привет, кому-то понравилась твоя анкета! Нажми "Посмотреть", чтобы узнать кто это.', reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: handle_view_liker(msg, owner_id, user))

def handle_view_liker(message, owner_id, user):
    if message.text == 'Посмотреть':
        bot.send_photo(message.chat.id, user[3], caption=f'{user[1]}, {user[2]} лет\n{user[4]}\nПол: {user[5]}\nОписание: {user[6]}\nВопрос-ответ 1: {user[18]}\nОтвет: {user[19]}\nВопрос-ответ 2: {user[20]}\nОтвет: {user[21]}\nВопрос-ответ 3: {user[22]}\nОтвет: {user[23]}')
    elif message.text == 'Пропустить':
        bot.send_message(message.chat.id, 'Вы пропустили просмотр анкеты.')

@bot.message_handler(func=lambda message: message.text == 'Начать смотреть анкеты')
def start_viewing_profiles(message):
    view_profiles(message)

@bot.message_handler(func=lambda message: message.text == 'Редактировать анкету')
def start_editing_profile(message):
    edit_profile(message)

bot.polling(non_stop=True)
