#!/bin/bash

# Production Deployment Script for Telegram Bot
# Usage: ./deploy.sh [start|stop|restart|logs|update]

set -e

BOT_NAME="telegram-bot-prod"
COMPOSE_FILE="docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Check if .env file exists
check_env() {
    if [ ! -f .env ]; then
        warning ".env file not found. Creating from template..."
        cp .env.production .env
        error "Please edit .env file with your actual bot token and admin IDs before running again."
        exit 1
    fi
}

# Start the bot
start_bot() {
    log "🚀 Starting Telegram Bot..."
    check_docker
    check_env
    
    # Create necessary directories
    mkdir -p data/books logs
    
    # Build and start containers
    docker-compose -f $COMPOSE_FILE up -d --build
    
    log "✅ Bot started successfully!"
    log "📊 Check status: docker-compose ps"
    log "📋 View logs: docker-compose logs -f telegram-bot"
}

# Stop the bot
stop_bot() {
    log "🛑 Stopping Telegram Bot..."
    docker-compose -f $COMPOSE_FILE down
    log "✅ Bot stopped successfully!"
}

# Restart the bot
restart_bot() {
    log "🔄 Restarting Telegram Bot..."
    stop_bot
    sleep 2
    start_bot
}

# Show logs
show_logs() {
    log "📋 Showing bot logs (Press Ctrl+C to exit)..."
    docker-compose -f $COMPOSE_FILE logs -f telegram-bot
}

# Update the bot
update_bot() {
    log "🔄 Updating Telegram Bot..."
    
    # Pull latest changes (if using git)
    if [ -d .git ]; then
        git pull
    fi
    
    # Rebuild and restart
    docker-compose -f $COMPOSE_FILE down
    docker-compose -f $COMPOSE_FILE up -d --build
    
    log "✅ Bot updated successfully!"
}

# Show status
show_status() {
    log "📊 Bot Status:"
    docker-compose -f $COMPOSE_FILE ps
    
    echo ""
    log "📈 Container Stats:"
    docker stats $BOT_NAME --no-stream
    
    echo ""
    log "💾 Disk Usage:"
    du -sh data/ logs/ 2>/dev/null || echo "No data/logs directories found"
}

# Backup data
backup_data() {
    log "💾 Creating backup..."
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p $BACKUP_DIR
    
    cp -r data/ $BACKUP_DIR/ 2>/dev/null || warning "No data directory to backup"
    cp -r logs/ $BACKUP_DIR/ 2>/dev/null || warning "No logs directory to backup"
    cp .env $BACKUP_DIR/ 2>/dev/null || warning "No .env file to backup"
    
    log "✅ Backup created at: $BACKUP_DIR"
}

# Main script logic
case "${1:-start}" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    logs)
        show_logs
        ;;
    update)
        update_bot
        ;;
    status)
        show_status
        ;;
    backup)
        backup_data
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs|update|status|backup}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the bot"
        echo "  stop    - Stop the bot"
        echo "  restart - Restart the bot"
        echo "  logs    - Show live logs"
        echo "  update  - Update and restart the bot"
        echo "  status  - Show bot status and stats"
        echo "  backup  - Create backup of data and logs"
        exit 1
        ;;
esac