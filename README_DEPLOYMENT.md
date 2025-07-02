# 🚀 Production Deployment Guide

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd telegram-bot
   chmod +x deploy.sh
   ```

2. **Configure Environment**
   ```bash
   cp .env.production .env
   # Edit .env with your actual bot token and admin IDs
   nano .env
   ```

3. **Deploy**
   ```bash
   ./deploy.sh start
   ```

## 📋 Prerequisites

- Docker and Docker Compose installed
- Bot token from @BotFather
- Admin user IDs
- Channel IDs for subscription verification

## 🔧 Configuration

### Environment Variables (.env)
```bash
BOT_TOKEN=your_actual_bot_token_here
ADMIN_IDS=123456789,987654321
CHANNEL1_ID=-1002593361788
CHANNEL2_ID=-1002834612989
CHANNEL3_ID=-1002810716295
CHANNEL4_ID=-1002632397336
```

## 🚀 Deployment Commands

```bash
# Start the bot
./deploy.sh start

# Stop the bot
./deploy.sh stop

# Restart the bot
./deploy.sh restart

# View live logs
./deploy.sh logs

# Update and restart
./deploy.sh update

# Check status
./deploy.sh status

# Create backup
./deploy.sh backup
```

## 📊 Monitoring

### Check Bot Status
```bash
docker-compose ps
docker stats telegram-bot-prod
```

### View Logs
```bash
# Live logs
docker-compose logs -f telegram-bot

# Last 100 lines
docker-compose logs --tail=100 telegram-bot
```

### Health Check
The bot includes automatic health checks that verify database connectivity every 30 seconds.

## 🔄 Updates

### Manual Update
```bash
./deploy.sh update
```

### Automatic Updates (Watchtower)
Watchtower is included in docker-compose.yml and will automatically update the container when a new image is available.

## 💾 Data Persistence

- **Database**: `./data/bot_database.db`
- **Books**: `./data/books/`
- **Logs**: `./logs/`

All data is persisted using Docker volumes and will survive container restarts.

## 🔒 Security Features

- Non-root user in container
- Read-only environment file mounting
- Rate limiting and file size restrictions
- Comprehensive logging and monitoring

## 🆘 Troubleshooting

### Bot Not Starting
```bash
# Check logs
./deploy.sh logs

# Check container status
docker-compose ps

# Restart with fresh build
docker-compose down
docker-compose up -d --build
```

### Database Issues
```bash
# Check database file permissions
ls -la data/

# Recreate database
rm data/bot_database.db
./deploy.sh restart
```

### Memory Issues
```bash
# Check resource usage
docker stats telegram-bot-prod

# Restart container
./deploy.sh restart
```

## 📈 Production Tips

1. **Regular Backups**: Run `./deploy.sh backup` regularly
2. **Log Rotation**: Logs are automatically rotated (10MB max, 5 files)
3. **Monitoring**: Use `./deploy.sh status` to monitor resource usage
4. **Updates**: Keep the bot updated with `./deploy.sh update`

## 🌐 VPS Deployment

### DigitalOcean/Hetzner/AWS
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy bot
git clone <your-repo>
cd telegram-bot
cp .env.production .env
# Edit .env with your values
./deploy.sh start
```

### Systemd Service (Alternative)
```bash
# Create service file
sudo nano /etc/systemd/system/telegram-bot.service

# Enable and start
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

## 📞 Support

For issues or questions:
1. Check logs: `./deploy.sh logs`
2. Check status: `./deploy.sh status`
3. Restart: `./deploy.sh restart`
4. Create backup before troubleshooting: `./deploy.sh backup`