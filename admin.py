"""
Admin handlers for the Telegram bot
"""
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import TelegramError

from config import ADMIN_IDS, BOOKS_DIR, MAX_FILE_SIZE
from database.db_manager import DatabaseManager

# Conversation states
WAITING_BOOK_CODE, WAITING_BOOK_TITLE, WAITING_BOOK_FILE, WAITING_TEST_FILE, WAITING_BROADCAST_MESSAGE = range(5)

db_manager = DatabaseManager()

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin menu"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Sizda admin huquqlari yo'q.")
        return
    
    keyboard = [
        [InlineKeyboardButton("➕ Kitob qo'shish", callback_data="admin_add_book")],
        [InlineKeyboardButton("📋 Kitoblar ro'yxati", callback_data="admin_book_list")],
        [InlineKeyboardButton("📊 Statistika", callback_data="admin_stats")],
        [InlineKeyboardButton("📤 Xabar yuborish", callback_data="admin_broadcast")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔧 Admin Panel\n\nQuyidagi amallardan birini tanlang:",
        reply_markup=reply_markup
    )

async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin callback queries"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ Sizda admin huquqlari yo'q.")
        return
    
    if query.data == "admin_add_book":
        await query.edit_message_text("📝 Yangi kitob kodi kiriting (masalan: ABC123):")
        return WAITING_BOOK_CODE
    
    elif query.data == "admin_book_list":
        await show_book_list(query)
    
    elif query.data == "admin_stats":
        await show_stats(query)
    
    elif query.data == "admin_broadcast":
        await query.edit_message_text("📝 Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:")
        return WAITING_BROADCAST_MESSAGE
    
    elif query.data.startswith("delete_book_"):
        book_code = query.data.replace("delete_book_", "")
        await delete_book_confirm(query, book_code)
    
    elif query.data.startswith("confirm_delete_"):
        book_code = query.data.replace("confirm_delete_", "")
        await delete_book(query, book_code)
    
    elif query.data == "cancel_delete":
        await query.edit_message_text("❌ O'chirish bekor qilindi.")

