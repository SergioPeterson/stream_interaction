import asyncio
import datetime
import time
from TikTokLive import TikTokLiveClient
from TikTokLive.events import (
    ConnectEvent, FollowEvent, GiftEvent, RoomUserSeqEvent, 
    CommentEvent, DisconnectEvent, LiveEndEvent
)
from Analytics import Analytics
import signal
import sys
from rich.console import Console
from rich.table import Table
from rich.live import Live

gift_values = {
    "Dalgona Candy": 1, "Brat": 1, "Ice cube": 1, "2025": 1, "Heart Me": 1,
    "Fest burst": 1, "Candy Cane": 1, "Flame Heart": 1, "Music play": 1, "Basketball": 1,
    "GG": 1, "Lightning Bolt": 1, "Ice cream Cone": 1, "Rose": 1, "TikTok": 1,
    "It’s corn": 1, "Heart Puff": 1, "Slay": 1, "GOAT": 1, "Chili": 1,
    "Paddington in Peru": 1, "Take More Photos": 1, "Team Bracelet": 2, "W": 5,
    "Fluffy penguin": 5, "Tofu the cat": 5, "Ladybug": 5, "Espresso": 5, "Finger heart": 5,
    "American football": 5, "Cheer You Up": 9, "Gold boxing glove": 10, "Festive potato": 10,
    "Little ghost": 10, "Christmas wreath": 10, "Friendship Necklace": 10, "Rosa": 10,
    "Dolphin": 10, "Tiny Dino": 10, "Hi Bear": 10, "Perfume": 20, "Let ‘Em Cook": 20,
    "Scented candle": 20, "S Flowers": 20, "Doughnut": 30, "Sign language love": 49,
    "Butterfly": 88, "Fist bump": 90, "Sending strength": 90, "Family": 90, "Chart topper": 90,
    "Cap": 99, "Level-up Sparks": 99, "Bubble Gum": 99, "Paper crane": 99, "Fest crown": 99,
    "Love Painting": 99, "Little crown": 99, "Hat and Mustache": 99, "Flowers": 100,
    "Game Controller": 100, "Hand Heart": 100, "Super GG": 100, "Confetti": 100,
    "Marvelous Confetti": 100, "Stroke hair": 100, "Massage for You": 199, "Potato in Paris": 199,
    "Hanging Lights": 199, "Wooly Hat": 199, "Headphone": 199, "Reindeer": 199, "Festive bear": 199,
    "Cheering Crab": 199, "Hearts": 199, "Sunglasses": 199, "Night star": 199, "Twinkling Star": 199,
    "Eye see you": 199, "Santa’s mailbox": 199, "Dancing hands": 199, "Mistletoe": 199,
    "Message for you": 199, "Stinging bee": 199, "Coffee magic": 199, "Sending positivity": 199,
    "Love you": 199, "Garland Headpiece": 199, "Bunny Ears": 200, "Gold Medal": 200,
    "Balloons": 200, "2025 Glasses": 225, "Pinch Face": 249, "Starlight Compass": 299,
    "Butterfly for You": 299, "Pawfect": 299, "Paddington Hat": 299, "Elephant trunk": 299,
    "TikTok Crown": 299, "Elf’s hat": 299, "Fruit friends": 299, "Play for You": 299,
    "Rock Star": 299, "Superpower": 299, "Boxing Gloves": 299, "Corgi": 299, "Dancing flower": 299,
    "Naughty Chicken": 299, "Falling For You": 299, "Full moon": 299, "Lover’s Glasses": 299,
    "Rosie the Rose Bean": 399, "Jollie the Joy Bean": 399, "Good Afternoon": 399, "Good Night": 399,
    "Tom’s Hug": 399, "Relaxed goose": 399, "Rocky the Rock Bean": 399, "Sage the Smart Bean": 399,
    "Pumpkin head": 399, "Forever Rosa": 399, "Gaming headset": 399, "Good Morning": 399,
    "Good Evening": 399, "You Are Loved": 399, "Let butterfly dances": 399, "Beating heart": 449,
    "Coral": 499, "Panda Hug": 499, "Im Just a Hamster": 499, "Hands Up": 499, "Dragon Crown": 500,
    "XXXL Flowers": 500, "You’re amazing": 500, "Money gun": 500, "Gem gun": 500, "Manifesting": 500,
    "Lion’s mane": 500, "DJ glasses": 500, "Star map polaris": 500, "VR Goggles": 500,
    "Diamond Microphone": 500, "Happy Weekend": 599, "Swan": 699, "Train": 899, "It’s a Match": 899,
    "Superstar": 900, "Travel with You": 999, "Lucky the Airdrop Box": 999, "Trending Figure": 999,
    "Enchanted Guitar": 999, "Magic Cat": 1000, "Drums": 1000, "Galaxy": 1000, "Blooming ribbons": 1000,
    "Glowing jellyfish": 1000, "Watermelon Love": 1000, "Dinosaur": 1000, "Gerry the giraffe": 1000,
    "Shiny air balloon": 1000, "Fireworks": 1088, "Diamond tree": 1088, "Umbrella of Love": 1200,
    "Epic GG": 1200, "Fountain": 1200, "Spooky cat": 1200, "Paddington Snow": 1200,
    "Moonlight flower": 1400, "Streamer’s Setup": 1400, "Level Ship": 1500, "Future Encounter": 1500,
    "Love explosion": 1500, "Under control": 1500, "Greeting card": 1500, "Card to You": 1500,
    "Chasing the dream": 1500, "Shooting Stars": 1580, "Here We Go": 1799, "Mystery firework": 1999,
    "Cooper flies home": 1999, "Spooktacular": 1999, "Christmas carousel": 2000, "Baby dragon": 2000,
    "Red telephone box": 2100, "Whale Diving": 2150, "Animal band": 2500, "Cupid": 2888,
    "Motorcycle": 2988, "Fest Celebration": 2999, "Rhythmic bear": 2999, "Magic Blast": 2999,
    "Dancing bears": 3000, "Meteor Shower": 3000, "Car drifting": 3000, "Gaming keyboard": 4000,
    "Your Concert": 4500, "Leon the kitten": 4888, "Signature Jet": 4888, "Private jet": 4888,
    "Fiery Dragon": 4888, "Silver sports car": 5000, "Ellie the Elephant": 5000, "Wanda the Witch": 5000,
    "Flying jets": 5000, "Diamond Gun": 5000, "DJ Alien": 5000, "Wolf": 5500, "Santa’s express": 5999,
    "Hands up high": 6000, "Future city": 6000, "Work Hard Play Harder": 6000, "Lili the Leopard": 6599,
    "Happy Party": 6999, "Sports car": 7000, "Love from Dubai": 7499, "Leon and Lili": 9699,
    "Santa’s here!": 9999, "Interstellar": 10000, "Sunset Speedway": 10000, "Octopus": 10000,
    "Luxury Yacht": 10000, "Bob’s Town": 15000, "Party On&On": 15000, "Rosa Nebula": 15000
}

