import requests
from config import TELEBOT_TOKEN
from config import id_chat_owner


def send_notification(user_id, user_info_str):
    try:
        chat_id = id_chat_owner # ID чата владельца бота
        token = TELEBOT_TOKEN   # Убедитесь, что здесь ваш действительный токен
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {'chat_id': chat_id, 'text': user_info_str, 'parse_mode': 'Markdown'}
        response = requests.post(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")




