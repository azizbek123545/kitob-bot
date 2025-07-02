# Uzbek Telegram Bot with Admin Panel

A professional Telegram bot that manages subscription verification, book distribution, and includes a comprehensive admin panel - all in Uzbek language.

## 🚀 Features

### User Features
- ✅ Subscription verification for 4 Telegram channels
- 📚 Book code validation and PDF/DOC delivery
- 🇺🇿 Full Uzbek language interface
- ⚡ Async/await for optimal performance

### Admin Features
- 🔐 Admin-only access control
- ➕ Add new books with PDF and test files
- 📋 View and manage book library
- ❌ Delete books and files
- 📊 Comprehensive statistics
- 📤 Broadcast messages to all users
- 💾 SQLite database for data persistence

## 📋 Setup Instructions

### 1. Create a Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Save your bot token

### 2. Configure the Bot

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your bot token:
   ```
   BOT_TOKEN=your_actual_bot_token_here
   ADMIN_IDS=your_user_id,another_admin_id
   ```

3. Edit `config.py` and update:
   - `REQUIRED_CHANNELS`: Your channel URLs
   - `CHANNEL_IDS`: Your channel IDs (with -100 prefix)
   - `CHANNEL_NAMES`: Display names in Uzbek
   - `ADMIN_IDS`: Admin user IDs

### 3. Setup Channels

1. Create 4 Telegram channels
2. Add your bot as an admin to all channels
3. Get channel IDs and update `config.py`

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Bot

```bash
python main.py
```

## 🔧 Admin Commands

- `/admin` - Open admin panel
- `/cancel` - Cancel current operation

### Admin Panel Features

1. **➕ Add New Book**
   - Enter book code
   - Upload book PDF
   - Upload test file (PDF/DOC)

2. **📋 Book List**
   - View all books
   - See download statistics
   - Delete books with confirmation

3. **📊 Statistics**
   - Total users
   - Active users (with downloads)
   - Total downloads
   - Most popular books

4. **📤 Broadcast**
   - Send messages to all users
   - Track delivery statistics

## 📊 Database Schema

The bot uses SQLite with the following tables:

- `books` - Book information and file paths
- `users` - User data and activity
- `downloads` - Download history
- `broadcasts` - Broadcast message history

## 🔄 Bot Flow

### User Flow
1. User sends `/start`
2. Bot shows 4 channel subscription buttons
3. User clicks "✅ Obuna bo'ldim"
4. Bot verifies subscriptions
5. If verified, asks for book code
6. User sends book code
7. Bot sends book PDF and test file
8. Bot sends promotional message

### Admin Flow
1. Admin sends `/admin`
2. Admin panel with options appears
3. Admin can manage books, view stats, broadcast

## 📁 File Structure

```
/bot/
├── main.py                 # Main bot application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── database/
│   └── db_manager.py      # Database operations
├── handlers/
│   ├── start.py           # /start command handler
│   ├── books.py           # Book code handler
│   └── admin.py           # Admin panel handlers
├── utils/
│   └── check_subs.py      # Subscription checking
├── data/
│   ├── books/             # PDF files storage
│   └── bot_database.db    # SQLite database
└── README.md              # This file
```

## 🚀 Deployment Options

### Option 1: VPS/Cloud Server
1. Upload files to your server
2. Install Python 3.8+
3. Install dependencies: `pip install -r requirements.txt`
4. Run with screen/tmux: `screen -S bot python main.py`

### Option 2: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Option 3: Heroku
1. Create `Procfile`: `worker: python main.py`
2. Deploy to Heroku
3. Scale worker dyno: `heroku ps:scale worker=1`

## ⚠️ Important Notes

- Make sure your bot is added as admin to all required channels
- Bot must have permission to check channel membership
- All user-facing messages are in Uzbek language
- Admin IDs must be configured in `config.py`
- Maximum file size is 50MB per file
- Database is automatically created on first run

## 🔧 Troubleshooting

- **Subscription checking fails**: Ensure bot is admin in channels
- **Files don't send**: Check file permissions in `data/books/`
- **Bot doesn't respond**: Verify bot token in `.env`
- **Admin panel not accessible**: Check your user ID in `ADMIN_IDS`
- **Database errors**: Ensure write permissions in `data/` directory

## 📞 Support

For support and questions, contact the bot administrator.