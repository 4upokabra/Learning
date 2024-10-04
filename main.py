import os
import aiohttp
import asyncio
import logging
import subprocess
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button
from datetime import datetime


# Загрузка переменных окружения из файла .env
load_dotenv()

# Ваши данные для авторизации
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
backend_url = os.getenv('BACKEND_URL')

# Белый список пользователей
whitelist = [int(user_id) for user_id in os.getenv('WHITELIST', '').split(',') if user_id.isdigit()]

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация клиента
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Функция для создания папки пользователя
def create_user_folder(user_id):
    user_folder = f'users/{user_id}'
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

# Функция для проверки пользователя в белом списке
def is_whitelisted(user_id):
    return user_id in whitelist

# Обработчик для команды /start
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    if is_whitelisted(user_id):
        await event.respond('''
Привет! Этот бот позволяет сохранять и управлять файлами.

Команды:
- /list: Показать список сохраненных файлов.
- Отправьте файл, чтобы сохранить его.

Пожалуйста, отправьте файл или используйте команду /list для просмотра сохраненных файлов.
''')
    else:
        await event.respond('Извините, у вас нет доступа к этому боту.')

# Обработчик для получения файлов
@client.on(events.NewMessage(func=lambda e: e.file))
async def handle_file(event):
    user_id = event.sender_id
    if is_whitelisted(user_id):
        user_folder = create_user_folder(user_id)

        # Получаем файл
        file_name = event.file.name
        file_type = event.file.mime_type
        if file_name is None:
            file_name = f'file_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

        file_path = await event.download_media(file=os.path.join(user_folder, file_name))
        if file_type == 'application/x-python-code':
            try:
                subprocess.run(['python', file_path], check=True)
                logger.info(f"Message with file from user {user_id} successfully started")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error executing file from user {user_id}: {e}")
                await event.respond(f'Ошибка при выполнении файла: {e}')
        await event.respond(f'Файл сохранен: {file_path}')
        await client.delete_messages(event.chat_id, event.message.id)
        logger.info(f"Message with file from user {user_id} deleted")
    else:
        await event.respond('Извините, у вас нет доступа к этому боту.')

# Обработчик для команды просмотра файлов
@client.on(events.NewMessage(pattern='/list'))
async def list_files(event):
    user_id = event.sender_id
    if is_whitelisted(user_id):
        user_folder = create_user_folder(user_id)

        files = os.listdir(user_folder)
        if files:
            buttons = []
            for file in files:
                buttons.append(Button.inline(file, data=f'download_{file}'))
            await event.respond('Ваши файлы:', buttons=buttons)
        else:
            await event.respond('У вас нет сохраненных файлов.')
    else:
        await event.respond('Извините, у вас нет доступа к этому боту.')

# Обработчик для команды скачивания файла
@client.on(events.CallbackQuery(pattern=r'download_(.+)'))
async def download_file(event):
    user_id = event.sender_id
    if is_whitelisted(user_id):
        user_folder = create_user_folder(user_id)
        file_name = event.pattern_match.group(1).decode('utf-8')  # Преобразование байтовой строки в обычную строку
        file_path = os.path.join(user_folder, file_name)

        if os.path.exists(file_path):
            message = await event.respond(file=file_path)
            await asyncio.sleep(15)  # Задержка на 15 секунд
            await client.delete_messages(event.chat_id, message.id)
        else:
            await event.respond('Файл не найден.')
    else:
        await event.respond('Извините, у вас нет доступа к этому боту.')

client.run_until_disconnected()