# Prompt user for TikTok username at runtime
user = input("Enter the TikTok username (without @): ").strip()
client = TikTokLiveClient(unique_id="@" + user)

analytics = Analytics(platform="TikTok")
session_id = analytics.start_stream_session(user)

# Tracking statistics
start_time = time.time()
viewer_last_logged = 0
reconnect_attempts = 0
max_views = 0
new_followers = 0
total_gift_points = 0
current_views = 0

console = Console()
lock = asyncio.Lock()  # Ensure thread-safe updates

def get_runtime():
    """Returns the stream runtime in hh:mm:ss format."""
    elapsed_time = int(time.time() - start_time)
    return str(datetime.timedelta(seconds=elapsed_time))

def get_formatted_time():
    """Returns current time in MM/DD/YYYY HH:MM format."""
    return datetime.datetime.now().strftime("%m/%d/%Y %H:%M")

def generate_table():
    """Generate a rich table with live stream statistics."""
    table = Table(title="📊 Live Stream Statistics", show_lines=True)
    
    table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="center", style="bold yellow")
    
    table.add_row("🎥 Streamer", user)
    table.add_row("⏳ Runtime", get_runtime())  # New runtime row
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
    handle_exit(None, None)

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

    analytics.aggregate_gift(session_id, gift_name, gift_count, sender_id, gift_value)
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
    """Save accumulated stats before exiting."""
    print("\n💾 Saving aggregated data before exit...")

    analytics.flush_summary_to_db()  # Now handles end_time & run_time inside analytics.py
    analytics.close()  # Close DB connection

    try:
        loop = asyncio.get_running_loop()
        loop.call_soon(loop.stop)  # Gracefully stop the event loop
    except RuntimeError:
        print("No running event loop, exiting directly.")
        sys.exit(0)  # Exit the program if no event loop is running

async def main():
    """Main async function to run the live table and TikTok client together."""
    asyncio.create_task(update_table())  # Start live table updates
    await client.connect()  # Start the TikTok client connection

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Start the event loop
    except RuntimeError:  # If loop is already running
        loop = asyncio.get_running_loop()
        loop.create_task(main())  # Create a new task