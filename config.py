import os
from dotenv import load_dotenv  # Load environment variables from .env file

# Load environment variables from .env (if present)
load_dotenv()

# Retrieve environment variables with type safety
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
OWNER_ID: int = int(os.getenv("OWNER_ID", "0"))  # Convert to int
DUMP_CHAT_ID: int = int(os.getenv("DUMP_CHAT_ID", "0"))  # Convert to int
MONGO_URL: str = os.getenv("MONGO_URL", "")
WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
PORT: int = int(os.getenv("PORT", "8443"))  # Default to 8443 if not set
