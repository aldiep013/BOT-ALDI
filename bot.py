from telethon import TelegramClient, events
import sqlite3
import re

# Inisialisasi bot dengan Telethon
api_id = '24576633'
api_hash = '29931cf620fad738ee7f69442c98e2ee'
bot_token = '7839023375:AAFeNnN--zEUYo7MygKGe_gHYOln-zhHQuo'

client = TelegramClient('referral_bot', api_id, api_hash).start(bot_token=bot_token)

# Fungsi untuk mendapatkan poin pengguna berdasarkan user_id
def get_points(user_id):
    conn = sqlite3.connect("referral_points.db")
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM referrals WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

# Fungsi untuk menambahkan poin
def add_points(user_id, points=1):
    conn = sqlite3.connect("referral_points.db")
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM referrals WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        new_points = result[0] + points
        cursor.execute("UPDATE referrals SET points = ? WHERE user_id = ?", (new_points, user_id))
    else:
        cursor.execute("INSERT INTO referrals (user_id, points) VALUES (?, ?)", (user_id, points))
    
    conn.commit()
    conn.close()

# Handler untuk perintah /start
@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    # Mendapatkan user_id yang merujuk
    match = re.search(r"start=(\d+)", event.raw_text)
    
    if match:
        ref_user_id = int(match.group(1))
        add_points(ref_user_id)  # Menambahkan poin ke user yang merujuk
        await event.respond(f"Referral Anda berhasil! {ref_user_id} mendapatkan 1 poin.")

    else:
        await event.respond("Selamat datang! Anda dapat merujuk teman dengan link berikut.")
        
# Handler untuk perintah /cek
@client.on(events.NewMessage(pattern='/cek'))
async def cek_handler(event):
    user_id = event.sender_id  # Mendapatkan user_id pengirim perintah
    
    # Mendapatkan jumlah referral (poin) pengguna
    points = get_points(user_id)
    
    # Menampilkan jumlah referral (poin)
    if points > 0:
        await event.respond(f"Anda memiliki {points} poin referral.")
    else:
        await event.respond("Anda belum memiliki poin referral.")
        
# Jalankan bot
client.run_until_disconnected()