"""
Handler for /start command and subscription checking
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from config import REQUIRED_CHANNELS, CHANNEL_IDS, CHANNEL_NAMES
from utils.check_subs import check_user_subscriptions
from database.db_manager import DatabaseManager

db_manager = DatabaseManager()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Add user to database
    await db_manager.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    # Create inline keyboard with channel links
    keyboard = []
    
    # Add channel buttons
    for channel_key, channel_url in REQUIRED_CHANNELS.items():
        channel_name = CHANNEL_NAMES[channel_key]
        keyboard.append([InlineKeyboardButton(f"📢 {channel_name}", url=channel_url)])
    
    # Add subscription confirmation button
    keyboard.append([InlineKeyboardButton("✅ Obuna bo'ldim", callback_data="check_subscription")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"Assalomu alaykum, {user.first_name}! 👋\n\n"
        "📚 Kitob olish uchun quyidagi 4 ta kanalga obuna bo'ling:\n\n"
        "Obuna bo'lgach, pastdagi tugmani bosing."
    )
    
    await update.message.reply_text(message, reply_markup=reply_markup)

async def subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle subscription check callback"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "check_subscription":
        # Check if user is subscribed to all channels
        is_subscribed = await check_user_subscriptions(context.bot, user_id, list(CHANNEL_IDS.values()))
        
        if is_subscribed:
            # User is subscribed to all channels
            await query.edit_message_text(
                "✅ Rahmat! Barcha kanallarga obuna bo'ldingiz.\n\n"
                "📝 Endi kitob kodini yuboring (masalan: ABC123):"
            )
            # Store user state to expect book code
            context.user_data['expecting_book_code'] = True
        else:
            # User is not subscribed to all channels
            keyboard = [[InlineKeyboardButton("🔁 Qayta tekshirish", callback_data="check_subscription")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "❌ Siz hali barcha kanallarga obuna bo'lmagansiz.\n\n"
                "Iltimos, barcha kanallarga obuna bo'lib, qaytadan tekshiring.",
                reply_markup=reply_markup
            )