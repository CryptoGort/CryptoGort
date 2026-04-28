# CryptoGort X Bot

Automated X posts for [@11_western_llc](https://x.com/11_western_llc) — AI-generated market commentary, memes, and recaps posted three times daily.

| Time (ET) | Post type |
|-----------|-----------|
| 8:30 AM | Pre-market commentary + crypto news |
| 12:00 PM | Midday meme / humor post |
| 4:05 PM | End-of-day market recap |

---

## Quick start (local)

```bash
git clone https://github.com/CryptoGort/CryptoGort.git
cd CryptoGort
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
python test_post.py premarket --post   # test a live post
python main.py                          # start the scheduler
```

---

## Deploy to a cloud server (runs 24/7)

### 1. Spin up a server

The cheapest options that work well:

| Provider | Product | Cost |
|----------|---------|------|
| DigitalOcean | Droplet (Basic, 1 GB) | ~$6/mo |
| Vultr | Cloud Compute | ~$6/mo |
| AWS | EC2 t4g.nano | ~$3/mo |
| Hetzner | CX11 | ~€4/mo |

Pick **Ubuntu 24.04** as the OS.

---

### 2. Connect to your server

```bash
ssh root@YOUR_SERVER_IP
```

---

### 3. Install Docker

```bash
curl -fsSL https://get.docker.com | sh
apt install -y docker-compose-plugin
```

---

### 4. Upload the bot

On your **local machine**:
```bash
git clone https://github.com/CryptoGort/CryptoGort.git
cd CryptoGort
cp .env.example .env
# Edit .env and fill in all your API keys
scp -r . root@YOUR_SERVER_IP:/root/cryptogort
```

---

### 5. Start the bot

On the **server**:
```bash
cd /root/cryptogort
docker compose up -d
```

The bot starts immediately and restarts automatically if the server reboots.

---

### 6. Useful commands

```bash
# View live logs
docker compose logs -f

# Stop the bot
docker compose down

# Restart after changing .env or code
docker compose up -d --build

# Test a post manually without the scheduler
docker compose run --rm cryptogort-bot python test_post.py premarket --post
```

---

## Project structure

```
.
├── main.py          # Scheduler entry point (run this)
├── content.py       # Claude AI content generation
├── market_data.py   # Live prices (CoinGecko / yfinance) + RSS news
├── poster.py        # Tweepy — posts to X
├── test_post.py     # Manual test tool
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## Environment variables

Copy `.env.example` to `.env` and fill in:

```
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
ANTHROPIC_API_KEY=
```

Your X app needs **Read and Write** permissions (OAuth 1.0a).
