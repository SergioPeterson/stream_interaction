from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, FollowEvent, GiftEvent
import pygame
import random

# ------------------ GIFT COIN VALUES ------------------
gift_values = {
    "rose": 1,
    "panda": 5,
    "perfume": 20,
    "i love you": 49,
    "confetti": 100,
    "sunglasses": 199,
    "money rain": 500,
    "disco ball": 1000,
    "mermaid": 2988,
    "airplane": 6000,
    "planet": 15000,
    "diamond flight": 18000,
    "lion": 29999,
    "tiktok universe": 44999
}

# ------------------ PYGAME SETUP ------------------
pygame.init()
screen_width, screen_height = 800, 100  # Overlay size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gift Progress Bar")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialize progress
current_coins = 0
goal = 1000  # Reset at 1,000 coins

# ------------------ SOUND SETUP ------------------
pygame.mixer.init()
follow_sound = "sounds/follow_sound.wav"
confetti_sound = "sounds/confetti_sound.wav"

# Create the TikTok client (Remove '@' from username)
client = TikTokLiveClient(unique_id="@sergiopeter20165")

# ------------------ EVENT HANDLERS ------------------

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"✅ Connected to @{event.unique_id} (Room ID: {client.room_id})")

@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    if random.randint(1, 10) == 1:  # 10% chance to play sound
        print(f"🎉 {event.user.nickname} followed! Playing sound...")
        pygame.mixer.music.load(follow_sound)
        pygame.mixer.music.play()

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    global current_coins

    gift_name = event.gift.info.name.lower()
    gift_coins = gift_values.get(gift_name, 0)  # Get coin value from dictionary

    if gift_coins > 0:
        current_coins += gift_coins
        print(f"🎁 {event.user.nickname} sent {gift_name} ({gift_coins} coins)! Total: {current_coins}/{goal}")

        # Play confetti sound (1/2 chance)
        if gift_name == "confetti" and random.randint(1, 2) == 1:
            pygame.mixer.music.load(confetti_sound)
            pygame.mixer.music.play()

        # Reset if goal reached
        if current_coins >= goal:
            print("🎉 Goal reached! Resetting progress...")
            current_coins = 0

# ------------------ PYGAME RENDER LOOP ------------------

def draw_progress_bar():
    """Draw the progress bar based on current coin value."""
    screen.fill(WHITE)  # Clear screen

    # Calculate bar width
    bar_width = (current_coins / goal) * screen_width if current_coins < goal else screen_width

    # Draw bar
    pygame.draw.rect(screen, GREEN, (0, 30, bar_width, 40))
    
    # Display text
    font = pygame.font.Font(None, 36)
    text = font.render(f"Gifts Progress: {current_coins}/{goal} coins", True, BLACK)
    screen.blit(text, (10, 5))

    pygame.display.flip()

# ------------------ MAIN LOOP ------------------

if __name__ == '__main__':
    pygame_thread_running = True

    while pygame_thread_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame_thread_running = False

        draw_progress_bar()
        pygame.time.delay(100)  # Update every 100ms

    pygame.quit()
    client.run()
