import telebot
from telebot import types
import logging

from telebot.types import KeyboardButton, ReplyKeyboardMarkup

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)

user_data = {}

menu_data = {
    'uz': {
        'menu_text': '2D Game Developer Unity kursining birinchi bepul darsiga roʻyxatdan oʻtganingiz uchun raxmat.',
        'option1': '🎮Darsni qanday ko’raman',
        'option2': '🎁 Sovg’a olish',
        'option3': '💳Kursni sotib olish',
        'option4': '🙋 Savol bermoqchiman',
        'back': 'Orqaga'
    },
    'ru': {
        'menu_text': 'Спасибо за регистрацию на первый бесплатный урок курса Разработчик 2D игр Unity.',
        'option1': '🎮Как посмотреть урок',
        'option2': '🎁 Забрать подарок',
        'option3': '💳Приобрести  весь курс',
        'option4': '🙋 Хочу спросить?',
        'back': 'Назад'
    }
}

menu_data_2 = {
    'uz': {
        'option1': 'Siz ko\'rsatgan elektron pochta manziliga login, parol va shaxsiy kabinetingizga kirish havolasi bilan xat yuborildi.Dars allaqachon mavjud, tomosha qiling😜Agar xat kelmagan bo\'lsa, spam papkasini tekshiring.',
        'option2': 'Va\'da qilinganidek, biz Unity ishlab chiqaruvchisidan "Yo\'l xaritasi"ni taqdim etamiz. Pastdagi havoladan yuklab olishingiz mumkin https://drive.google.com/file/d/19byBVLHKSE3AD-x_fVZre1OtrprdfLIs/view?usp=sharing',
        'option3': '💳PayMe bilan toʻlashda kurs narxi 6 000 000 soʻmni tashkil qiladi 2 000 000 so\'m. Kurs narxiga o\'qituvchi suhbati yordami va 10 soatdan ortiq video kontent kiradi.',
        'option4': 'Savollaringiz bormi?',
        'back': 'Orqaga'
    },
    'ru': {
        'option1': 'На указанную вами почту пришло письмо с логином,паролем и ссылкой для входа в личный кабинет.Урок уже там,приятного просмотра😜Если письмо не пришло,пожалуйста проверьте папку спам.',
        'option2': 'Как и обещали, дарим Road Map (Дорожную карту) разработчика Unity. Скачать можно по ссылке ниже https://drive.google.com/file/d/19byBVLHKSE3AD-x_fVZre1OtrprdfLIs/view?usp=sharing',
        'option3': 'При оплате PayMe стоимость курса 6 000 000 UZS 2 000 000 UZS. В стоимость курса входит поддержка преподавателя в чате и более 10 часов видео контента.',
        'option4': 'У вас возникли вопросы?',
        'back': 'Назад'
    }
}

text_phone_request = {
    'uz': {
        'phone_request': 'Agar sizda biron bir savol bo\'lsa yoki kurs haqida ko\'proq bilmoqchi bo\'lsangiz, pastdagi formada telefon raqamingizni qoldiring.',
        'btn_text': 'Nomer jonatish',
        'reply': 'Rahmat, tez orada siz bilan bog\'lanamiz.'
    },
    'ru': {
        'phone_request': 'Если у вас появились вопросы или вы хотите узнать больше о курсе,оставьте телефон в форме ниже.',
        'btn_text': 'Отправить номер',
        'reply': 'Спасибо,мы скоро с вами свяжемся.'
    }
}


# Function to handle the main menu
def handle_main_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("RU", callback_data="lang_ru"))
    markup.add(types.InlineKeyboardButton("UZ", callback_data="lang_uz"))

    bot.send_message(message.chat.id, "Добро пожаловать в Онлайн школу программирования Codemoon.Я твой личный помощник.Пожалуйста выберите язык для продолжения общения.\n\n➖\n\n Codemoon Online dasturlash maktabiga xush kelibsiz. Men sizning shaxsiy yordamchingizman. Muloqotni davom ettirish uchun tilni tanlang.")
    bot.send_message(message.chat.id,'Выберите язык\nTil tanlang', reply_markup=markup)


