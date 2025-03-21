import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')
OWNER_ID: int = int(os.getenv("OWNER_ID", "0"))
BOT_TOKEN = os.getenv('BOT_TOKEN')
DUMP_CHAT_ID = os.getenv('DUMP_CHAT_ID')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 8443))
