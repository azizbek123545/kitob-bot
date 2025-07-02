"""
Production configuration file for the Telegram bot with admin panel
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration - Your actual bot credentials
BOT_TOKEN = os.getenv("BOT_TOKEN", "7717992642:AAG1NaiRIxJqq8VTAOL7I0UWnQRMnnd2ax8")
BOT_USERNAME = os.getenv("BOT_USERNAME", "Kitob_Bazasi_botAIPromptYordamchi_Bot")

# Admin User IDs (from environment variable or default)
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "123456789,987654321")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()]

# Required Channels for subscription - Your actual channels
REQUIRED_CHANNELS = {
    "channel1": "https://t.me/Kitob_Bazasi_1",
    "channel2": "https://t.me/ITBlogUz1", 
    "channel3": "https://t.me/ieltsgram_test",
    "channel4": "https://t.me/deepreadClub"
}

# Channel IDs for verification - Your actual channel IDs with proper -100 prefix
CHANNEL_IDS = {
    "channel1": os.getenv("CHANNEL1_ID", "-1002593361788"),
    "channel2": os.getenv("CHANNEL2_ID", "-1002834612989"),
    "channel3": os.getenv("CHANNEL3_ID", "-1002810716295"), 
    "channel4": os.getenv("CHANNEL4_ID", "-1002632397336")
}

# Channel names for display (in Uzbek)
CHANNEL_NAMES = {
    "channel1": "Kitob Bazasi",
    "channel2": "IT Blog Uz",
    "channel3": "IELTS Gram Test",
    "channel4": "Deep Read Club"
}

# Final promotion channel
PROMO_CHANNEL = "https://t.me/Kitob_Bazasi_1"

# Database and file paths
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/bot_database.db")
BOOKS_DIR = os.getenv("BOOKS_DIR", "data/books")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")

# Security settings
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "52428800"))  # 50MB
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"

# Create directories if they don't exist
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
os.makedirs(BOOKS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Bot info for logging
print(f"🤖 Bot configured: @{BOT_USERNAME}")
print(f"📊 Admin IDs: {ADMIN_IDS}")
print(f"📢 Monitoring {len(CHANNEL_IDS)} channels")