# Function to handle 'Buy a House' option
def handle_selection(chat_id, lang):
    markup = types.InlineKeyboardMarkup()
    user_data[chat_id]['lang'] = lang
    # Example price ranges, adjust as needed
    markup.add(types.InlineKeyboardButton(menu_data[lang]['option1'], callback_data="view_class"))
    markup.add(types.InlineKeyboardButton(menu_data[lang]['option2'], callback_data="take_gift"))
    markup.add(types.InlineKeyboardButton(menu_data[lang]['option3'], callback_data="buy"))
    markup.add(types.InlineKeyboardButton(menu_data[lang]['option4'], callback_data="ask"))

    markup.add(types.InlineKeyboardButton(menu_data[lang]['back'], callback_data="back_m1"))

    bot.send_message(chat_id, menu_data[lang]['menu_text'], reply_markup=markup)


# Function to handle 'Rent a House' option

# Function to handle the price selection
def handle_price_selection(chat_id, price_range):
    user_data[chat_id]['price_range'] = price_range
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Указать на карте", callback_data="put_map"),
               types.InlineKeyboardButton("Далее", callback_data="next"))
    bot.send_message(chat_id, "Вы хотите выбрать удобное вам место в городе?", reply_markup=markup)


# Start command
@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    handle_main_menu(message)


# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        chat_id = call.message.chat.id

        if call.data.startswith("lang_"):
            lang = call.data.split('_')[1]
            handle_selection(chat_id, lang)

        elif call.data.startswith("back_"):
            if call.data.split('_')[1] == 'm1':
                handle_main_menu(call.message)
            else:
                handle_selection(chat_id, user_data[chat_id]['lang'])
        elif call.data == "view_class":
            markup = create_keyboard(user_data[call.message.chat.id]['lang'])
            bot.send_message(chat_id=call.message.chat.id,
                             text=menu_data_2[user_data[call.message.chat.id]['lang']]['option1'],
                             reply_markup=markup)
        elif call.data == "take_gift":
            markup = create_keyboard(user_data[call.message.chat.id]['lang'])
            bot.send_message(chat_id=call.message.chat.id,
                             text=menu_data_2[user_data[call.message.chat.id]['lang']]['option2'],
                             reply_markup=markup)
        elif call.data == "buy":
            markup = create_keyboard(user_data[call.message.chat.id]['lang'])
            bot.send_message(chat_id=call.message.chat.id,
                             text=menu_data_2[user_data[call.message.chat.id]['lang']]['option3'],
                             reply_markup=markup)

        elif call.data == "ask":
            markup = create_phone_request(user_data[call.message.chat.id]['lang'])
            bot.send_message(chat_id=call.message.chat.id,
                             text=text_phone_request[user_data[call.message.chat.id]['lang']]['phone_request'],
                             reply_markup=markup)

        elif call.data == "next":
            process_search_for_house(call.message)

    except Exception as e:
        print(e)
        print(e.args)


def create_keyboard(lang):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton(menu_data_2[lang]['back'] + ' ')
    markup.add(btn1)
    return markup


def create_phone_request(lang):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    phone_button = types.KeyboardButton(text_phone_request[lang]['btn_text'], request_contact=True)
    markup.add(phone_button)
    return markup


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        if message.text == menu_data_2['ru']['back'] or message.text == menu_data_2['uz']['back']:
            handle_selection(message.chat.id, user_data[message.chat.id]['lang'])
        if message.contact:
            bot.send_message(message.chat.id, text_phone_request[user_data[message.message.chat.id]['lang']]['reply'])
            handle_main_menu(message)
    except Exception as e:
        print(e)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        bot.send_message(message.chat.id, text_phone_request[user_data[message.chat.id]['lang']]['reply'])
        handle_selection(message.chat.id, user_data[message.chat.id]['lang'])
    except Exception as e:
        print(e)

# Run the bot


def process_search_for_house(message):
    pass


bot.polling(none_stop=True)
