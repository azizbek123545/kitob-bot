# 🚀 Production Setup Guide for @Kitob_Bazasi_botAIPromptYordamchi_Bot

## ✅ Bot Information
- **Bot Username**: @Kitob_Bazasi_botAIPromptYordamchi_Bot
- **Bot Token**: Configured ✅
- **Channels**: 4 channels configured ✅

## 🔧 Pre-Deployment Checklist

### 1. Update Admin IDs
Edit `.env` file and replace with your actual Telegram user IDs:
```bash
ADMIN_IDS=YOUR_ACTUAL_USER_ID,ANOTHER_ADMIN_ID
```

**How to get your User ID:**
1. Message @userinfobot on Telegram
2. It will reply with your user ID
3. Replace `123456789` in the `.env` file

### 2. Verify Bot Permissions
Make sure your bot is added as **ADMIN** to all 4 channels:
- ✅ https://t.me/Kitob_Bazasi_1
- ✅ https://t.me/ITBlogUz1
- ✅ https://t.me/ieltsgram_test
- ✅ https://t.me/deepreadClub

**Steps:**
1. Go to each channel
2. Click channel name → Administrators
3. Add @Kitob_Bazasi_botAIPromptYordamchi_Bot as admin
4. Give permissions: "Delete messages" and "Ban users"

### 3. Test Channel IDs
The following channel IDs are configured:
```
Kitob Bazasi: -1002593361788
IT Blog Uz: -1002834612989
IELTS Gram Test: -1002810716295
Deep Read Club: -1002632397336
```

## 🚀 Quick Deployment

### Option 1: Docker (Recommended)
```bash
# 1. Make deploy script executable
chmod +x deploy.sh

# 2. Start the bot
./deploy.sh start

# 3. Check logs
./deploy.sh logs
```

### Option 2: Direct Python
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the bot
python main.py
```

## 📱 Testing the Bot

### 1. Start Command
Send `/start` to @Kitob_Bazasi_botAIPromptYordamchi_Bot

Expected response:
```
Assalomu alaykum, [Your Name]! 👋

📚 Kitob olish uchun quyidagi 4 ta kanalga obuna bo'ling:

[4 channel buttons]

Obuna bo'lgach, pastdagi tugmani bosing.
```

### 2. Admin Panel
Send `/admin` to the bot (only works if your user ID is in ADMIN_IDS)

Expected response:
```
🔧 Admin Panel

Quyidagi amallardan birini tanlang:
[Admin buttons]
```

### 3. Book Code Test
1. Subscribe to all 4 channels
2. Click "✅ Obuna bo'ldim"
3. Send book code: `ABC123`
4. Bot should send the test PDF files

## 🔍 Troubleshooting

### Bot doesn't respond to /start
- Check if bot token is correct
- Verify bot is running: `./deploy.sh status`
- Check logs: `./deploy.sh logs`

### Subscription check fails
- Ensure bot is admin in all channels
- Verify channel IDs are correct
- Check bot permissions in channels

### Admin panel not accessible
- Verify your user ID is in ADMIN_IDS
- Get your user ID from @userinfobot
- Update .env file and restart: `./deploy.sh restart`

### Files not sending
- Check if files exist in `data/books/`
- Verify file permissions
- Check file size (max 50MB)

## 📊 Monitoring Commands

```bash
# Check bot status
./deploy.sh status

# View live logs
./deploy.sh logs

# Restart bot
./deploy.sh restart

# Create backup
./deploy.sh backup
```

## 🌐 VPS Deployment

### DigitalOcean/Hetzner/AWS
```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 2. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. Clone and deploy
git clone <your-repo>
cd telegram-bot
chmod +x deploy.sh
./deploy.sh start
```

## ✅ Production Checklist

- [ ] Bot token configured
- [ ] Admin user IDs updated
- [ ] Bot added as admin to all 4 channels
- [ ] Test files uploaded to `data/books/`
- [ ] Bot responds to `/start`
- [ ] Subscription verification works
- [ ] Admin panel accessible
- [ ] Book codes work
- [ ] Files are sent correctly

## 📞 Support

If you encounter issues:
1. Check logs: `./deploy.sh logs`
2. Verify configuration in `.env`
3. Test bot permissions in channels
4. Restart bot: `./deploy.sh restart`

Your bot is ready for production! 🎉