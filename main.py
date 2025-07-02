"""
Enhanced main bot application file with Railway deployment support
"""

import asyncio
import logging
import os
import sys
import threading
from logging.handlers import RotatingFileHandler
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    MessageHandler, 
    ConversationHandler,
    filters
)

from config import BOT_TOKEN, LOG_LEVEL, LOG_FILE
from handlers.start import start_command, subscription_callback
from handlers.books import handle_book_code
from handlers.admin import (
    admin_menu, 
    admin_callback_handler,
    handle_book_code as admin_handle_book_code,
    handle_book_title,
    handle_book_file,
    handle_test_file,
    handle_broadcast_message,
    cancel_conversation,
    WAITING_BOOK_CODE,
    WAITING_BOOK_TITLE,
    WAITING_BOOK_FILE,
    WAITING_TEST_FILE,
    WAITING_BROADCAST_MESSAGE
)
from database.db_manager import DatabaseManager

def setup_logging():
    """Setup logging configuration for production"""
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(sys.stdout),
            # File handler with rotation
            RotatingFileHandler(
                LOG_FILE,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    # Set specific loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.INFO)
    
    return logging.getLogger(__name__)

def start_health_server():
    """Start health check server for Railway"""
    from health_check import start_health_server
    try:
        start_health_server()
    except Exception as e:
        logging.getLogger(__name__).warning(f"Health server failed to start: {e}")

async def error_handler(update, context):
    """Global error handler"""
    logger = logging.getLogger(__name__)
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Notify user about the error
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
            )
        except Exception:
            pass

async def main():
    """Main function to start the bot"""
    logger = setup_logging()
    logger.info("🚀 Starting Telegram Bot on Railway...")
    
    # Start health check server in background
    if os.getenv('RAILWAY_ENVIRONMENT'):
        health_thread = threading.Thread(target=start_health_server, daemon=True)
        health_thread.start()
        logger.info("✅ Health check server started for Railway")
    
    try:
        # Initialize database
        db_manager = DatabaseManager()
        await db_manager.init_database()
        logger.info("✅ Database initialized successfully")
        
        # Create application
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Add error handler
        app.add_error_handler(error_handler)
        
        # Add book conversation handler for admin
        add_book_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(admin_callback_handler, pattern="^admin_add_book$")],
            states={
                WAITING_BOOK_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_handle_book_code)],
                WAITING_BOOK_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_book_title)],
                WAITING_BOOK_FILE: [MessageHandler(filters.Document.ALL, handle_book_file)],
                WAITING_TEST_FILE: [MessageHandler(filters.Document.ALL, handle_test_file)],
            },
            fallbacks=[CommandHandler("cancel", cancel_conversation)],
        )
        
        # Add broadcast conversation handler for admin
        broadcast_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(admin_callback_handler, pattern="^admin_broadcast$")],
            states={
                WAITING_BROADCAST_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_broadcast_message)],
            },
            fallbacks=[CommandHandler("cancel", cancel_conversation)],
        )
        
        # Add handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("admin", admin_menu))
        app.add_handler(add_book_conv_handler)
        app.add_handler(broadcast_conv_handler)
        app.add_handler(CallbackQueryHandler(subscription_callback, pattern="^check_subscription$"))
        app.add_handler(CallbackQueryHandler(admin_callback_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_book_code))
        
        logger.info("✅ All handlers registered successfully")
        
        # Start the bot
        logger.info("🤖 Bot is now running and polling for updates...")
        logger.info(f"🔗 Bot username: @{os.getenv('BOT_USERNAME', 'Kitob_Bazasi_botAIPromptYordamchi_Bot')}")
        
        await app.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("🛑 Bot stopped by user")
    except Exception as e:
        logging.getLogger(__name__).error(f"❌ Fatal error: {e}")
        sys.exit(1)