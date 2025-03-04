import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import (
    ConnectEvent, FollowEvent, GiftEvent, RoomUserSeqEvent, 
    CommentEvent, DisconnectEvent, LiveEndEvent
)
from Analytics import Analytics
import signal
import sys
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live

# Gift values mapping for point calculations
gift_values = {
    "rose": 1, "panda": 5, "perfume": 20, "i love you": 49,
    "confetti": 100, "sunglasses": 199, "money rain": 500,
    "disco ball": 1000, "mermaid": 2988, "airplane": 6000,
    "planet": 15000, "diamond flight": 18000, "lion": 29999,
    "tiktok universe": 44999
}

user = input("Enter the TikTok username (without @): ").strip()
client = TikTokLiveClient(unique_id="@" + user)
analytics = Analytics(platform="TikTok")
session_id = analytics.start_stream_session(user)
start_time = time.time()
viewer_last_logged = 0
reconnect_attempts = 0
max_views = 0
new_followers = 0
total_gift_points = 0
current_views = 0
console = Console()
lock = asyncio.Lock() 

def generate_table():
    """Generate a rich table with live stream statistics."""
    table = Table(title="📊 Live Stream Statistics", show_lines=True)
    
    table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="center", style="bold yellow")
    
    table.add_row("🎥 Streamer", user)
    table.add_row("👀 Current Views", str(current_views))
    table.add_row("🔥 Max Views", str(max_views))
    table.add_row("📌 New Followers", str(new_followers))
    table.add_row("🎁 Gift Points", str(total_gift_points))

    return table

async def update_table():
    """Continuously updates the table every second."""
    with Live(generate_table(), console=console, refresh_per_second=1) as live:
        while True:
            await asyncio.sleep(1)  # Update every second
            async with lock:  # Ensure thread-safe updates
                live.update(generate_table())  # Refresh table

async def reconnect():
    """Handles automatic reconnection on network loss, with rate limiting awareness."""
    global reconnect_attempts
    while reconnect_attempts < 3:
        try:
            print(f"Attempting to reconnect ({reconnect_attempts + 1}/3)...")
            await client.connect()
            print("Successfully reconnected to TikTok Live.")
            reconnect_attempts = 0  
            return
        except Exception as e:
            reconnect_attempts += 1
            wait_time = min(2 ** reconnect_attempts, 60)  
            print(f"Reconnection failed: {e}. Retrying in {wait_time} seconds...")
            await asyncio.sleep(wait_time)

    print("Maximum reconnection attempts reached. Exiting.")
    handle_exit(None, None)

@client.on(ConnectEvent)
async def on_connect(event):
    print(f"✅ Connected to TikTok Live as {client.unique_id}")

@client.on(DisconnectEvent)
async def on_disconnect(event):
    """Handles disconnection by attempting to reconnect."""
    print("⚠️ Disconnected from TikTok Live! Trying to reconnect...")
    asyncio.create_task(reconnect())

@client.on(LiveEndEvent)
async def on_live_end(event):
    """Handles stream ending by gracefully shutting down."""
    print("TikTok Live has ended. Saving data and exiting.")
    handle_exit(None, None)  # Call the fixed exit function
@client.on(FollowEvent)
async def on_follow(event):
    """Count total followers gained in session"""
    global new_followers
    async with lock:
        new_followers += 1
    analytics.increment_followers(session_id)

@client.on(GiftEvent)
async def on_gift(event):
    """Aggregate gifts received and handle missing attributes."""
    global total_gift_points
    sender_id = getattr(event.user, "unique_id", "Unknown")
    gift = getattr(event, "gift", None)
    
    if gift:
        gift_name = getattr(gift, "name", f"Gift-{event.gift_id}")
        gift_count = (
            getattr(event, "combo_count", None) or 
            getattr(event, "repeat_count", None) or 
            getattr(event, "group_count", None) or 
            getattr(event, "fan_ticket_count", None) or 
            getattr(event, "room_fan_ticket_count", None) or 
            1
        )
        gift_value = gift_values.get(gift_name.lower(), 0) * gift_count
        async with lock:
            total_gift_points += gift_value
    else:
        print(f"⚠️ Error: 'gift' object missing in event: {event.__dict__}")
        return 

    analytics.aggregate_gift(session_id, gift_name, gift_count, sender_id)
    print(f"{sender_id} sent {gift_count}x {gift_name} ({gift_value} points)")

@client.on(RoomUserSeqEvent)
async def on_viewers(event):
    """Save viewer count every minute, handle missing data during disconnect."""
    global viewer_last_logged, current_views, max_views
    viewer_count = getattr(event, "total", None) or 0
    async with lock:
        current_views = viewer_count
        max_views = max(max_views, viewer_count)

    current_minute = int(time.time() - start_time) // 60  
    if current_minute > viewer_last_logged:
        analytics.save_viewer_count(session_id, current_minute, viewer_count or "NULL")  
        viewer_last_logged = current_minute

@client.on(CommentEvent)
async def on_comment(event):
    """Store total comments and track top commenter"""
    analytics.save_comment(session_id, event.user.unique_id)

def handle_exit(signum, frame):
    """Save accumulated stats before exiting gracefully."""
    print("\n💾 Saving aggregated data before exit...")
    analytics.flush_summary_to_db()
    analytics.close()
    
    loop = asyncio.get_event_loop()
    loop.stop()  # Stop the event loop instead of sys.exit(0)

# Capture termination signals to ensure data is saved before exit
signal.signal(signal.SIGINT, handle_exit)  
signal.signal(signal.SIGTERM, handle_exit)  

async def main():
    """Main async function to run the live table and TikTok client together."""
    asyncio.create_task(update_table())  # Start live table updates
    await client.connect()  # Start the TikTok client connection

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Start event loop properly
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.create_task(main())  # If already running, just create the task
        loop.run_forever()