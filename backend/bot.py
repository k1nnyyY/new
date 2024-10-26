import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import hashlib
import os
import subprocess

API_TOKEN = '7707557872:AAG--9m0u1aAsDjW_Vaijm-8c9tYlJ4Qwbw'
PASSWORD_FILE = 'passwords.txt'
DATA_FILE_PATH = "/app/shared_data/data.txt"
DEFAULT_PASSWORD_HASH = hashlib.sha256('666'.encode()).hexdigest()

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


registered_users = set()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_password_file():
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'w') as file:
            file.write(DEFAULT_PASSWORD_HASH + '\n')

# Функция для проверки пароля
def check_password(password):
    hashed_password = hash_password(password)
    with open(PASSWORD_FILE, 'r') as file:
        return hashed_password in file.read().splitlines()

# Хэндлер для старта и регистрации
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    if message.from_user.id in registered_users:
        await message.answer("Вы уже зарегистрированы. Можете присылать данные.")
    else:
        await message.answer("Пожалуйста, введите пароль для регистрации.")

# Хэндлер для обработки пароля
@dp.message()
async def password_handler(message: types.Message):
    # Проверяем, зарегистрирован ли пользователь
    if message.from_user.id in registered_users:
        # Если пользователь зарегистрирован, он может присылать данные
        await handle_data(message)
        return
    
    if message.text is None:
        await message.answer("Сообщение не содержит текста. Пожалуйста, введите пароль.")
        return

    # Проверка пароля
    if check_password(message.text):
        registered_users.add(message.from_user.id)
        await message.answer("Регистрация прошла успешно. Теперь вы можете присылать данные.")
    else:
        await message.answer("Неверный пароль. Попробуйте снова.")

# Хэндлер для обработки данных
async def handle_data(message: types.Message):
    # Получаем текст из сообщения
    data_text = message.text
    lines = data_text.split('\n')

    required_keys = {
        'mos', 'inpol', 'first_name', 'last_name', 'passport_code',
        'country', 'email', 'radio_choice', 'date_of_birth', 'guardian_name'
    }

    # Проверяем данные
    parsed_data = {}
    errors = []
    for line in lines:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            parsed_data[key] = value
        else:
            errors.append(f"Ошибка в строке: {line.strip()}")

    missing_keys = required_keys - parsed_data.keys()
    if missing_keys:
        errors.append(f"Отсутствуют необходимые переменные: {', '.join(missing_keys)}")

    if errors:
        await message.answer(f"Данные не сохранены. Обнаружены следующие ошибки:\n" + "\n".join(errors))
    else:
        # Удаляем старый data.txt, если он существует
        if os.path.exists(DATA_FILE_PATH):
            os.remove(DATA_FILE_PATH)
        
        # Сохраняем данные в новый data.txt
        with open(DATA_FILE_PATH, 'w') as new_file:
            for key, value in parsed_data.items():
                new_file.write(f"{key}={value}\n")
        
        await message.answer("Данные успешно сохранены!")

        # Запускаем парсер
        run_parser()

# Функция для запуска парсера
def run_parser():
    try:
        # Здесь мы предполагаем, что "parser.py" — это скрипт, который нужно выполнить
        subprocess.run(["python", "./parser/parser.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске парсера: {e}")

# Запуск бота
async def main():
    init_password_file()  # Инициализация файла с паролями при первом запуске
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
