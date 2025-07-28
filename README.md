# Discord-auto-with-AI From Airdrop Sambil Rebahan

# sistem Requarements
- 4 core cpu
- 8GB ram
  
# Fitur
- auto chat with AI
- use reply in discord
- auto restart 
- random time spam
- Push level Dscord
- AI lebih manusiawi 

**buat screen**
```
sudo apt update && sudo apt install screen
```
```
screen -S AI
```
**install AI lokal**
```
curl -fsSL https://ollama.com/install.sh | sh
```
```
ollama serve
```
```
ollama pull gemma:2b
```
**Keluar screen AI**
- crtl a+d

**buat screen discord**
```
screen -S discord
```
**Install Script**
```
git clone https://github.com/kevinnft/discord-auto-chat-with-ai
cd discord-auto-chat-with-ai
```
Buat environtment
```
python3 -m venv dc
source dc/bin/activate
```
**install bahan**
```
pip3 install -r requirements.txt
```
```
pip uninstall discord discord.py discord.py-self -y
```
```
pip install git+https://github.com/dolfies/discord.py-self@71609f4f62649d18bdf14f0e286b7e62bc605390
```
**buka script**
```
nano bot.py
```
= isi TOKEN DC & channel ID target (tutorial token : https://www.youtube.com/watch?v=zyl6VGTJ4fY)

= ganti interval min dan max ( untuk waktu random dalam menit )

= klik ctrl + x -> klik y -> klik enter (untuk keluar)

**Mainkan script**
```
python3 bot.py
```
## Fungsi tambahan
masuk screen AI
```
screen -r AI
```
masuk screen discord
```
screen -r discord
```
## DISCLAIMER
Gunakan dengan bijak, semua risiko dan tanggung jawab ada di tangan pengguna.

## ☕ Donate for Coffee

**EVM Address**  
`0x7C8c8eF20a48901372775618330B294ab937C934`

**SOL Address**  
`GvvSje68JxGQ1suRguLcTq27TwNUzTomed3mEtt1s1KE`

---
© 2025 Airdrop Sambil Rebahan. All rights reserved.
