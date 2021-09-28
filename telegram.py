import telebot
bot = telebot.TeleBot('1865413913:AAEQ0LWWY0YvPK4CwAUCGXBVPO3TaLEXFAs')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start\nВот другие мои команды:')
    print('/start - старт бота')
    print('/materials - все раздаточные материалы проекта')
    print('/status - режим работы системы')
    print('/charge - заряд аккумулятора')
    print('/consumption - сколько потребляется')
    print('/production - сколько вырабатывается')
    print('/water - воды в ГЭС')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '/materials':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    else:
        print(message.chat.username)

 
bot.polling()