async def show_book_list(query):
    """Show list of all books"""
    books = await db_manager.get_all_books()
    
    if not books:
        await query.edit_message_text("📚 Hozircha kitoblar yo'q.")
        return
    
    text = "📚 Barcha kitoblar:\n\n"
    keyboard = []
    
    for book in books:
        text += f"📖 {book['code']} - {book['title']}\n"
        text += f"   📥 Yuklab olingan: {book['download_count']} marta\n\n"
        
        keyboard.append([InlineKeyboardButton(
            f"🗑 {book['code']} o'chirish", 
            callback_data=f"delete_book_{book['code']}"
        )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_stats(query):
    """Show bot statistics"""
    stats = await db_manager.get_stats()
    
    text = "📊 Bot statistikasi:\n\n"
    text += f"👥 Jami foydalanuvchilar: {stats['total_users']}\n"
    text += f"📚 Faol foydalanuvchilar: {stats['active_users']}\n"
    text += f"📥 Jami yuklab olingan: {stats['total_downloads']}\n\n"
    
    if stats['popular_books']:
        text += "🔥 Eng mashhur kitoblar:\n"
        for i, (code, title, count) in enumerate(stats['popular_books'], 1):
            text += f"{i}. {code} - {title} ({count} marta)\n"
    
    await query.edit_message_text(text)

async def delete_book_confirm(query, book_code):
    """Confirm book deletion"""
    keyboard = [
        [InlineKeyboardButton("✅ Ha, o'chirish", callback_data=f"confirm_delete_{book_code}")],
        [InlineKeyboardButton("❌ Yo'q, bekor qilish", callback_data="cancel_delete")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"⚠️ {book_code} kitobini o'chirishni tasdiqlaysizmi?\n\n"
        "Bu amal qaytarib bo'lmaydi!",
        reply_markup=reply_markup
    )

async def delete_book(query, book_code):
    """Delete book from database and files"""
    book = await db_manager.get_book(book_code)
    if not book:
        await query.edit_message_text("❌ Kitob topilmadi.")
        return
    
    # Delete files
    try:
        if os.path.exists(book['book_file_path']):
            os.remove(book['book_file_path'])
        if os.path.exists(book['test_file_path']):
            os.remove(book['test_file_path'])
    except Exception as e:
        print(f"Error deleting files: {e}")
    
    # Delete from database
    success = await db_manager.delete_book(book_code)
    
    if success:
        await query.edit_message_text(f"✅ {book_code} kitob muvaffaqiyatli o'chirildi.")
    else:
        await query.edit_message_text("❌ Kitobni o'chirishda xatolik yuz berdi.")

# Conversation handlers for adding books
async def handle_book_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle book code input"""
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    
    book_code = update.message.text.strip().upper()
    
    # Check if book already exists
    existing_book = await db_manager.get_book(book_code)
    if existing_book:
        await update.message.reply_text(f"❌ {book_code} kodi allaqachon mavjud.")
        return ConversationHandler.END
    
    context.user_data['new_book_code'] = book_code
    await update.message.reply_text(f"📝 {book_code} uchun kitob nomini kiriting:")
    return WAITING_BOOK_TITLE

async def handle_book_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle book title input"""
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    
    title = update.message.text.strip()
    context.user_data['new_book_title'] = title
    
    await update.message.reply_text("📎 Kitob faylini yuklang (PDF format):")
    return WAITING_BOOK_FILE

async def handle_book_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle book file upload"""
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    
    if not update.message.document:
        await update.message.reply_text("❌ Iltimos, fayl yuklang.")
        return WAITING_BOOK_FILE
    
    document = update.message.document
    
    # Check file size
    if document.file_size > MAX_FILE_SIZE:
        await update.message.reply_text("❌ Fayl hajmi juda katta (maksimal 50MB).")
        return WAITING_BOOK_FILE
    
    # Check file extension
    if not document.file_name.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Faqat PDF formatdagi fayllar qabul qilinadi.")
        return WAITING_BOOK_FILE
    
    # Download file
    book_code = context.user_data['new_book_code']
    os.makedirs(BOOKS_DIR, exist_ok=True)
    
    book_file_path = os.path.join(BOOKS_DIR, f"{book_code}.pdf")
    
    try:
        file = await document.get_file()
        await file.download_to_drive(book_file_path)
        context.user_data['new_book_file_path'] = book_file_path
        
        await update.message.reply_text("✅ Kitob fayli yuklandi.\n\n📎 Endi test faylini yuklang (PDF yoki DOC):")
        return WAITING_TEST_FILE
    
    except Exception as e:
        await update.message.reply_text("❌ Faylni yuklashda xatolik yuz berdi.")
        return WAITING_BOOK_FILE

async def handle_test_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle test file upload"""
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    
    if not update.message.document:
        await update.message.reply_text("❌ Iltimos, fayl yuklang.")
        return WAITING_TEST_FILE
    
    document = update.message.document
    
    # Check file size
    if document.file_size > MAX_FILE_SIZE:
        await update.message.reply_text("❌ Fayl hajmi juda katta (maksimal 50MB).")
        return WAITING_TEST_FILE
    
    # Check file extension
    allowed_extensions = ['.pdf', '.doc', '.docx']
    if not any(document.file_name.lower().endswith(ext) for ext in allowed_extensions):
        await update.message.reply_text("❌ Faqat PDF, DOC yoki DOCX formatdagi fayllar qabul qilinadi.")
        return WAITING_TEST_FILE
    
    # Download file
    book_code = context.user_data['new_book_code']
    file_extension = os.path.splitext(document.file_name)[1]
    test_file_path = os.path.join(BOOKS_DIR, f"{book_code}_test{file_extension}")
    
    try:
        file = await document.get_file()
        await file.download_to_drive(test_file_path)
        
        # Save book to database
        success = await db_manager.add_book(
            book_code,
            context.user_data['new_book_title'],
            context.user_data['new_book_file_path'],
            test_file_path
        )
        
        if success:
            await update.message.reply_text(
                f"✅ {book_code} kitob muvaffaqiyatli qo'shildi!\n\n"
                f"📖 Nom: {context.user_data['new_book_title']}\n"
                f"📁 Kod: {book_code}"
            )
        else:
            await update.message.reply_text("❌ Kitobni saqlashda xatolik yuz berdi.")
        
        # Clear user data
        context.user_data.clear()
        return ConversationHandler.END
    
    except Exception as e:
        await update.message.reply_text("❌ Faylni yuklashda xatolik yuz berdi.")
        return WAITING_TEST_FILE

async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle broadcast message"""
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    
    message = update.message.text
    
    await update.message.reply_text("📤 Xabar yuborilmoqda...")
    
    # Get all users
    users = await db_manager.get_all_users()
    sent_count = 0
    failed_count = 0
    
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            sent_count += 1
            await asyncio.sleep(0.1)  # Rate limiting
        except TelegramError:
            failed_count += 1
    
    # Record broadcast
    await db_manager.record_broadcast(message, sent_count)
    
    await update.message.reply_text(
        f"✅ Xabar yuborish yakunlandi!\n\n"
        f"📤 Yuborildi: {sent_count}\n"
        f"❌ Yuborilmadi: {failed_count}"
    )
    
    return ConversationHandler.END

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel current conversation"""
    await update.message.reply_text("❌ Amal bekor qilindi.")
    context.user_data.clear()
    return ConversationHandler.END