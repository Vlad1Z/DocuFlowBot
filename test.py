
def ask_for_phone_number(self, message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    markup.add(button_phone)
    self.bot.send_message(message.chat.id, "Для обратной связи, пожалуйста, поделитесь своим номером телефона.", reply_markup=markup)

def handle_phone_number(self, message):
    if message.contact is not None:
        user_id = message.from_user.id
        phone_number = message.contact.phone_number
        # Здесь вы можете сохранить номер телефона в своей базе данных или выполнить другие действия
        self.bot.send_message(message.chat.id, "Спасибо, ваш номер телефона получен.", reply_markup=types.ReplyKeyboardRemove())
    else:
        self.bot.send_message(message.chat.id, "Не удалось получить номер телефона. Пожалуйста, попробуйте еще раз.", reply_markup=types.ReplyKeyboardRemove())

# Не забудьте зарегистрировать handle_phone_number для обработки следующего шага после ask_for_phone_number
# Например, через self.bot.register_next_step_handler(message, self.handle_phone_number) после отправки запроса на номер телефона.
