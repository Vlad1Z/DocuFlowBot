from telebot import TeleBot
from config import TELEBOT_TOKEN
from handlers.StartHandler import StartHandler
from handlers.PassportInfoHandler import PassportInfoHandler
from handlers.PassportOfficeInfoHandler import PassportOfficeInfoHandler
from handlers.CertificateHandler import CertificateHandler
from handlers.RegistrationInfoHandler import RegistrationInfoHandler


bot = TeleBot(TELEBOT_TOKEN)

# Экземпляры обработчиков
start_handler = StartHandler(bot)
passport_info_handler = PassportInfoHandler(bot)
passport_office_info_handler = PassportOfficeInfoHandler(bot)
certificate_handler = CertificateHandler(bot)
registration_info_handler = RegistrationInfoHandler(bot)


# Функция для регистрации обработчиков
def register_handlers():
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        start_handler.handle(message)

    @bot.message_handler(func=lambda message: True)
    def handle_text(message):
        if message.text == 'Узнать перечень документов на замену паспорта':
            passport_info_handler.handle(message)
        elif message.text == 'Получить информацию о работе паспортных столов г. Гомель':
            passport_office_info_handler.handle(message)
        elif message.text == 'Заказать справку':
            certificate_handler.handle(message)
        elif message.text == 'Узнать перечень документов для регистрации (прописки)':
            registration_info_handler.handle(message)
        else:
            # Если текст сообщения не соответствует ни одному из условий выше,
            # можно отправить пользователю сообщение о том, что команда не распознана,
            bot.send_message(message.chat.id, "Команда не распознана. Пожалуйста, выберите один из доступных вариантов.")
            start_handler.handle(message)  # Возвращаем пользователя в главное меню


register_handlers()

bot.polling(none_stop=True)
