from TikTokLive import TikTokLiveClient
from TikTokLive.events import (
    ConnectEvent, FollowEvent, GiftEvent, RoomUserSeqEvent, JoinEvent,
    LikeEvent, CommentEvent, ShareEvent, SubscribeEvent, LiveEndEvent,
    LivePauseEvent, LiveUnpauseEvent, RankTextEvent
)
import signal
import sys

client = TikTokLiveClient(unique_id="@zbventress")


@client.on(ConnectEvent)
async def on_connect(event):
    """Triggered when connected to the stream."""
    print(f"✅ Connected to TikTok Live as {client}")


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
        return  # Exit function to prevent further errors

    print(f"🎁 {sender_id} sent {gift_count}x {gift_name}")


# @client.on(FollowEvent)
# async def on_follow(event):
#     """Tracks when someone follows the streamer."""
#     print(f"📌 New Follower: {event.user.unique_id}")


# @client.on(GiftEvent)
# async def on_gift(event):
#     """Tracks when a user sends a gift."""
#     print(f"🎁 {event.user.unique_id} sent {event.gift.count}x {event.gift.name}")


# @client.on(RoomUserSeqEvent)
# async def on_viewers(event):
#     """Tracks the number of viewers in real-time."""
#     viewer_count = getattr(event, "total", None)
#     if viewer_count is not None:
#         print(f"👀 Current Viewers: {viewer_count}")
#     else:
#         print(f"⚠️ Viewer count not found in RoomUserSeqEvent: {event.__dict__}")



# @client.on(RoomUserSeqEvent)
# async def all_time_viewers(event):
#     """Tracks the number of viewers in real-time."""
#     viewer_count = getattr(event, "total_user", None)
#     if viewer_count is not None:
#         print(f"👀 Current Viewers: {viewer_count}")
#     else:
#         print(f"⚠️ Viewer count not found in RoomUserSeqEvent: {event.__dict__}")


# @client.on(JoinEvent)
# async def on_user_join(event):
#     """Tracks when a new user joins the stream."""
#     print(f"🚀 {event.user.unique_id} joined the live!")


# @client.on(LikeEvent)
# async def on_like(event):
#     """Tracks when a like is received."""
#     print(f"❤️ {event.user.unique_id} liked the stream!")


# @client.on(CommentEvent)
# async def on_comment(event):
#     """Tracks when a comment is sent in the chat."""
#     print(f"💬 {event.user.unique_id} commented: {event.comment}")


# @client.on(ShareEvent)
# async def on_share(event):
#     """Tracks when a user shares the stream."""
#     print(f"🔄 {event.user.unique_id} shared the stream!")


# @client.on(SubscribeEvent)
# async def on_subscribe(event):
#     """Tracks when a user subscribes to the creator."""
#     print(f"⭐ {event.user.unique_id} subscribed!")


# @client.on(RankTextEvent)
# async def on_rank_update(event):
#     """Tracks when a user ranks among top gifters."""
#     print(f"🏆 Rank Update: {event.rank_text}")




# def handle_exit(signum, frame):
#     """Handles script exit to clean up."""
#     print("\n⚠️ Exiting... Stopping client.")
#     client.stop()
#     sys.exit(0)


# # Capture termination signals to ensure cleanup
# signal.signal(signal.SIGINT, handle_exit)  # Ctrl+C
# signal.signal(signal.SIGTERM, handle_exit)  # Process termination


# Start listening
if __name__ == "__main__":
    client.run()