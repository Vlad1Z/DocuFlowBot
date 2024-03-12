from telebot import types
from .BaseHandler import BaseHandler
from utils import send_notification
from datetime import datetime


class CertificateHandler(BaseHandler):
    """
    Класс для обработки запросов на получение различных справок от пользователя.
    Отображает опции справок и обрабатывает последующий ввод данных.
    """
    def handle(self, message):
        """
        Основной метод для обработки входящего сообщения.
        Выводит пользователю клавиатуру с выбором справок.
        """
        self.show_certificate_options(message)

    def show_certificate_options(self, message):
        """
        Отображает клавиатуру с опциями справок, доступных для запроса.
        """
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
        self.bot.send_message(message.chat.id, "Выберите тип справки:", reply_markup=certificate_markup)
        self.bot.register_next_step_handler(message, self.process_certificate_choice)

    def process_certificate_choice(self, message):
        """
        Обрабатывает выбор справки пользователем.
        Запускает процесс сбора дополнительной информации.
        """
        user_id = message.from_user.id
        if user_id not in self.user_data:
            self.user_data[user_id] = {}

        # Здесь мы устанавливаем тип справки в user_data
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
            # Перед вызовом функции handler_function сохраняем тип справки
            handler_function(message)
        else:
            self.handle_unknown(message, self.show_certificate_options)

    def ask_for_address(self, message, return_to_confirmation=False):
        """
        Запрашивает у пользователя адрес.
        В зависимости от параметра 'return_to_confirmation', определяет следующий шаг в процессе.
        """
        self.bot.send_message(message.chat.id, "Введите адрес регистарции (Город, улица, дом, корпус, квартира):")
        next_step_handler = self.save_address_and_confirm if return_to_confirmation else self.save_address
        self.bot.register_next_step_handler(message, lambda msg: self.validate_input(msg, next_step_handler))

    def save_address(self, message):
        """
        Сохраняет адрес пользователя и запрашивает следующий набор данных.
        """
        user_id = message.from_user.id
        address = message.text.strip()
        if not BaseHandler.contains_two_numbers_and_text(address):
            msg = self.bot.send_message(message.chat.id, "Адрес введен некорректно. Убедитесь, что он содержит название улицы, номер дома, номер квартиры, и повторите попытку:")
            self.bot.register_next_step_handler(msg, self.save_address)
        else:
            self.user_data[user_id]['address'] = address
            self.ask_for_full_name(message)

    def save_address_and_confirm(self, message):
        """
        Сохраняет адрес пользователя и переходит к подтверждению данных.
        """
        user_id = message.from_user.id
        address = message.text.strip()
        if not BaseHandler.contains_two_numbers_and_text(address):
            msg = self.bot.send_message(message.chat.id,
                                        "Адрес введен некорректно. Убедитесь, что он содержит название улицы, номер дома, номер квартиры, и повторите попытку:")
            self.bot.register_next_step_handler(msg, self.save_address_and_confirm)
        else:
            self.user_data[user_id]['address'] = address
            self.confirm_and_display_data(message)

    def ask_for_full_name(self, message, return_to_confirmation=False):
        """
        Запрашивает у пользователя ФИО для справки.
        """
        self.bot.send_message(message.chat.id, "Введите ФИО полностью того, на кого оформляется справка:")
        next_step_handler = self.save_full_name_and_confirm if return_to_confirmation else self.save_full_name
        self.bot.register_next_step_handler(message, lambda msg: self.validate_input(msg, next_step_handler))

    def save_full_name(self, message):
        """
        Сохраняет ФИО пользователя.
        """
        user_id = message.from_user.id
        full_name = message.text.strip()  # Удаляем лишние пробелы по краям
        # Простая проверка на количество слов в ФИО
        if len(full_name.split()) >= 3 and len(full_name) > 4:
            self.user_data[user_id]['full_name'] = full_name
            self.ask_for_birth_date(message)
        else:
            msg = self.bot.send_message(
                message.chat.id,
                "Пожалуйста, введите ваше полное ФИО."
            )
            self.bot.register_next_step_handler(msg, self.save_full_name)

    def save_full_name_and_confirm(self, message):
        """
        Сохраняет ФИО пользователя и переходит к подтверждению данных.
        """
        user_id = message.from_user.id
        full_name = message.text.strip()  # Удаляем лишние пробелы по краям
        # Простая проверка на количество слов в ФИО
        if len(full_name.split()) >= 3 and len(full_name) > 4:
            self.user_data[user_id]['full_name'] = full_name
            self.confirm_and_display_data(message)
        else:
            msg = self.bot.send_message(
                message.chat.id,
                "Пожалуйста, введите ваше полное ФИО."
            )
            self.bot.register_next_step_handler(msg, self.save_full_name_and_confirm)

    def ask_for_birth_date(self, message, return_to_confirmation=False):
        """Сохраняет дату рождения пользователя после проверки формата даты."""
        user_id = message.from_user.id
        self.bot.send_message(message.chat.id, "Введите дату рождения (в формате ДД.ММ.ГГГГ):")
        if return_to_confirmation:
            next_step_handler = self.save_birth_date_and_confirm
        else:
            next_step_handler = self.save_birth_date
        self.bot.register_next_step_handler(message, next_step_handler)

    def save_birth_date(self, message):
        """Сохраняет дату рождения пользователя после проверки валидности."""
        user_id = message.from_user.id
        date_text = message.text
        try:
            # Попытка преобразовать текст в дату
            birth_date = datetime.strptime(date_text, '%d.%m.%Y')
            # Если дата корректна, сохраняем и переходим к следующему шагу
            self.user_data[user_id]['birth_date'] = birth_date.strftime('%d.%m.%Y')
            self.ask_for_number_of_certificates(message)
        except ValueError:
            # Если дата некорректна, просим ввести снова
            msg = self.bot.send_message(
                message.chat.id,
                "Дата введена некорректно. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ:"
            )
            self.bot.register_next_step_handler(msg, self.save_birth_date)

    def save_birth_date_and_confirm(self, message):
        """Сохраняет Дату рождения пользователя и возвращает его к подтверждению данных."""
        user_id = message.from_user.id
        date_text = message.text
        try:
            # Попытка преобразовать текст в дату
            birth_date = datetime.strptime(date_text, '%d.%m.%Y')
            # Если дата корректна, сохраняем и продолжаем
            self.user_data[user_id]['birth_date'] = birth_date.strftime('%d.%m.%Y')
            self.confirm_and_display_data(message)
        except ValueError:
            # Если дата некорректна, просим ввести снова
            msg = self.bot.send_message(message.chat.id,
                                        "Дата введена некорректно. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ:")
            self.bot.register_next_step_handler(msg, self.save_birth_date_and_confirm)

    def ask_for_number_of_certificates(self, message, return_to_confirmation=False):
        """Запрашивает у пользователя количество необходимых справок."""
        user_id = message.from_user.id
        self.bot.send_message(message.chat.id, "Введите необходимое количество справок:")
        if return_to_confirmation:
            next_step_handler = self.save_number_of_certificates_and_confirm
        else:
            next_step_handler = self.save_number_of_certificates
        self.bot.register_next_step_handler(message, next_step_handler)

    def save_number_of_certificates(self, message):
        """Сохраняет количество запрашиваемых пользователем справок."""
        user_id = message.from_user.id
        try:
            number = int(message.text)
            if not 1 <= number <= 10:
                raise ValueError
            self.user_data[user_id]['number_of_certificates'] = number
            self.ask_for_extra_details(message)
        except ValueError:
            self.bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 10.")
            # Повторно запросите ввод количества справок, если ввод некорректен
            self.bot.register_next_step_handler(message, self.save_number_of_certificates)

    def save_number_of_certificates_and_confirm(self, message):
        """Сохраняет необходимое Количество справок пользователя и возвращает его к подтверждению данных."""
        user_id = message.from_user.id
        try:
            number = int(message.text)
            if not 1 <= number <= 10:
                raise ValueError
            self.user_data[user_id]['number_of_certificates'] = number
            self.confirm_and_display_data(message)
        except ValueError:
            self.bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 10.")
            # Повторно запросите ввод количества справок, если ввод некорректен
            self.bot.register_next_step_handler(message, self.save_number_of_certificates)

    def ask_for_extra_details(self, message, return_to_confirmation=False):
        """Запрашивает у пользователя дополнительные сведения, если они необходимы для справки."""
        self.bot.send_message(message.chat.id, "Введите дополнительные сведения (если необходимо):")
        next_step_handler = self.save_extra_details_and_confirm if return_to_confirmation else self.save_extra_details
        self.bot.register_next_step_handler(message,
                                            lambda msg: self.validate_input(msg, next_step_handler))

    def save_extra_details(self, message):
        """Сохраняет дополнительные сведения, предоставленные пользователем."""
        user_id = message.from_user.id
        self.user_data[user_id]['extra_details'] = message.text
        self.confirm_and_display_data(message)

    def save_extra_details_and_confirm(self, message):
        """Сохраняет дополнительные сведения пользователя и переходит к подтверждению данных."""
        user_id = message.from_user.id
        self.user_data[user_id]['extra_details'] = message.text
        self.confirm_and_display_data(message)

    def confirm_and_display_data(self, message):
        """Отображает пользователю все введённые данные для подтверждения перед финальной отправкой."""
        user_id = message.from_user.id
        # Здесь уже все данные сохранены, просто извлекаем их для подтверждения
        address = self.user_data[user_id].get('address', 'Не указан')
        full_name = self.user_data[user_id].get('full_name', 'Не указано')
        birth_date = self.user_data[user_id].get('birth_date', 'Не указана')
        number_of_certificates = self.user_data[user_id].get('number_of_certificates', 'Не указана')
        extra_details = self.user_data[user_id].get('extra_details', 'Не указано')
        certificate_type = self.user_data[user_id].get('certificate_type', 'Не указано')

        confirmation_message = f"""Пожалуйста, проверьте введенные данные:

    Тип справки: {certificate_type}
    Адрес: {address}
    ФИО: {full_name}
    Дата рождения: {birth_date}
    Количество справок: {number_of_certificates}
    Дополнительные сведения: {extra_details}"""

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton('Данные верны'), types.KeyboardButton('Редактировать'),types.KeyboardButton('Отменить заказ справки'))
        self.bot.send_message(message.chat.id, confirmation_message, reply_markup=markup)
        self.bot.register_next_step_handler(message, self.ask_for_phone_number)

    def ask_for_phone_number(self, message):
        """Запрашивает у пользователя номер телефона для возможной обратной связи."""
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        button_cancel = types.KeyboardButton(text="Отмена")
        markup.add(button_phone, button_cancel)
        msg = self.bot.send_message(message.chat.id,
                                    "Для обратной связи, пожалуйста, поделитесь своим номером телефона или нажмите 'Отмена'.",
                                    reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.handle_phone_number)

    def handle_phone_number(self, message):
        """Обрабатывает номер телефона, предоставленный пользователем, или его отказ от предоставления."""
        user_info = message.from_user
        user_data = self.user_data.get(user_info.id, {})
        user_name = f"{user_info.first_name} {user_info.last_name}" if user_info.last_name else user_info.first_name
        phone_number = "Не указан"

        if message.contact is not None:
            # Пользователь поделился номером телефона
            phone_number = message.contact.phone_number
            user_data['phone_number'] = phone_number  # Сохраняем номер телефона
            self.bot.send_message(message.chat.id, "Спасибо, ваш номер телефона получен.",
                                  reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "Отмена":
            # Пользователь выбрал "Отмена"
            self.bot.send_message(message.chat.id, "Вы отменили отправку номера телефона.",
                                  reply_markup=types.ReplyKeyboardRemove())
        else:
            # Неожиданный ввод
            self.ask_for_phone_number(message)  # Повторный запрос на номер телефона
            return

        # Формируем строку с информацией о пользователе для уведомления
        user_info_str = (
            f"Имя: {user_name}\n"
            f"ID: {user_info.id}\n"
            f"Username: @{user_info.username if user_info.username else 'Не указан'}\n"
            f"Телефон: {phone_number}"
        )

        # Отправляем уведомление
        send_notification(user_info.id, user_data, user_info_str)

        # Переходим к финальному выбору
        self.show_final_choice(message)

    def final_confirmation(self, message, phone_number=None):
        """Заключительный этап, где пользователь подтверждает все введённые данные."""
        user_info = message.from_user
        user_name = f"{user_info.first_name} {user_info.last_name}" if user_info.last_name else user_info.first_name
        user_id = user_info.id
        username = user_info.username
        user_data = self.user_data.get(user_id, {})
        if phone_number:
            user_data['phone_number'] = phone_number

        if message.text == 'Данные верны' or phone_number:
            # Подготовка строки с информацией о пользователе и его данных
            user_info_str = (
                f"Имя: {user_name}\n"
                f"ID: {user_id}\n"
                f"Username: @{username}\n"
                f"Телефон: {user_data.get('phone_number', 'Не указан')}")
            # Передаем эту строку в функцию отправки уведомления и дальнейшую обработку
            send_notification(user_id, user_data, user_info_str)
            self.show_final_choice(message)
        elif message.text == 'Редактировать':
            self.edit_user_data(message)
        elif message.text == 'Отменить заказ справки':
            from .StartHandler import StartHandler
            StartHandler(self.bot).handle(message)
        else:
            self.handle_unknown(message, self.confirm_and_display_data)
        return

    def edit_user_data(self, message):
        """Позволяет пользователю редактировать введенные ранее данные."""
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        buttons = [
            'Изменить адрес',
            'Изменить ФИО',
            'Изменить дату рождения',
            'Изменить количество справок',
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
        if message.text == 'Изменить адрес':
            self.ask_for_address(message, return_to_confirmation=True)
        elif message.text == 'Изменить ФИО':
            self.ask_for_full_name(message, return_to_confirmation=True)
        elif message.text == 'Изменить дату рождения':
            self.ask_for_birth_date(message, return_to_confirmation=True)
        elif message.text == 'Изменить количество справок':
            self.ask_for_number_of_certificates(message, return_to_confirmation=True)
        elif message.text == 'Изменить дополнительные сведения':
            self.ask_for_extra_details(message, return_to_confirmation=True)
        elif message.text == 'Отмена':
            self.confirm_and_display_data(message)
        else:
            self.handle_unknown(message, self.confirm_and_display_data)

    def show_final_choice(self, message):
        """
        Показывает пользователю финальные опции после обработки и подтверждения всех данных.
        """
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        buttons = ["Заказать еще справку", "Вернуться в главное меню", "Спасибо за информацию"]
        for button in buttons:
            markup.add(types.KeyboardButton(button))
        self.bot.send_message(message.chat.id, "Спасибо! Ваша заявка принята и будет обработана в ближайшее время.", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.handle_final_choice)

    def handle_final_choice(self, message):
        """
        Обрабатывает финальный выбор пользователя после получения справки.
        """
        if message.text == "Заказать еще справку":
            self.show_certificate_options(message)
        elif message.text == "Вернуться в главное меню":
            from .StartHandler import StartHandler
            StartHandler(self.bot).handle(message)
        elif message.text == "Спасибо за информацию":
            self.bot.send_message(message.chat.id, "Спасибо! Если у вас возникнут дополнительные вопросы, вы всегда можете к нам обратиться.")
        else:
            self.bot.send_message(message.chat.id, "Неизвестная команда, пожалуйста, выберите один из предложенных вариантов.")
            self.show_final_choice(message)
