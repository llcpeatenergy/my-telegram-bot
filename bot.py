import telebot
import os
import re
import logging
from telebot import types

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)
logger = logging.getLogger(__name__)

# Токен береться зі змінних середовища
API_TOKEN = os.getenv('API_TOKEN') 
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '452999752')

if not API_TOKEN:
    logger.error("Не встановлено API_TOKEN! Бот не може бути запущений.")
    exit(1)

bot = telebot.TeleBot(API_TOKEN)
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

# Функція для створення кнопки "Почати"
def make_start_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = types.KeyboardButton('🚀 Почати роботу')
    markup.add(btn_start)
    return markup

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
    try:
        bot.send_message(ADMIN_CHAT_ID, order_text)
        logger.info(f"Замовлення від {chat_id} відправлено адміністратору")
    except Exception as e:
        logger.error(f"Помилка відправки замовлення адміністратору: {e}")

# ========== ОБРОБНИКИ ПОВІДОМЛЕНЬ ==========

# Вітальне повідомлення при першому контакті
@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda message: message.text == '🚀 Почати роботу')
def send_welcome(message):
    welcome_text = """
🤖 <b>Вітаю! Я віртуальний помічник компанії ТЕК.</b>

💡 <i>Обери потрібну опцію з меню нижче 👇</i>
    """
    bot.send_message(message.chat.id, welcome_text, 
                    parse_mode='HTML', 
                    reply_markup=make_main_menu())
    logger.info(f"Користувач {message.chat.id} запустив бота")
    user_data[message.chat.id] = {'started': True}

# Обробник для будь-якого першого повідомлення
@bot.message_handler(func=lambda message: message.chat.id not in user_data, 
                    content_types=['text', 'photo', 'document', 'sticker'])
def handle_first_message(message):
    welcome_text = """
👋 <b>Ласкаво просимо!</b>

Я віртуальний помічник компанії ТЕК. 
Для початку роботи натисніть кнопку <b>"Почати роботу"</b> 👇
    """
    bot.send_message(message.chat.id, welcome_text, 
                    parse_mode='HTML', 
                    reply_markup=make_start_button())
    logger.info(f"Користувач {message.chat.id} відправив перше повідомлення: {message.text}")

# Обробник для кнопок головного меню
@bot.message_handler(func=lambda message: message.chat.id in user_data and message.text in [
    '📋 Продукція', '💰 Ціни', '🚚 Доставка', 
    '📞 Контакти', '🗺️ Де ми знаходимось', '🛒 Зробити замовлення'
])
def handle_main_menu(message):
    if message.text == '📋 Продукція':
        product_text = """
🟫 <b>Наші торф'яні пелети</b>

<b>Основні переваги:</b>
• Висока теплотворність: до 5 кВт/кг (як у вугілля)
• Калорійність від 4700 ккал
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
        logger.info(f"Користувач {message.chat.id} переглянув інформацію про продукцію")
    
    elif message.text == '💰 Ціни':
        price_text = """
💵 <b>Актуальні ціни</b>

<b>Роздріб:</b>
• Біг Бег (1000 кг) — <b>7000 грн з ПДВ</b>

<b>Вартість доставки:</b>
• розраховується індивідуально

💡 <i>При замовленні від 23 тонн — додаткова знижка!</i>
        """
        bot.send_message(message.chat.id, price_text, parse_mode='HTML')
        logger.info(f"Користувач {message.chat.id} переглянув ціни")
    
    elif message.text == '🚚 Доставка':
        delivery_text = """
🚛 <b>Умови доставки та оплати</b>

<b>Регіони доставки:</b>
• Доставляємо по всій Україні (окрім тимчасово окупованих територій)

<b>Способи оплати:</b>
• Безготівковий розрахунок (для ФОП та юридичних осіб)
• Готівковий розрахунок через кассу

