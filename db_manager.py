"""
Database manager for the Telegram bot
"""
import aiosqlite
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from config import DATABASE_PATH

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        
    async def init_database(self):
        """Initialize database tables"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        async with aiosqlite.connect(self.db_path) as db:
            # Books table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    book_file_path TEXT NOT NULL,
                    test_file_path TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    download_count INTEGER DEFAULT 0
                )
            """)
            
            # Users table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_downloads INTEGER DEFAULT 0
                )
            """)
            
            # Downloads table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    book_code TEXT,
                    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (book_code) REFERENCES books (code)
                )
            """)
            
            # Broadcast messages table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS broadcasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sent_count INTEGER DEFAULT 0
                )
            """)
            
            await db.commit()
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Add or update user in database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, last_activity)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, datetime.now()))
            await db.commit()
    
    async def add_book(self, code: str, title: str, book_file_path: str, test_file_path: str) -> bool:
        """Add a new book to database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO books (code, title, book_file_path, test_file_path)
                    VALUES (?, ?, ?, ?)
                """, (code.upper(), title, book_file_path, test_file_path))
                await db.commit()
                return True
        except aiosqlite.IntegrityError:
            return False
    
    async def get_book(self, code: str) -> Optional[Dict]:
        """Get book by code"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT code, title, book_file_path, test_file_path, download_count
                FROM books WHERE code = ?
            """, (code.upper(),)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {
                        'code': row[0],
                        'title': row[1],
                        'book_file_path': row[2],
                        'test_file_path': row[3],
                        'download_count': row[4]
                    }
                return None
    
    async def get_all_books(self) -> List[Dict]:
        """Get all books"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT code, title, download_count, created_at
                FROM books ORDER BY created_at DESC
            """) as cursor:
                rows = await cursor.fetchall()
                return [
                    {
                        'code': row[0],
                        'title': row[1],
                        'download_count': row[2],
                        'created_at': row[3]
                    }
                    for row in rows
                ]
    
    async def delete_book(self, code: str) -> bool:
        """Delete book by code"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("DELETE FROM books WHERE code = ?", (code.upper(),))
            await db.commit()
            return cursor.rowcount > 0
    
    async def record_download(self, user_id: int, book_code: str):
        """Record a book download"""
        async with aiosqlite.connect(self.db_path) as db:
            # Record download
            await db.execute("""
                INSERT INTO downloads (user_id, book_code)
                VALUES (?, ?)
            """, (user_id, book_code.upper()))
            
            # Update book download count
            await db.execute("""
                UPDATE books SET download_count = download_count + 1
                WHERE code = ?
            """, (book_code.upper(),))
            
            # Update user total downloads
            await db.execute("""
                UPDATE users SET total_downloads = total_downloads + 1, last_activity = ?
                WHERE user_id = ?
            """, (datetime.now(), user_id))
            
            await db.commit()
    
    async def get_stats(self) -> Dict:
        """Get bot statistics"""
        async with aiosqlite.connect(self.db_path) as db:
            # Total users
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                total_users = (await cursor.fetchone())[0]
            
            # Users with downloads
            async with db.execute("SELECT COUNT(*) FROM users WHERE total_downloads > 0") as cursor:
                active_users = (await cursor.fetchone())[0]
            
            # Total downloads
            async with db.execute("SELECT COUNT(*) FROM downloads") as cursor:
                total_downloads = (await cursor.fetchone())[0]
            
            # Most popular books
            async with db.execute("""
                SELECT b.code, b.title, b.download_count
                FROM books b
                ORDER BY b.download_count DESC
                LIMIT 5
            """) as cursor:
                popular_books = await cursor.fetchall()
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'total_downloads': total_downloads,
                'popular_books': popular_books
            }
    
    async def get_all_users(self) -> List[int]:
        """Get all user IDs for broadcasting"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT user_id FROM users") as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
    
    async def record_broadcast(self, message: str, sent_count: int):
        """Record broadcast message"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO broadcasts (message, sent_count)
                VALUES (?, ?)
            """, (message, sent_count))
            await db.commit()