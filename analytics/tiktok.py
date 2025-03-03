from TikTokLive import TikTokLiveClient
from TikTokLive.events import (
    ConnectEvent, FollowEvent, GiftEvent, RoomUserSeqEvent, 
    CommentEvent
)
from Analytics import Analytics
import signal
import sys
import time

user = "zbventress"
client = TikTokLiveClient(unique_id="@" + user)

analytics = Analytics(platform="TikTok")

session_id = analytics.start_stream_session(user)

start_time = time.time()
viewer_last_logged = 0  # Track the last logged minute


@client.on(ConnectEvent)
async def on_connect(event):
    print(f"Connected to TikTok Live as {client.unique_id}")


@client.on(FollowEvent)
async def on_follow(event):
    """Count total followers gained in session"""
    analytics.increment_followers(session_id)
    print(f"📌 New Follower: {event.user.unique_id}")

@client.on(GiftEvent)
async def on_gift(event):
    """Aggregate gifts received and handle missing attributes."""

    # Extract sender info safely
    sender_id = getattr(event.user, "unique_id", "Unknown")

    # Extract gift details safely
    gift = getattr(event, "gift", None)
    if gift:
        gift_name = getattr(gift, "name", f"Gift-{event.gift_id}")  # Use gift_id if name is missing
        gift_count = (
            getattr(event, "combo_count", None) or 
            getattr(event, "repeat_count", None) or 
            getattr(event, "group_count", None) or 
            getattr(event, "fan_ticket_count", None) or 
            getattr(event, "room_fan_ticket_count", None) or 
            1  # Default to 1 if all counts are missing
        )
    else:
        print(f"⚠️ Error: 'gift' object missing in event: {event.__dict__}")
        return 

    # Store aggregated gift data
    analytics.aggregate_gift(session_id, gift_name, gift_count, sender_id)
    print(f"🎁 {sender_id} sent {gift_count}x {gift_name}")
    
@client.on(RoomUserSeqEvent)
async def on_viewers(event):
    """Save viewer count every minute"""
    global viewer_last_logged
    viewer_count = getattr(event, "total", None)
    
    if viewer_count is not None:
        current_minute = int(time.time() - start_time) // 60  # Minute bucket
        if current_minute > viewer_last_logged:
            analytics.save_viewer_count(session_id, current_minute, viewer_count)
            viewer_last_logged = current_minute  # Update last logged minute
            print(f"👀 Viewers logged for minute {current_minute}: {viewer_count}")


@client.on(CommentEvent)
async def on_comment(event):
    """Store total comments and track top commenter"""
    analytics.save_comment(session_id, event.user.unique_id)
    print(f"💬 {event.user.unique_id} commented: {event.comment}")


def handle_exit(signum, frame):
    """Save accumulated stats before exiting"""
    print("\nSaving aggregated data before exit...")
    analytics.flush_summary_to_db()
    analytics.close()
    sys.exit(0)


# Capture termination signals to ensure data is saved before exit
signal.signal(signal.SIGINT, handle_exit)  
signal.signal(signal.SIGTERM, handle_exit)  

if __name__ == "__main__":
    client.run()