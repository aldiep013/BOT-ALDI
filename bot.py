from telethon import TelegramClient, events
from database import create_table, insert_nft, get_all_nfts

# Konfigurasi API Telethon
api_id = 24576633         # Ganti dengan API ID kamu
api_hash = '29931cf620fad738ee7f69442c98e2ee' # Ganti dengan API Hash kamu
bot_token = '7839023375:AAFeNnN--zEUYo7MygKGe_gHYOln-zhHQuo'    # Ganti dengan token botmu

client = TelegramClient('nftbot', api_id, api_hash).start(bot_token=bot_token)

# Pastikan database sudah siap
create_table()

@client.on(events.NewMessage(pattern='/upload'))
async def handler(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        
        # Misal formatnya reply berupa teks kaya:
        # Name: Ginger Cookies
        # Model: Amaretto 0.6%
        # Latar: Pacific Cyan 2%
        # Simbol: Mistletoe 1.5%
        # Owner: @bumbleebbee
        # Price: Rp95.000
        # Image: https://i.imgur.com/WDl8XBo.jpeg
        # Link: https://t.me/nft/GingerCookie-6213

        lines = reply.text.split('\n')
        data = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip().lower()] = value.strip()

        insert_nft(
            data.get('name', ''),
            data.get('model', ''),
            data.get('latar', ''),
            data.get('simbol', ''),
            data.get('owner', ''),
            data.get('price', ''),
            data.get('image', ''),
            data.get('link', '')
        )

        await event.reply("✅ NFT berhasil disimpan!")

@client.on(events.NewMessage(pattern='/generate'))
async def generate(event):
    nfts = get_all_nfts()

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>NFT GIFT LUCKY JASTIP</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white">
    <div id="productGrid" class="grid grid-cols-1 gap-4 p-4">
    """

    for nft in nfts:
        _, name, model, latar, simbol, owner, price, image_url, nft_link = nft
        html_template += f"""
        <div class="bg-gray-800 rounded-lg p-4 product-card" data-name="{name}" data-model="{model}" data-latar="{latar}" data-simbol="{simbol}">
            <a href="{nft_link}" target="_blank">
                <img src="{image_url}" alt="{name}" class="rounded-lg mb-2 mx-auto cursor-pointer" width="250" height="250">
            </a>
            <div class="font-bold text-md mb-1">
                <a href="{nft_link}" class="text-blue-400 hover:underline">{name}</a>
            </div>
            <div class="format-box text-sm">
                <p><strong>Pemilik:</strong> <a href="https://t.me/{owner.replace('@','')}" class="text-blue-400">{owner}</a></p>
                <p><strong>Model :</strong> {model}</p>
                <p><strong>Latar :</strong> {latar}</p>
                <p><strong>Simbol :</strong> {simbol}</p>
                <p><strong>Harga :</strong> {price}</p>
            </div>
        </div>
        """

    html_template += """
    </div>
</body>
</html>
"""

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

    await event.reply("✅ Website berhasil diupdate! Cek di folder web/index.html")

client.start()
client.run_until_disconnected()
