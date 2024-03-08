import requests


def send_notification(user_id, data, user_info_str):
    try:
        chat_id = '1753749064'  # ID чата владельца бота
        token = "6592198559:AAG77aB9aIvhcZMUZzKTTQ2TRhqRZWa0FW4"  # Убедитесь, что здесь ваш действительный токен
        message = (
            f"Новый запрос от пользователя:\n{user_info_str}\n\n"
            f"Тип справки: {data.get('certificate_type', 'Не указано')}\n"
            f"Адрес: {data.get('address', 'Не указан')}\n"
            f"ФИО: {data.get('full_name', 'Не указано')}\n"
            f"Дата рождения: {data.get('birth_date', 'Не указана')}\n"
            f"Дополнительные сведения: {data.get('extra_details', 'Не указано')}"
        )
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")