<b>Терміни виконання замовлення:</b>
• 1-2 робочих дні після підтвердження замовлення
        """
        bot.send_message(message.chat.id, delivery_text, parse_mode='HTML')
        logger.info(f"Користувач {message.chat.id} переглянув умови доставки")
    
    elif message.text == '📞 Контакти':
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
        logger.info(f"Користувач {message.chat.id} переглянув контакти")
    
    elif message.text == '🗺️ Де ми знаходимось':
        latitude = 50.70145383475299
        longitude = 26.354577705876483
        bot.send_location(message.chat.id, latitude, longitude)
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
        logger.info(f"Користувач {message.chat.id} переглянув локацію")
    
    elif message.text == '🛒 Зробити замовлення':
        chat_id = message.chat.id
        user_data[chat_id] = {'step': 'name'}
        bot.send_message(chat_id, "✏️ Будь ласка, введіть ваше ім'я:")
        logger.info(f"Користувач {message.chat.id} почав оформлення замовлення")

# Обробник для отримання імені
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id].get('step') == 'name')
def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['name'] = message.text
    user_data[chat_id]['step'] = 'phone'
    
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    reg_button = types.KeyboardButton(text="📞 Поділитися контактом", request_contact=True)
    keyboard.add(reg_button)
    
    bot.send_message(chat_id, "📞 Тепер поділіться вашим номером телефону:", reply_markup=keyboard)
    logger.info(f"Користувач {message.chat.id} ввів ім'я: {message.text}")

# Обробник для отримання контакту
@bot.message_handler(content_types=['contact'])
def get_contact(message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id].get('step') == 'phone':
        user_data[chat_id]['phone'] = message.contact.phone_number
        user_data[chat_id]['step'] = 'quantity'
        bot.send_message(chat_id, "✅ Дякую! Тепер введіть кількість продукції (у тонах):", reply_markup=make_main_menu())
        logger.info(f"Користувач {message.chat.id} надав контакт: {message.contact.phone_number}")

# Обробник для отримання номера телефону як тексту
@bot.message_handler(func=lambda message: message.chat.id in user_data 
                     and user_data[message.chat.id].get('step') == 'phone' 
                     and message.text
                     and not message.text.startswith('/'))
def get_phone_text(message):
    chat_id = message.chat.id
    phone_pattern = r'^(\+?\d{1,3})?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    if re.match(phone_pattern, message.text):
        user_data[chat_id]['phone'] = message.text
        user_data[chat_id]['step'] = 'quantity'
        bot.send_message(chat_id, "✅ Дякую! Тепер введіть кількість продукції (у тонах):", reply_markup=make_main_menu())
        logger.info(f"Користувач {message.chat.id} ввів телефон: {message.text}")
    else:
        bot.send_message(chat_id, "❌ Будь ласка, введіть коректний номер телефону або скористайтеся кнопкою 'Поділитися контактом':")

# Обробник для отримання кількості
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id].get('step') == 'quantity')
def get_quantity(message):
    chat_id = message.chat.id
    try:
        quantity = float(message.text.replace(',', '.'))  
        user_data[chat_id]['quantity'] = quantity
        send_order_to_admin(chat_id)
        bot.send_message(chat_id, "✅ Ваше замовлення прийнято! Наш менеджер зв'яжеться з вами найближчим часом.", reply_markup=make_main_menu())
        logger.info(f"Користувач {message.chat.id} замовив {quantity} тонн")
        del user_data[chat_id]
    except ValueError:
        bot.send_message(chat_id, "❌ Будь ласка, введіть число. Наприклад: 1.5 або 2:")

# Обробник для скасування
@bot.message_handler(func=lambda message: message.text.lower() in ['скасувати', '/cancel', 'відміна', 'відмінити'])
def cancel_order(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        del user_data[chat_id]
        bot.send_message(chat_id, "❌ Замовлення скасовано.", reply_markup=make_main_menu())
        logger.info(f"Користувач {message.chat.id} скасував замовлення")

# Обробник для невідомих команд після старту
@bot.message_handler(func=lambda message: message.chat.id in user_data and message.text not in [
    '📋 Продукція', '💰 Ціни', '🚚 Доставка', '📞 Контакти', 
    '🗺️ Де ми знаходимось', '🛒 Зробити замовлення', '🚀 Почати роботу'
])
def handle_unknown_after_start(message):
    help_text = """
🤔 <b>Не розпізнав команду</b>

Будь ласка, оберіть потрібну опцію з меню нижче 👇
Або напишіть /start для перезапуску бота
    """
    bot.send_message(message.chat.id, help_text, parse_mode='HTML', reply_markup=make_main_menu())

if __name__ == '__main__':
    logger.info("Бот запускається...")
    print("Бот запущений і чекає повідомлення...")
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        logger.error(f"Помилка в роботі бота: {e}")
        print(f"Сталася помилка: {e}")