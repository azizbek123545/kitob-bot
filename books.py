"""
Handler for book code processing and file sending
"""

import os
from telegram import Update
from telegram.ext import ContextTypes

from config import PROMO_CHANNEL
from database.db_manager import DatabaseManager

db_manager = DatabaseManager()

async def handle_book_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle book code input from user"""
    
    # Check if we're expecting a book code
    if not context.user_data.get('expecting_book_code'):
        return
    
    book_code = update.message.text.strip().upper()
    
    # Get book from database
    book = await db_manager.get_book(book_code)
    
    if book and os.path.exists(book['book_file_path']) and os.path.exists(book['test_file_path']):
        try:
            # Send the main book PDF
            with open(book['book_file_path'], 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"{book['code']}.pdf",
                    caption=f"📕 {book['title']}"
                )
            
            # Send the test file
            with open(book['test_file_path'], 'rb') as test_file:
                file_extension = os.path.splitext(book['test_file_path'])[1]
                filename = f"{book['code']}_test{file_extension}"
                
                await update.message.reply_document(
                    document=test_file,
                    filename=filename,
                    caption=f"📝 {book['title']} - Test savollari"
                )
            
            # Record download
            await db_manager.record_download(update.effective_user.id, book_code)
            
            # Send final promotional message
            final_message = (
                "📌 Ushbu kitobning batafsil tahlili va muhokamasi uchun "
                f"bizning kanalimizga tashrif buyuring: {PROMO_CHANNEL}"
            )
            
            await update.message.reply_text(final_message)
            
            # Reset user state
            context.user_data['expecting_book_code'] = False
            
        except Exception as e:
            await update.message.reply_text(
                "❌ Fayllarni yuborishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
            )
    else:
        # Invalid book code
        await update.message.reply_text(
            "❌ Noto'g'ri kod kiritildi. Iltimos, kodni tekshirib qayta urinib ko'ring.\n\n"
            "💡 Maslahat: Kod harflari katta bo'lishi kerak (masalan: ABC123)"
        )