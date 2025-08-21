import telebot
import os
import re
from telebot import types
from flask import Flask
import threading

# Токен береться зі змінних середовища
API_TOKEN = os.getenv('API_TOKEN') 
# ID адміністратора також береться зі змінних середовища
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '452999752')  # Значення за замовчуванням на випадок відсутності змінної

bot = telebot.TeleBot(API_TOKEN)

# Словник для зберігання даних замовлень
user_data = {}

# Функція для створення головного меню
def make_main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_product = types.KeyboardButton('📋 Продукція')
    btn_price = types.KeyboardButton('💰 Ціни')
    btn_delivery = types.KeyboardButton('🚚 Доставка')
    btn_contacts = types.KeyboardButton('📞 Контакти')
    btn_order = types.KeyboardButton('🛒 Зробити замовлення')
    btn_location = types.KeyboardButton('🗺️ Де ми знаходимось')
    markup.add(btn_product, btn_price, btn_delivery, btn_contacts, btn_order, btn_location)
    return markup

# Команди /start та /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = """
Вітаю! Я віртуальний помічник компанії ТЕК.
Чим можу допомогти? Оберіть опцію з меню👇
    """
    bot.send_message(message.chat.id, welcome_text, reply_markup=make_main_menu())

# Обробник для "📋 Продукція"
@bot.message_handler(func=lambda message: message.text == '📋 Продукція')
def send_product_info(message):
    product_text = """
🟫 <b>Наші торф'яні пелети</b>

<b>Основні переваги:</b>
• Висока теплотворність: до 5.2 кВт/кг (як у вугілля)
• Калорійність від 4600 ккал
• Низька зольність: менше 10%
• Екологічне паливо
• Висока щільність та найбільша тривалість горіння серед пеллет

<b>Фасування:</b>
• Біг-беги (по 1000 кг)
• Навалом

<b>Застосування:</b>
• Котли опалення
• Каміни та печі
• Котельні
• Твердопаливні генератори
    """
    bot.send_message(message.chat.id, product_text, parse_mode='HTML')

# Обробник для "💰 Ціни"
@bot.message_handler(func=lambda message: message.text == '💰 Ціни')
def send_price_info(message):
    price_text = """
💵 <b>Актуальні ціни на серпень 2025</b>

<b>Роздріб:</b>
• Біг Бег (1000 кг) — <b>7000 грн з ПДВ</b>

<b>Вартість доставки:</b>
• розраховується індивідуально

💡 <i>При замовленні від 23 тонн — додаткова знижка!</i>
    """
    bot.send_message(message.chat.id, price_text, parse_mode='HTML')

# Обробник для "🚚 Доставка"
@bot.message_handler(func=lambda message: message.text == '🚚 Доставка')
def send_delivery_info(message):
    delivery_text = """
🚛 <b>Умови доставки та оплати</b>

<b>Регіони доставки:</b>
• Доставляємо по всій Україні (окрім тимчасово окупованих територій)

<b>Способи оплати:</b>
• Готівковий розрахунок
• Безготівковий розрахунок (для ФОП та юридичних осіб)

<b>Терміни виконання замовлення:</b>
• 1-2 робочих дні після підтвердження замовлення
    """
    bot.send_message(message.chat.id, delivery_text, parse_mode='HTML')

# Обробник для "📞 Контакти"
@bot.message_handler(func=lambda message: message.text == '📞 Контакти')
def send_contacts(message):
    contacts_text = """
📞 <b>Наші контакти</b>

<b>Телефон менеджера:</b>
+38 (050) 444 61 62

<b>Електронна пошта:</b>
LLC.peatenergy@gmail.com

<b>Адреса складу:</b>
Рівненський район, Забороль вул. Колгоспна 41Є

<b>Графік роботи:</b>
Пн-Пт: 9:00-19:00
Сб-Нд: 11:00-19:00

🌐 <b>Наш сайт:</b> www.peat-energy.com.ua
    """
    bot.send_message(message.chat.id, contacts_text, parse_mode='HTML')

# Обробник для "🗺️ Де ми знаходимось"
@bot.message_handler(func=lambda message: message.text == '🗺️ Де ми знаходимось')
def send_location(message):
    # Координати вашого складу
    latitude = 50.70145383475299
    longitude = 26.354577705876483
    
    # Відправляємо локацію на карті
    bot.send_location(message.chat.id, latitude, longitude)
    
    # Додаємо посилання на Google Maps
    maps_text = """
🗺️ <b>Наше місцезнаходження:</b>

<b>Адреса:</b>
Рівненський район, Забороль вул. Колгоспна 41Є

