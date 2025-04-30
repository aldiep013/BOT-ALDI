from telethon import TelegramClient, events
from db import add_user, count_users
import os

# Ganti dengan API milikmu
api_id = 24576633  # Ganti dengan API ID dari my.telegram.org
api_hash = '29931cf620fad738ee7f69442c98e2ee'  # Ganti dengan API Hash
bot_token = '7839023375:AAFeNnN--zEUYo7MygKGe_gHYOln-zhHQuo'

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user = event.sender
    add_user(user)
    await event.respond(f"Halo {user.first_name}, kamu sudah terdaftar!")

@bot.on(events.NewMessage(pattern='/cek'))
async def cek(event):
    total = count_users()
    await event.respond(f"Ada {total} user yang sudah start bot ini.")

print("Bot berjalan...")
bot.run_until_disconnected()