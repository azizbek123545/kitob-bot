# 🚀 Railway Deployment Guide

## ✅ Deployment Status
Your Telegram bot is configured for Railway deployment with:
- ✅ Docker support (python:3.9)
- ✅ Health checks enabled
- ✅ Auto-restart on failure
- ✅ Environment variables configured
- ✅ Persistent storage for database and files

## 🔧 Environment Variables Required

Set these in Railway dashboard:

```bash
BOT_TOKEN=7717992642:AAG1NaiRIxJqq8VTAOL7I0UWnQRMnnd2ax8
BOT_USERNAME=Kitob_Bazasi_botAIPromptYordamchi_Bot
ADMIN_IDS=YOUR_ACTUAL_USER_ID,ANOTHER_ADMIN_ID
CHANNEL1_ID=-1002593361788
CHANNEL2_ID=-1002834612989
CHANNEL3_ID=-1002810716295
CHANNEL4_ID=-1002632397336
DATABASE_PATH=data/bot_database.db
BOOKS_DIR=data/books
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

## 🚀 Deploy to Railway

### Method 1: GitHub Integration (Recommended)
1. Push this code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables
6. Deploy!

### Method 2: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add environment variables
railway variables set BOT_TOKEN=your_token_here
railway variables set ADMIN_IDS=your_user_id

# Deploy
railway up
```

## 📊 Monitoring URLs

After deployment, Railway will provide:
- **App URL**: `https://your-app-name.railway.app`
- **Health Check**: `https://your-app-name.railway.app/health`
- **Logs**: Available in Railway dashboard

## 🔍 Health Check

The bot includes a health endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "...",
  "bot": "running"
}
```

## 📋 Post-Deployment Checklist

1. **Verify Environment Variables**
   - Check Railway dashboard → Variables
   - Ensure all required variables are set

2. **Check Bot Status**
   - Visit health endpoint: `https://your-app.railway.app/health`
   - Should return `{"status": "healthy"}`

3. **Test Bot**
   - Send `/start` to @Kitob_Bazasi_botAIPromptYordamchi_Bot
   - Verify subscription checking works
   - Test admin panel with `/admin`

4. **Monitor Logs**
   - Check Railway dashboard → Logs
   - Look for "🤖 Bot is now running and polling for updates..."

## 🔧 Troubleshooting

### Bot Not Starting
```bash
# Check logs in Railway dashboard
# Common issues:
# - Missing BOT_TOKEN
# - Invalid environment variables
# - Database permission issues
```

### Health Check Failing
```bash
# Check if port is correctly exposed
# Verify health_check.py is working
# Check Railway logs for errors
```

### Database Issues
```bash
# Railway provides persistent storage
# Database will be created automatically
# Check logs for SQLite errors
```

## 📈 Scaling

Railway automatically handles:
- ✅ Auto-restart on crashes
- ✅ Health monitoring
- ✅ Log aggregation
- ✅ Environment management
- ✅ HTTPS termination

## 💰 Cost

Railway offers:
- **Free Tier**: $5 credit monthly (sufficient for small bots)
- **Pro Plan**: $20/month for production apps
- **Usage-based**: Pay only for what you use

## 🔄 Updates

To update your bot:
1. Push changes to GitHub
2. Railway auto-deploys from main branch
3. Or use: `railway up` with CLI

## 📞 Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Bot Logs**: Railway dashboard → Logs tab