<b>Посилання на Google Maps:</b>
https://maps.app.goo.gl/?q=50.70145383475299,26.354577705876483

<b>Графік роботи:</b>
Пн-Пт: 9:00-19:00
Сб-Нд: 11:00-19:00
"""
    bot.send_message(message.chat.id, maps_text, parse_mode='HTML')

# Обробник для "🛒 Зробити замовлення"
@bot.message_handler(func=lambda message: message.text == '🛒 Зробити замовлення')
def start_order(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 'name'}
    bot.send_message(chat_id, "✏️ Будь ласка, введіть ваше ім'я:")

# Обробник для отримання імені
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id]['step'] == 'name')
def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['name'] = message.text
    user_data[chat_id]['step'] = 'phone'
    
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    reg_button = types.KeyboardButton(text="📞 Поділитися контактом", request_contact=True)
    keyboard.add(reg_button)
    
    bot.send_message(chat_id, "📞 Тепер поділіться вашим номером телефону:", reply_markup=keyboard)

# Обробник для отримання контакту
@bot.message_handler(content_types=['contact'])
def get_contact(message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id]['step'] == 'phone':
        user_data[chat_id]['phone'] = message.contact.phone_number
        user_data[chat_id]['step'] = 'quantity'
        bot.send_message(chat_id, "✅ Дякую! Тепер введіть кількість продукції (у тонах):", reply_markup=make_main_menu())

# Обробник для отримання номера телефону як тексту (альтернатива контакту)
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id]['step'] == 'phone')
def get_phone_text(message):
    chat_id = message.chat.id
    # Проста перевірка, чи введений текст схожий на номер телефону
    phone_pattern = r'^(\+?\d{1,3})?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    if re.match(phone_pattern, message.text):
        user_data[chat_id]['phone'] = message.text
        user_data[chat_id]['step'] = 'quantity'
        bot.send_message(chat_id, "✅ Дякую! Тепер введіть кількість продукції (у тонах):", reply_markup=make_main_menu())
    else:
        bot.send_message(chat_id, "❌ Будь ласка, введіть коректний номер телефону або скористайтеся кнопкою 'Поділитися контактом':")

# Обробник для отримання кількості
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id]['step'] == 'quantity')
def get_quantity(message):
    chat_id = message.chat.id
    try:
        # Спроба перетворити текст у число (дробові також)
        quantity = float(message.text.replace(',', '.'))  
        user_data[chat_id]['quantity'] = quantity
        send_order_to_admin(chat_id)
        bot.send_message(chat_id, "✅ Ваше замовлення прийнято! Наш менеджер зв'яжеться з вами найближчим часом.", reply_markup=make_main_menu())
        del user_data[chat_id]
    except ValueError:
        # Якщо не вдалося перетворити, просимо ввести ще раз
        bot.send_message(chat_id, "❌ Будь ласка, введіть число. Наприклад: 1.5 або 2:")

# Функція для відправки замовлення адміну
def send_order_to_admin(chat_id):
    order = user_data[chat_id]
    order_text = f"""
🛒 НОВЕ ЗАМОВЛЕННЯ!

👤 Ім'я: {order['name']}
📞 Телефон: {order['phone']}
📦 Кількість: {order['quantity']} т
    
💬 Чат ID: {chat_id}
    """
    bot.send_message(ADMIN_CHAT_ID, order_text)

# Обробник для скасування
@bot.message_handler(func=lambda message: message.text.lower() in ['скасувати', '/cancel', 'відміна', 'відмінити'])
def cancel_order(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        del user_data[chat_id]
        bot.send_message(chat_id, "❌ Замовлення скасовано.", reply_markup=make_main_menu())

# Обробник всіх інших повідомлень
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Оберіть опцію з меню 👇", reply_markup=make_main_menu())

# Створюємо Flask сервер для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is running! Use /start in Telegram."

def run_flask():
    app.run(host='0.0.0.0', port=8000, debug=False)

# Запускаємо Flask у фоновому потоці
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

print("Flask server started on port 8000")

# Додаємо періодичні ping-и для Render
import requests
import schedule
import time

def ping_server():
    try:
        response = requests.get('https://my-telegram-bot-8118.onrender.com', timeout=5)
        print(f"Ping successful: {response.status_code}")
    except Exception as e:
        print(f"Ping failed: {e}")

def run_ping_schedule():
    schedule.every(10).minutes.do(ping_server)
    while True:
        schedule.run_pending()
        time.sleep(1)

ping_thread = threading.Thread(target=run_ping_schedule)
ping_thread.daemon = True
ping_thread.start()

print("Ping scheduler started")

# Запуск бота
print("Бот запущений і чекає повідомлення...")
bot.infinity_polling()