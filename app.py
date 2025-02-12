import os
import telebot
from flask import Flask, request
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv

# Загрузка конфигураций из .env файла
load_dotenv()

# Инициализация Flask
app = Flask(__name__)

# Инициализация Firebase
cred = credentials.Certificate(os.getenv('firebase-credentials.json'))
firebase_app = initialize_app(cred)
db = firestore.client()

# Инициализация Telegram Bot API
bot = telebot.TeleBot(os.getenv('7551355568:AAEWx4fUrqfzGXqpsH2skkXr6wVS9-h6UTU'))

# Обработчик команды "/start" для получения ID пользователя
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
# Обработчик команд для обновления монет
@app.route('/update_coins', methods=['POST'])
def update_coins():
    data = request.get_json()

    user_id = data.get('user_id')
    coins = data.get('coins')

    if not user_id or coins is None:
        return "Invalid data", 400

    user_ref = db.collection('users').document(str(user_id))

    user_doc = user_ref.get()
    if user_doc.exists:
        current_coins = user_doc.to_dict().get('coins', 0)
        user_ref.update({'coins': current_coins + coins})
    else:
        user_ref.set({'coins': coins})

    return "Coins updated", 200

# Обработчик команд для получения монет
@app.route('/get_coins/<user_id>', methods=['GET'])
def get_coins(user_id):
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        coins = user_doc.to_dict().get('coins', 0)
        return {"coins": coins}, 200
    return {"coins": 0}, 200

# Запуск сервера Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
