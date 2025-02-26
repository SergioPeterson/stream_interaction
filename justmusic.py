from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, FollowEvent, GiftEvent
import pygame
import random

# Initialize pygame for sound playback
pygame.mixer.init()

# Load sounds
follow_sound = "sounds/follow_sound.wav"
confetti_sound = "sounds/confetti_sound.wav"

# Create the client (Remove "@" from username)
client = TikTokLiveClient(unique_id="sergiopeter20165")


# 🎥 When connected to TikTok Live
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"✅ Connected to @{event.unique_id} (Room ID: {client.room_id})")


# 🟢 When someone follows (1/10 chance to play sound)
@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    if random.randint(1, 10) == 1:  # 10% chance
        print(f"🎉 {event.user.nickname} followed! Playing sound...")
        pygame.mixer.music.load(follow_sound)
        pygame.mixer.music.play()


@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    if event.gift.info.name.lower() == "rose":  # Check if the gift is "Confetti"
        if random.randint(1, 2) == 1:  # 50% chance
            print(f"🎊 {event.user.nickname} sent Confetti! Playing sound...")
            pygame.mixer.music.load(confetti_sound)
            pygame.mixer.music.play()


if __name__ == '__main__':
    client.run()
