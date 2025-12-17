<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/fyaz05/Resources@main/FileToLink/Thunder.jpg" alt="NETFLIXIAN X Logo" width="200">
  <h1 align="center">🔥 NETFLIXIAN X</h1>
</p>

<p align="center">
  <b>High-Performance Telegram File-to-Link Bot for Ultra-Fast Direct Links & Streaming</b>
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.13%2B-blue?style=for-the-badge&logo=python">
  </a>
  <a href="https://github.com/LastPerson07">
    <img src="https://img.shields.io/badge/Pyrofork-Stable-red?style=for-the-badge">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge">
  </a>
  <a href="https://github.com/LastPerson07">
    <img src="https://img.shields.io/badge/Telegram-Updates-blue?style=for-the-badge&logo=telegram">
  </a>
</p>

<hr>
📑 Table of Contents
About The Project

How It Works

Features

Configuration

Usage & Commands

Advanced Features

Deployment Guide

Support & Community

License

Acknowledgments

🚀 About The Project
NETFLIXIAN X is a next-generation Telegram File Streaming Bot designed to convert Telegram files into high-speed HTTP(S) direct links.
It enables instant streaming and fast downloads without forcing users to download files directly from Telegram.

💡 Why NETFLIXIAN X?
Built for speed, stability, and scalability

Designed for large communities & media channels

Fully self-hosted & watermark-free

Optimized for production environments

⚙️ How It Works
User sends a file to the bot or channel

Bot securely fetches the file from Telegram servers

A direct streaming/download link is generated

Users can:

▶️ Stream instantly

⬇️ Download at maximum speed

🔗 Share links externally

No Telegram app download required for end users.

✨ Features
🚀 High-Speed File Streaming

🔗 Direct Download Links

📁 Supports Large Files

📡 Adaptive Streaming

🛡 Rate Limiting & Abuse Protection

🔐 Token-Based Secure Links

🌐 Reverse Proxy Support

📊 Network Speed Test Endpoint

⚡ Low Latency & Optimized Buffering

❌ No Watermark / No Forced Branding

🛠 Configuration
Essential Configuration
Set these environment variables:

env
Copy code
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=your_telegram_user_id
Optional Configuration
env
Copy code
PORT=8080
BIND_ADDRESS=0.0.0.0
BASE_URL=https://your-domain.com
ENABLE_TOKEN_SYSTEM=True
RATE_LIMIT=10
🤖 Usage & Commands
Basic Usage
Send any file to the bot

Get an instant streaming/download link

Share anywhere

Commands Reference
Command Description
/start Start the bot
/help Show help menu
/ping Check bot status
/stats Server & usage stats
/speedtest Network speed test
/links Active generated links

⚡ Advanced Features
🔐 Token System
Protects links from unauthorized access using expiring tokens.

🔗 URL Shortening
Integrate your own shortener or custom domain.

🚦 Rate Limiting
Prevents spam & abuse automatically.

📈 Network Speed Testing
Built-in speed test for diagnostics and optimization.

🚢 Deployment Guide
Prerequisites
Python 3.13+

Telegram API credentials

VPS / Cloud platform

Installation
bash
Copy code
git clone https://github.com/LastPerson07
cd netflixian-x
pip install -r requirements.txt
python main.py
☁️ Quick Deploy
Deploy to Koyeb
One-click scalable deployment

Ideal for production bots

Deploy to Render
Free & paid plans supported

Easy environment setup

Deploy to Railway
Fast CI/CD deployment

Automatic scaling

🔁 Reverse Proxy Setup
Supports:

Nginx

Cloudflare

Caddy

Ensures:

HTTPS

Custom domains

Better caching

🤝 Support & Community
📢 Updates Channel: https://t.me/Netflixian_Movie

🧑‍💻 Maintainer: Dhanpal Sharma

💬 Feature requests & issues via GitHub

📜 License
This project is licensed under the Apache License 2.0
You are free to use, modify, and distribute it.

❤️ Acknowledgments
Pyrofork Community

Telegram Developers

Open-Source Contributors

Everyone supporting NETFLIXIAN X

🔥 NETFLIXIAN X — Stream Smarter. Download Faster.
