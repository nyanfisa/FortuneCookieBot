import telebot
import json
import random
import os
from dotenv import load_dotenv
from telebot import types 

load_dotenv()
token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(token)

def get_fortune(category=None):
    with open('data/fortunes.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if category:
        category_fortunes = [f for f in data['fortunes'] if f['type'] == category]
        if category_fortunes: 
            fortune = random.choice(category_fortunes)
        else:
            fortune = random.choice(data['fortunes'])
    else:
        fortune = random.choice(data['fortunes'])
    
    return fortune['message']


def keyboard_bottons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  
    btn1 = types.KeyboardButton("Мудрость🧙‍♀️")
    btn2 = types.KeyboardButton("Предсказание🥠")
    markup.row(btn1, btn2)
    return markup

@bot.message_handler(commands=['start'])   
def start(message):
    bot.send_message(
        message.chat.id, 
        "Привет! Я бот с предсказаниями! Выбери категорию:", 
        reply_markup=keyboard_bottons()
    )

@bot.message_handler()   
def all_message_handler(message):
    if message.text == "Мудрость🧙‍♀️":
        fortune = get_fortune("wisdom")  
        bot.send_message(
            message.chat.id, 
            f"🧙‍♀️ *Мудрость дня:*\n_{fortune}_", 
            parse_mode='Markdown',
            reply_markup=keyboard_bottons()
        )
    elif message.text == "Предсказание🥠":
        fortune = get_fortune("prediction") 
        bot.send_message(
            message.chat.id, 
            f"*Предсказание для тебя ✨🥠✨*\n_{fortune}_", 
            parse_mode='Markdown',
            reply_markup=keyboard_bottons()
        )
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используй кнопки!")

bot.infinity_polling()