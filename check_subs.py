"""
Utility functions for checking user subscriptions
"""

from telegram import Bot
from telegram.error import BadRequest, Forbidden

async def check_user_subscriptions(bot: Bot, user_id: int, channel_ids: list) -> bool:
    """
    Check if user is subscribed to all required channels
    
    Args:
        bot: Telegram bot instance
        user_id: User's Telegram ID
        channel_ids: List of channel IDs
    
    Returns:
        bool: True if subscribed to all channels, False otherwise
    """
    
    for channel_id in channel_ids:
        try:
            # Get chat member info
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            
            # Check if user is a member (not left or kicked)
            if member.status in ['left', 'kicked']:
                return False
                
        except (BadRequest, Forbidden):
            # If we can't check (channel doesn't exist, bot not admin, etc.)
            # Return False to be safe
            return False
        except Exception:
            # Any other error, return False
            return False
    
    # If we get here, user is subscribed to all channels
    return True

async def check_single_subscription(bot: Bot, user_id: int, channel_id: str) -> bool:
    """
    Check if user is subscribed to a single channel
    
    Args:
        bot: Telegram bot instance
        user_id: User's Telegram ID
        channel_id: Channel ID
    
    Returns:
        bool: True if subscribed, False otherwise
    """
    
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status not in ['left', 'kicked']
    except:
        return False