# PulseCut AI — Automated Viral Shorts & Video Studio

<p align="center">
  <img src="web/brand/logo.svg" alt="PulseCut AI" width="320"/>
</p>

<p align="center">
  <b>Turn long videos and live streams into captioned vertical clips, ready to post.</b><br>
  Free, open-source, and self-hosted. Run it on your computer with your own AI key and zero cloud limits.
</p>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-0.162-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="https://playwright.dev"><img src="https://img.shields.io/badge/Playwright-Automated_Bot-45ba4b?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright"></a>
  <a href="https://ffmpeg.org"><img src="https://img.shields.io/badge/FFmpeg-Hardware_Accelerated-007808?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="FFmpeg"></a>
  <a href="https://github.com/MdNayem-Dev"><img src="https://img.shields.io/badge/Developer-Md._Nayem_Hossain-6366f1?style=for-the-badge&logo=github&logoColor=white" alt="Developer"></a>
  <a href="https://www.linkedin.com/in/md-nayem-dev"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
</p>

---

## ⚡ What is PulseCut AI?

**PulseCut AI** is an all-in-one automated video studio designed to transform long YouTube videos, Twitch/Kick streams, podcasts, and video recordings into high-converting 9:16 vertical Shorts, Reels, and TikToks.

Unlike traditional clipping tools that lock you into monthly subscriptions, upload queues, or restrictive API limits, **PulseCut AI** runs directly on your local machine or server. Video rendering and speech recognition happen locally on your hardware, and AI clipping intelligence connects directly to your own LLM API key.

---

## ✨ Key Features

- 🎯 **AI Highlight Scouting**: Automatically identifies viral moments, exciting gameplay clutches, and memorable talking points using your favorite AI (Gemini, OpenAI, Claude, Grok, Groq, Ollama, etc.).
- 🎙️ **Private On-Device Transcription**: Fast offline speech-to-text powered by **Sherpa-ONNX** and NVIDIA NeMo models. Your audio never leaves your machine. Supports English, Arabic, Hindi, Urdu, and more.
- 🎨 **Dynamic Kinetic Captions**: Active word-by-word colored subtitle highlighting with customizable themes, fonts, emojis, and layouts.
- 📹 **Smart Facecam Tracking**: Automatically detects webcams and speakers in gaming streams and podcasts, centering them perfectly in 9:16 vertical videos.
- 🔴 **Live Stream Clipping**: Monitor live Twitch, YouTube, or Kick streams in real time. PulseCut buffers the audio and generates instant clips while the stream is still broadcasting.
- 🤖 **Quota-Free YouTube Studio Bot**: Built-in Playwright browser automation that bypasses Google Cloud API daily upload quotas. Upload and schedule 40–50+ Shorts directly through YouTube Studio in a visible or background Chrome browser.
- 📅 **Multi-Platform Scheduler**: Connect YouTube, Instagram Reels, and TikTok to queue and auto-publish content with custom spacing and daily caps.
- 👤 **Single or Multi-User Mode**: Runs with no sign-in required on your local PC, or toggle `PEAKCUT_ACCOUNTS=1` for a complete multi-user SaaS platform with admin metrics and authentication.

---

## 🚀 Quick Start Guide

### Prerequisites

1. **Python 3.10+**: Download from [python.org](https://www.python.org/downloads/).
2. **FFmpeg**:
   - **Windows**: `winget install Gyan.FFmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`
3. **Google Chrome**: Recommended for YouTube Studio browser automation.

---

### Step 1: Clone Repository

```bash
git clone https://github.com/MdNayem-Dev/PulseCut-AI.git
cd PulseCut-AI
```

> **Tip for Windows**: Keep the folder path short (e.g., `C:\pulsecut` or `D:\pulsecut`) to prevent Windows path length issues with speech recognition libraries.

---

### Step 2: Set Up Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

---

### Step 4: Configure Settings

Copy the example environment file:

```bash
# Windows:
copy .env.example .env

# macOS / Linux:
cp .env.example .env
```

*(Optional)* You can add your AI key directly to `.env`, or simply enter it in the web dashboard under **Settings → AI**.

---

### Step 5: Start PulseCut AI

```bash
python -m studio.server
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8765](http://127.0.0.1:8765)**

*(On first start, the lightweight offline speech model (~480 MB) downloads automatically once).*

---

## 🤖 YouTube Studio Bot (Quota-Free Automation)

The standard YouTube Data API v3 enforces a strict **10,000 units/day quota**, which limits uploads to only **3–5 videos per day**.

PulseCut AI features an intelligent, quota-free browser automation bot powered by Playwright:

1. In the PulseCut dashboard, click **"Sign In to YouTube"** (or run `python tools/login.py` in your terminal).
2. A local Chrome window opens directly on your desktop. Log in to your Google / YouTube account once.
3. Queue up as many clips as you want in PulseCut.
4. Click **"Upload queued shorts"** — watch Chrome automatically upload each video, fill in titles, descriptions, and hashtags, and schedule them for their target release times!

---

## 🧠 Choose Your AI Service

PulseCut AI works with any modern LLM that supports structured output:

| Provider | Supported Models | Key Source |
|---|---|---|
| **Google Gemini** | `gemini-2.5-flash`, `gemini-1.5-pro` | [Google AI Studio](https://aistudio.google.com/apikey) |
| **OpenAI** | `gpt-4o-mini`, `gpt-4o` | [OpenAI Platform](https://platform.openai.com/api-keys) |
| **Grok (xAI)** | `grok-4` | [xAI Console](https://console.x.ai) |
| **Groq** | `llama-3.3-70b-versatile` | [Groq Cloud](https://console.groq.com/keys) |
| **Anthropic** | `claude-3-5-sonnet` | [Anthropic Console](https://console.anthropic.com) |
| **Ollama** | Local models (e.g. `llama3.1`) — No API key needed | [Ollama](https://ollama.com) |

> **No AI key?** PulseCut can still cut clips based purely on audio volume and energy peaks without an AI model!

---

## 🛠️ Testing & Verification

PulseCut AI includes a comprehensive test suite covering permissions, queue management under heavy load, caption alignment, facecam detection, and security hardening:

```bash
python tests/run.py
```

The test runner starts an isolated sandbox server on a spare port and cleans up all temporary data upon completion.

---

## 👨‍💻 Author & Maintainer

**Developed with ❤️ by Md. Nayem Hossain**

- 🌐 **LinkedIn**: [linkedin.com/in/md-nayem-dev](https://www.linkedin.com/in/md-nayem-dev)
- 🐙 **GitHub**: [github.com/MdNayem-Dev](https://github.com/MdNayem-Dev)

If you find this project useful, please give it a ⭐️ on GitHub!

---

## 📄 License

This project is open-source and released under the [MIT License](LICENSE).
