import os
import time
import asyncio
import requests
import random
import sys
from datetime import datetime, timedelta
from discord.ext import tasks, commands
from discord import Message

print(r'''
                      .^!!^.
                  .:~7?7!7??7~:.
               :^!77!~:..^^~7?J?!^.
           .^!7??!^..  ..^^^^^~JJJJ7~:.
           7?????: ...^!7?!^^^~JJJJJJJ?.
           7?????:...^???J7^^^~JJJJJJJJ.
           7?????:...^??7?7^^^~JJJJJJJ?.
           7?????:...^~:.^~^^^~JJJJJJJ?.
           7?????:.. .:^!7!~^^~7?JJJJJ?.
           7?????:.:~JGP5YJJ?7!^^~7?JJ?.
           7?7?JY??JJ5BBBBG5YJJ?7!~7JJ?.
           7Y5GBBYJJJ5BBBBBBBGP5Y5PGP5J.
           ^?PBBBP555PBBBBBBBBBBBB#BPJ~
              :!YGB#BBBBBBBBBBBBGY7^
                 .~?5BBBBBBBBPJ~.
                     :!YGGY7:
                        ..

 🚀 Support Me: 0x7C8c8eF20a48901372775618330B294ab937C934
''')

# === Konfigurasi ===
DISCORD_USER_TOKEN = "Your_Token_Here"
CHANNEL_ID = 1177659428229619753
INTERVAL_MIN = 1  # menit
INTERVAL_MAX = 3
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma:2b"

# === State ===
next_reply_time = datetime.now()
pending_message = None
has_printed_wait = False

# Inisialisasi selfbot
client = commands.Bot(command_prefix="!", self_bot=True)

# === Fungsi AI Lokal ===
async def get_ai_reply(prompt):
    try:
        crypto_prompt = (
    "Reply in casual, natural English like you're just chatting with a friend. "
    "Keep it super short — one sentence only. "
    "Don’t repeat words like 'yeah', 'just', or 'like' more than once. "
    "Don’t copy or rephrase the original message. "
    "Avoid sounding like an AI or trying to be too smart. "
    "No greetings, no emojis, and no unnecessary questions. "
    "Mention Plume Network only if it fits casually. "
    "Keep it real, simple, and effortless — like a human reply that flows.\n\n"
    f"Message: {prompt}\n"
    "Reply:"
)
        response = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": OLLAMA_MODEL,
            "prompt": crypto_prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except Exception as e:
        print(f"[❌] Error Ollama: {e}")
        return "have a nice day"

# === Saat Bot Aktif ===
@client.event
async def on_ready():
    print(f"[✅] Login sebagai {client.user}")
    reply_loop.start()
    auto_restart.start()

# === Ketika Ada Pesan Masuk ===
@client.event
async def on_message(message: Message):
    global pending_message
    if message.channel.id != CHANNEL_ID:
        return
    if message.author.id == client.user.id:
        return
    pending_message = message

# === Loop untuk Balasan Otomatis ===
@tasks.loop(seconds=10)
async def reply_loop():
    global pending_message, next_reply_time, has_printed_wait

    if not pending_message:
        has_printed_wait = False
        return

    now = datetime.now()
    if now < next_reply_time:
        if not has_printed_wait:
            remaining = int((next_reply_time - now).total_seconds() // 60)
            print(f"[⏳] Menunggu {remaining} menit sebelum balas...")
            has_printed_wait = True
        return

    has_printed_wait = False
    reply = await get_ai_reply(pending_message.content)

    # Filter respons buruk
    banned_phrases = [
        "Sure, here's a random sentence",
        "Here's a sentence",
        "As an AI language model",
        "In conclusion"
    ]
    if any(phrase.lower() in reply.lower() for phrase in banned_phrases) or reply.count("\n") >= 2:
        print("[⚠️] Balasan AI tidak cocok, dilewati.")
        pending_message = None
        next_reply_time = datetime.now() + timedelta(minutes=1)
        return

    # Kirim balasan sebagai REPLY tanpa mention
    try:
        content = reply
        await pending_message.reply(content)
        print(f"[✅] Balas ke {pending_message.author.name}: {reply}")

        wait_minutes = random.randint(INTERVAL_MIN, INTERVAL_MAX)
        next_reply_time = datetime.now() + timedelta(minutes=wait_minutes)
        pending_message = None
    except Exception as e:
        print(f"[❌] Gagal kirim balasan: {e}")

# === Restart Otomatis ===
@tasks.loop(hours=2)
async def auto_restart():
    print(f"[♻️] Restart otomatis pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    python = sys.executable
    os.execv(python, [python] + sys.argv)

@auto_restart.before_loop
async def before_auto_restart():
    await client.wait_until_ready()
    print(f"[⏳] Auto-restart aktif setiap 2 jam")
    await asyncio.sleep(2 * 60 * 60)

# === Jalankan Bot ===
client.run(DISCORD_USER_TOKEN)
