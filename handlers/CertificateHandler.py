from telebot import types
from .BaseHandler import BaseHandler
from utils import send_notification  # Убедитесь, что это правильный путь импорта


class CertificateHandler(BaseHandler):
    def handle(self, message):
        """Обрабатывает входящее сообщение и отображает опции справок."""
        self.show_certificate_options(message)

    def show_certificate_options(self, message):
        """Отображает пользователю клавиатуру с опциями различных справок, по одной опции на строку."""
        certificate_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        buttons = [
            'Справка о месте жительства и составе семьи',
            'Справка о месте жительства',
            'Справка о занимаемом жилом помещении и составе семьи',
            'Справка о последнем месте жительства наследодателя и о составе его семьи',
            'Вернуться назад'
        ]
        for button in buttons:
            certificate_markup.row(types.KeyboardButton(button))
        # Отправляем сообщение с созданной клавиатурой пользователю
        self.bot.send_message(message.chat.id, "Выберите тип справки:", reply_markup=certificate_markup)
        # Регистрируем следующий обработчик для выбора пользователя
        self.bot.register_next_step_handler(message, self.process_certificate_choice)

    def process_certificate_choice(self, message):
        """Обрабатывает выбор пользователя после отображения клавиатуры справок."""
        user_id = message.from_user.id
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id]['certificate_type'] = message.text
        choice_map = {
            'Справка о месте жительства и составе семьи': self.ask_for_address,
            'Справка о месте жительства': self.ask_for_address,
            'Справка о занимаемом жилом помещении и составе семьи': self.ask_for_address,
            'Справка о последнем месте жительства наследодателя и о составе его семьи': self.ask_for_address,
            'Вернуться назад': self.handle_back
        }
        handler_function = choice_map.get(message.text)
        if handler_function:
            handler_function(message)
        else:
            self.handle_unknown(message, self.show_certificate_options)


    def ask_for_address(self, message):
        """Запрашивает у пользователя адрес проживания."""
        user_id = message.from_user.id
        if not hasattr(self, 'user_data'):
            self.user_data = {}
        self.user_data[user_id] = {'certificate_type': message.text}  # Предполагаем, что тип справки уже сохранен
        self.bot.send_message(message.chat.id, "Введите адрес проживания (город, улица, дом):")
        self.bot.register_next_step_handler(message, self.ask_for_full_name)

    def ask_for_full_name(self, message):
        """Запрашивает у пользователя ФИО."""
        user_id = message.from_user.id
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        # Сохраняем адрес перед получением ФИО
        self.user_data[user_id]['address'] = message.text
        self.bot.send_message(message.chat.id, "Введите ФИО полностью:")
        self.bot.register_next_step_handler(message, self.ask_for_birth_date)

    def ask_for_birth_date(self, message):
        """Запрашивает у пользователя дату рождения."""
        user_id = message.from_user.id
        self.user_data[user_id]['full_name'] = message.text  # Теперь правильно сохраняем ФИО
        self.bot.send_message(message.chat.id, "Введите дату рождения (в формате ДД.ММ.ГГГГ):")
        self.bot.register_next_step_handler(message, self.ask_for_extra_details)

    def ask_for_extra_details(self, message):
        """Запрашивает у пользователя дополнительные сведения."""
        user_id = message.from_user.id
        self.user_data[user_id]['birth_date'] = message.text  # Правильно сохраняем дату рождения
        self.bot.send_message(message.chat.id, "Введите дополнительные сведения (если необходимо):")
        self.bot.register_next_step_handler(message, self.confirm_and_display_data)

    def confirm_and_display_data(self, message):
        user_id = message.from_user.id
        self.user_data[user_id]['extra_details'] = message.text  # Сохраняем дополнительные сведения
        # Формирование сообщения для подтверждения данных
        confirmation_message = f"Пожалуйста, проверьте введенные данные:\n\n" \
                               f"Тип справки: {self.user_data[user_id]['certificate_type']}\n" \
                               f"Адрес: {self.user_data[user_id]['address']}\n" \
                               f"ФИО: {self.user_data[user_id]['full_name']}\n" \
                               f"Дата рождения: {self.user_data[user_id]['birth_date']}\n" \
                               f"Дополнительные сведения: {self.user_data[user_id]['extra_details']}"
        # Отправка сообщения с подтверждением и кнопками для выбора
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton('Данные верны'), types.KeyboardButton('Редактировать'))
        self.bot.send_message(message.chat.id, confirmation_message, reply_markup=markup)
        self.bot.register_next_step_handler(message, self.final_confirmation)

    def final_confirmation(self, message):
        """Обрабатывает ответ пользователя на подтверждение данных."""
        user_info = message.from_user
        user_name = f"{user_info.first_name} {user_info.last_name}" if user_info.last_name else user_info.first_name
        user_id = user_info.id
        username = user_info.username
        # Телефонный номер нельзя получить напрямую через message.from_user, его можно получить только если пользователь явно отправил его через специальный интерфейс.
        # phone_number = user_info.phone_number if hasattr(user_info, 'phone_number') else 'Не указан'

        if message.text == 'Данные верны':
            # Данные подтверждены, можно их сохранять/обрабатывать
            user_data = self.user_data.get(user_id, {})
            # Подготовка строки с информацией о пользователе
            user_info_str = (
                f"Имя: {user_name}\n"
                f"ID: {user_id}\n"
                f"Username: @{username}")
            # Передаем эту строку в функцию отправки уведомления
            send_notification(user_id, user_data, user_info_str)
            # Здесь ваш код для обработки и сохранения данных заявки...
            # self.complete_certificate_request(user_id)
            self.show_final_choice(message)
        elif message.text == 'Редактировать':
            # Пользователь выбрал редактирование данных
            self.edit_user_data(message)  # Убедитесь, что edit_user_data правильно обрабатывает передачу message
        else:
            self.handle_unknown(message, self.confirm_and_display_data)

    def edit_user_data(self, message):
        """Позволяет пользователю редактировать введенные ранее данные."""
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        buttons = [
            'Изменить адрес',
            'Изменить ФИО',
            'Изменить дату рождения',
            'Изменить дополнительные сведения',
            'Отмена'
        ]
        for button in buttons:
            markup.add(types.KeyboardButton(button))
        self.bot.send_message(user_id, "Какие данные вы хотите изменить?", reply_markup=markup)
        self.bot.register_next_step_handler_by_chat_id(user_id, self.process_edit_choice)

    def process_edit_choice(self, message):
        """Обрабатывает выбор пользователя при редактировании данных."""
        user_id = message.from_user.id
        # Проверяем, какие данные пользователь хочет изменить и вызываем соответствующий метод
        if message.text == 'Изменить адрес':
            self.ask_for_address(message)
        elif message.text == 'Изменить ФИО':
            self.ask_for_full_name(message)
        elif message.text == 'Изменить дату рождения':
            self.ask_for_birth_date(message)
        elif message.text == 'Изменить дополнительные сведения':
            self.ask_for_extra_details(message)
        elif message.text == 'Отмена':
            self.show_certificate_options(message)  # Отмена и возвращение к выбору справок
        else:
            self.bot.send_message(user_id, "Неизвестный выбор. Пожалуйста, попробуйте еще раз.")
            self.edit_user_data(user_id)

    def confirmation_and_save(self, message):
        """Сохраняет все данные справки и подтверждает пользователю завершение процесса."""
        user_id = message.from_user.id
        # Здесь можно реализовать логику проверки и сохранения данных, отправки их на сервер или в базу данных
        self.complete_certificate_request(user_id)

    def complete_certificate_request(self, user_id):
        """Завершает процесс заказа справки."""
        # Предполагаем, что данные пользователя уже сохранены в self.user_data[user_id]
        user_data = self.user_data.get(user_id, {})
        # Отправляем уведомление о новой заявке
        send_notification(user_id, user_data)
        # Уведомляем пользователя о принятии заявки
        self.bot.send_message(user_id, "Ваша заявка принята и будет обработана в ближайшее время.")

    def show_final_choice(self, message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        buttons = ["Заказать еще справку", "Вернуться в главное меню", "Спасибо за информацию"]
        for button in buttons:
            markup.add(types.KeyboardButton(button))
        self.bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.handle_final_choice)

    def handle_final_choice(self, message):
        if message.text == "Заказать еще справку":
            self.show_certificate_options(message)
        elif message.text == "Вернуться в главное меню":
            from .StartHandler import StartHandler
            StartHandler(self.bot).handle(message)
        elif message.text == "Спасибо за информацию":
            self.bot.send_message(message.chat.id, "Спасибо! Если у вас возникнут дополнительные вопросы, вы всегда можете к нам обратиться.")
        else:
            self.bot.send_message(message.chat.id, "Неизвестная команда, пожалуйста, выберите один из предложенных вариантов.")
            self.show_final_choice(message)  # Предложить пользователю снова сделать выбор
