import telebot
import os

# Токен тепер береться з безпечного місця на Koyeb
API_TOKEN = os.getenv('API_TOKEN') 
bot = telebot.TeleBot(API_TOKEN)

# Функція для створення головного меню з кнопками
def make_main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_product = telebot.types.KeyboardButton('📋 Продукція')
    btn_price = telebot.types.KeyboardButton('💰 Ціни')
    btn_delivery = telebot.types.KeyboardButton('🚚 Доставка')
    btn_contacts = telebot.types.KeyboardButton('📞 Контакти')
    btn_order = telebot.types.KeyboardButton('🛒 Зробити замовлення')
    markup.add(btn_product, btn_price, btn_delivery, btn_contacts, btn_order)
    return markup

# Обробник команд /start та /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = """
Вітаю! Я віртуальний помічник компанії ТЕК.
Чим можу допомогти? Оберіть опцію з меню👇
    """
    bot.send_message(message.chat.id, welcome_text, reply_markup=make_main_menu())

# Обробник для кнопки "📋 Продукція"
@bot.message_handler(func=lambda message: message.text == '📋 Продукція')
def send_product_info(message):
    product_text = """
🟫 <b>Наші торф'яні пелети</b>

<b>Основні переваги:</b>
• Висока теплотворність: до 5 кВт/кг (як у вугіллі)
• Низька зольність: менше 10%
• Екологічне паливо
• Висока щільність та найбільша тривалість горіння серед пеллет

<b>Фасування:</b>
• Біг-беги (по 1000 кг)
• Доставка навалом

<b>Застосування:</b>
• Котли опалення
• Каміни та печі
• Бойлерні
• Твердопаливні генератори
    """
    bot.send_message(message.chat.id, product_text, parse_mode='HTML')

# Обробник для кнопки "💰 Ціни"
@bot.message_handler(func=lambda message: message.text == '💰 Ціни')
def send_price_info(message):
    price_text = """
💵 <b>Актуальні ціни на 20.08.2025</b>

<b>Роздріб:</b>
• Біг Бег (1000 кг) — <b>7000 грн</b>



<b>Вартість доставки:</b>
• розраховується індивідуально

💡 <i>При замовленні від 23 тонн — додаткова знижка!</i>
    """
    bot.send_message(message.chat.id, price_text, parse_mode='HTML')

# Обробник для кнопки "🚚 Доставка"
@bot.message_handler(func=lambda message: message.text == '🚚 Доставка')
def send_delivery_info(message):
    delivery_text = """
🚛 <b>Умови доставки та оплати</b>

<b>Регіони доставки:</b>
• Доставляємо по всій Україні (окрім поки що окупованих територій)


<b>Способи оплати:</b>
• Готівковий розрахунок
• Безготівковий розрахунок (для ФОП та юридичних осіб)


<b>Терміни виконання замовлення:</b>
• 1-2 робочих дні після підтвердження замовлення
    """
    bot.send_message(message.chat.id, delivery_text, parse_mode='HTML')

# Обробник для кнопки "📞 Контакти"
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
Сб: 11:00-19:00
Нд: 11:00-19:00

🌐 <b>Наш сайт:</b> www.peat-energy.com.ua
    """
    bot.send_message(message.chat.id, contacts_text, parse_mode='HTML')

# Заглушка для кнопки "🛒 Зробити замовлення" (поки що)
@bot.message_handler(func=lambda message: message.text == '🛒 Зробити замовлення')
def start_order(message):
    bot.send_message(message.chat.id, "Функція оформлення замовлення тимчасово недоступна. Будь ласка, зателефонуйте нам для оформлення замовлення. 📞")

# Обробник всіх інших повідомлень
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Оберіть опцію з меню 👇", reply_markup=make_main_menu())

# Запуск бота
print("Бот запущений і чекає повідомлення...")
bot.infinity_polling()