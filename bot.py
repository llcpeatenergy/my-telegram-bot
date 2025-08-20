import telebot 

API_TOKEN = '8247514083:AAFftrPNCpM9l0yUYFzjuTlDfHZ59WhBuSE'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я тестовий бот. Як справи?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

print("Бот запущений і чекає повідомлення...")
bot.infinity_polling()