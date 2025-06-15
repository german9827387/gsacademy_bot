
import telebot
from telebot import types

import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(TOKEN)

faq_answers = {
    "цена": "Стоимость занятий — 4500₽ в месяц. Пробное занятие бесплатно.",
    "пробное": "Пробное занятие бесплатно! Мы предоставим экипировку.",
    "мотивация": "У нас уникальная система мотивации: оценки по личным качествам, браслеты и ярмарка призов.",
    "направления": "Мы проводим занятия по БЖЖ, грэпплингу, ММА и боксу.",
    "запись": "Нажмите кнопку 'Записаться' ниже или напишите имя, возраст, направление и удобное время.",
}

user_states = {}

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Записаться", "Цены", "Отзывы", "Позвонить", "Сайт")

    bot.send_message(
        message.chat.id,
        "Привет! Я бот Академии единоборств. Могу ответить на вопросы или записать на занятие. Выберите действие или задайте вопрос.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "Позвонить")
def call_button(message):
    bot.send_message(message.chat.id, "📞 +7 (342) 256-32-55")

@bot.message_handler(func=lambda message: message.text == "Сайт")
def site_button(message):
    bot.send_message(message.chat.id, "🌐 https://bjj59.ru")

@bot.message_handler(func=lambda message: message.text == "Отзывы")
def reviews_button(message):
    bot.send_message(message.chat.id, "⭐ Отзывы: https://2gis.ru/perm/geo/70000001006776807")

@bot.message_handler(func=lambda message: message.text == "Цены")
def price_button(message):
    bot.send_message(message.chat.id, faq_answers["цена"])

@bot.message_handler(func=lambda message: message.text == "Записаться")
def start_application(message):
    user_states[message.chat.id] = {"step": 1}
    bot.send_message(message.chat.id, "Как вас зовут?")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id in user_states:
        state = user_states[chat_id]
        step = state.get("step", 1)

        if step == 1:
            state["name"] = text
            state["step"] = 2
            bot.send_message(chat_id, "Сколько вам лет?")
        elif step == 2:
            state["age"] = text
            state["step"] = 3
            bot.send_message(chat_id, "Какое направление вас интересует?")
        elif step == 3:
            state["direction"] = text
            state["step"] = 4
            bot.send_message(chat_id, "В какое время вам удобно приходить?")
        elif step == 4:
            state["time"] = text
            msg = f"📥 Новая заявка:
👤 Имя: {state['name']}
🎂 Возраст: {state['age']}
🥋 Направление: {state['direction']}
⏰ Удобное время: {state['time']}
От @{message.from_user.username or message.from_user.first_name}"
            bot.send_message(CHAT_ID, msg)
            bot.send_message(chat_id, "Спасибо! Ваша заявка отправлена. Мы скоро свяжемся с вами!")
            user_states.pop(chat_id)
        return

    for key in faq_answers:
        if key in text.lower():
            bot.send_message(chat_id, faq_answers[key])
            return

    bot.send_message(chat_id, "Не понял ваш вопрос. Вы можете воспользоваться кнопками ниже.")

bot.polling()
