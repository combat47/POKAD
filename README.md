# 🦜 POKAD – Offline AI assistant that speaks Persian (Farsi). Private, runs on your CPU, no cloud. Chat, search, translate, remember conversations. Llama‑2‑7B int8.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/combat47/POKAD?style=social)](https://github.com/combat47/POKAD)
[![GitHub watchers](https://img.shields.io/github/watchers/combat47/style=social&label=Watch&maxAge=2592000)](https://GitHub.com/combat47/POKAD/watchers/)

> **P**ersian **O**ffline **K**nowledge **A**I & **D**igital assistant  
> *Your smart, sassy, and totally offline Persian buddy.*  
> *No internet? No problem. 🤙*

<img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="800">


---

## 🌟 What's POKAD?

POKAD is a **fully offline** AI assistant that speaks Persian (Farsi) like a native.  
It runs on your own machine – no cloud, no data leakage, no subscription fees.  
Think of it as a **private, snarky, and surprisingly helpful** companion that can:

- 💬 Chat in **natural Persian** (with a bit of personality)
- 🔍 Search the web for you (if you let it)
- 🌐 Translate English ↔ Persian on the fly
- 🧠 **Remember** your name and recent conversation
- 📝 Keep chat history in a local database
- 🖥️ Run on your CPU (yes, even a laptop can handle it with int8 magic)
- 🔌 *(Coming soon)* Connect to **IoT devices** – tell POKAD to turn on the lights!

> 🎯 **Mission:** Make powerful AI accessible, private, and fun for Persian speakers worldwide.

---

## 🚀 Features (the fun parts)

- ✅ **100% offline** – Your secrets stay on your machine. No "Oops, our servers are down".
- ✅ **Persian first** – No more weird Google Translate artifacts. POKAD thinks in Farsi.
- ✅ **Smart fallback** – Can search the web when it doesn't know something (you control it).
- ✅ **Memory with a twist** – Remembers who you are and the last 5 messages. Like a goldfish but smarter.
- ✅ **PyQt GUI** – A real desktop app, not just a terminal.
- ✅ **Model flexibility** – Uses Llama-2-7B (int8) – strong enough to be clever, small enough to not melt your laptop.
- ✅ **Extensible** – Swap the translator, add new search backends, or hook up your smart home.

> 🧙 **Coming in v0.2:**  
> - Voice input/output  
> - IoT integration (control real devices)  
> - Mobile-friendly API  
> - Plugins system

---

## 📦 How to install (it's easier than making tea)

### Prerequisites
- **Python 3.9+** ([download](https://www.python.org/downloads/))
- **4–6 GB of free RAM** (for the LLM model)
- **Git** (to clone the repo)
- A bit of patience – the model is chonky (~4GB).

### 1. Clone the magic

```bash
git clone https://github.com/combat47/POKAD.git
cd POKAD
```
### 2. Create a virtual environment (because we're civilized)
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
# or
venv\Scripts\activate         # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Download the AI model (the brain of POKAD)
We don't store the model in this repo (GitHub would cry). Run the download script:

```bash
python models/download_models.py
```
> ⏳ This will fetch ~4GB from Hugging Face. Go grab a coffee. ☕

### 5. Run POKAD!
```bash
python src/chatbotApp.py
```
A beautiful window appears. Say hello. Try "سلام" or "تو کی هستی؟".
POKAD will answer in Persian. Be amazed. 😲

### 🎮 How to use (it's chat, but smarter)
Normal chat: Type anything in Persian (or English). POKAD will reply in Persian.

Ask for web info: Include a question like "آب و هوای تهران چطوره؟" – if it needs help, it'll search.

Tell it your name: Say "اسم من علی است". It'll remember.

Check memory: Ask "اسم من چی بود؟" – it won't forget (until you close the app).

Exit: Type "خروج" or close the window.

> 💡 Pro tip: POKAD's personality is a bit cheeky. It might roast you if you ask stupid questions. You've been warned.

### 🧠 How does it work? (the boring-but-impressive tech)
| Component	| Technology	| Why? |
|---------|---------|---------|
| Language model	| Llama-2-7B (int8 via CTranslate2)	| Strong, open, runs on CPU |
| Translation	| Google Translate API (fallback)	| Easy for now – will become offline later |
| Web search	| googlesearch-python + BeautifulSoup	| Gets live info |
|GUI	| PyQt6	| Native desktop feel |
| Memory	| SQLite	| Lightweight, no setup |
| Architecture	| Modular (src/core, gui, etc.)	| Easy to hack |

Soon we'll replace Google Translate with a local MT5 model (already in models/mt5-* – but not fully integrated yet). Contributions welcome!

### 🤝 Contributing (join the circus!)
We love new contributors – even if you've never done open source before.
Check out our CONTRIBUTING.md for the boring legal stuff.
Here's the fun version:

- 🐛 Found a bug? Open an Issue.

- 💡 Have an idea? Start a Discussion.

- 🔧 Can code? Pick a good first issue and send a Pull Request.

- 📝 Not a coder? Improve the docs, translate this README into Persian, or draw a better logo.

All contributors get:

- Eternal gratitude 😌

- Your name in the Hall of Fame (below)

- A warm fuzzy feeling inside

### 🌍 Hall of Fame (people who made POKAD awesome)
- Amirhossein Jahazi – Creator, maintainer, idea machine

- Your name here? – You!

### 📜 License
POKAD is open source under the [Apache 2.0 License.](https://github.com/combat47/POKAD/blob/main/LICENSE)
You can use, modify, and even sell it – just keep the original copyright notice and don't sue us if it calls you names.

### 💰 Making money with POKAD (yes, it's possible)
- We're not greedy, but servers aren't free. Here's how we (and you) can earn:

- GitHub Sponsors – Support the project monthly. We'll put your logo on the fridge (README).

- Paid support – Companies can pay for custom integrations (IoT, enterprise features).

- Open Core – The core stays free; advanced features (multi‑user, cloud sync) will be paid.

- Bounties – We'll tag some issues with a cash reward (via Algora or similar).

If you want to consult or build a business around POKAD – go for it! We're friendly.

### ❓ FAQ (Frequently Absurd Questions)
Q: Why "POKAD"?
A: It stands for "Persian Offline Knowledge AI & Digital assistant". Also, it sounds like a cute pokémon. Catch it.

Q: Does it work on Windows / Mac / Linux?
A: Yes! Python is our magic carpet.

Q: Can I use it with a Raspberry Pi?
A: Not yet – the 7B model is too heavy. But we plan a tiny version for Pi later.

Q: Why does it take 5 seconds to reply?
A: It's thinking. Or judging you. Probably both.

Q: I don't speak Persian. Can I still use it?
A: You can, but it'll reply in Persian. Great way to practice! 😉

### 📬 Contact & Social
GitHub Issues – Best for bugs & features

Discord – Join our server (soon)

X – @amir__aj1 (follow for memes & updates)

⭐ Star this repo if you want POKAD to become the Jarvis of the Persian world.
🍰 Bake me a cookie if you actually read this far.
Now go chat with your new AI friend! 🤖💬

Made with 💻 and ☕ in Iran.
