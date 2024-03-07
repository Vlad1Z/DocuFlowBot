from telebot import types


class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.user_data = {}
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.main_menu(message)

        @self.bot.message_handler(func=lambda message: True)
        def handle_text(message):
            if message.text == 'Заказать справку':
                self.order_certificate(message)
            elif message.text == 'Узнать перечень документов на замену паспорта':
                self.passport_info(message)
            elif message.text == 'Получить информацию о работе паспортных столов г. Гомель':
                self.passport_department_info(message)
            # Добавьте дополнительные условия для других кнопок меню здесь
            else:
                self.bot.send_message(message.chat.id, "Не понимаю ваш выбор, попробуйте еще раз.")
                self.main_menu(message)  # Возвращаем пользователя в главное меню

    def main_menu(self, message):
        # Логика главного меню
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        buttons = ['Заказать справку', 'Узнать перечень документов на замену паспорта', 'Получить информацию о работе паспортных столов г. Гомель']
        markup.add(*(types.KeyboardButton(button) for button in buttons))
        self.bot.send_message(message.chat.id, f"Добрый день, {message.from_user.first_name}! Чем я могу вам помочь?", reply_markup=markup)

    def order_certificate(self, message):
        # Логика для заказа справки
        # Отправляем пользователю сообщение с дополнительными инструкциями или запросами
        self.bot.send_message(message.chat.id, "Вы выбрали заказ справки. Пожалуйста, выберите тип справки:", reply_markup=self.get_sertificate_markup())

        sertificate_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        sertificate_buttons = [
            'Справка о месте жительства и составе семьи',
            'Справка о месте жительства',
            'Справка о занимаемом в данном населенном пункте жилом помещении и составе семьи',
            'Справка о последнем месте жительства наследодателя и о составе его семьи на день смерти',
            'Вернуться назад'
        ]
        for button in sertificate_buttons:
            sertificate_markup.add(types.KeyboardButton(button))

        # Отправляем пользователю сообщение с клавиатурой
        self.bot.send_message(message.chat.id, "Вы выбрали заказ справки. Пожалуйста, выберите тип справки:",
                              reply_markup=sertificate_markup)

        # Устанавливаем следующий шаг обработчика
        self.bot.register_next_step_handler(message, self.process_spravka_choice)

    def process_spravka_choice(self, message):
        # Обрабатываем выбор пользователя
        user_id = message.from_user.id
        text = message.text
        if text == 'Справка о месте жительства и составе семьи':
            # Запрашиваем дополнительные данные или предоставляем информацию
            pass
        elif text == 'Вернуться назад':
            # Возвращаем пользователя в главное меню
            self.main_menu(message)
        # Добавьте обработку для других типов справок
        else:
            self.bot.send_message(message.chat.id, "Не понимаю ваш выбор, попробуйте еще раз.")
            self.order_certificate(message)  # Возвращаем пользователя к выбору типа справки

    def passport_info(self, message):
        # Логика для информации о документах на замену паспорта
        pass

    def passport_department_info(self, message):
        # Логика для информации о работе паспортных столов
        pass

    def get_sertificate_markup(self):
        # Метод для создания клавиатуры выбора справки
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        sertificate_buttons = ['Справка о месте жительства и составе семьи', 'Справка о месте жительства', 'Вернуться назад']
        markup.add(*(types.KeyboardButton(button) for button in sertificate_buttons))
        return markup


def setup_handlers(bot):
    handler = CommandHandler(bot)
