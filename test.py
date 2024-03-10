def ask_for_extra_details(self, message, return_to_confirmation=False):
    user_id = message.from_user.id
    self.bot.send_message(message.chat.id, "Введите дополнительные сведения (если необходимо):")
    if return_to_confirmation:
        next_step_handler = self.save_extra_details_and_confirm
    else:
        next_step_handler = self.save_extra_details
    self.bot.register_next_step_handler(message, next_step_handler)


def save_extra_details(self, message):
    user_id = message.from_user.id
    self.user_data[user_id]['extra_details'] = message.text
    self.confirm_and_display_data(message)


def save_extra_details_and_confirm(self, message):
    """Сохраняет Дополнительные сведения пользователя и возвращает его к подтверждению данных."""
    user_id = message.from_user.id
    self.user_data[user_id]['extra_details'] = message.text
    self.confirm_and_display_data(message)



def ask_for_number_of_certificates(self, message, return_to_confirmation=False):
    user_id = message.from_user.id
    self.bot.send_message(message.chat.id, "Введите необходимое количество справок:")
    if return_to_confirmation:
        next_step_handler = self.save_number_of_certificates_and_confirm
    else:
        next_step_handler = self.save_number_of_certificates
    self.bot.register_next_step_handler(message, next_step_handler)

def save_number_of_certificates(self, message):
    user_id = message.from_user.id
    self.user_data[user_id]['number_of_certificates'] = message.text
    self.confirm_and_display_data(message)

def save_extra_details_and_confirm(self, message):
    """Сохраняет необходимое Количество справок пользователя и возвращает его к подтверждению данных."""
    user_id = message.from_user.id
    self.user_data[user_id]['number_of_certificates'] = message.text
    self.confirm_and_display_data(message)


