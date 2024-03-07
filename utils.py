import requests


def send_notification(user_id, data):
    try:
        chat_id = '1753749064'  # ID чата владельца бота
        # Используем .get() для избежания KeyError
        message = f"Новый запрос:\nТип справки: {data.get('type', 'Неизвестный тип')}\nАдрес: {data.get('address', 'Не указан')}\nФИО: {data.get('name', 'Не указано')}\nДата рождения: {data.get('birthdate', 'Не указана')}\nКоличество справок: {data.get('count', '1')}"
        url = "https://api.telegram.org/bot6592198559:AAG77aB9aIvhcZMUZzKTTQ2TRhqRZWa0FW4/sendMessage"
        params = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")

