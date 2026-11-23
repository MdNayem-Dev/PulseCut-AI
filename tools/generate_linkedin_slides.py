"""Generate high-resolution professional LinkedIn showcase slides for PulseCut AI.
"""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "linkedin_assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Read images as base64 for embedding in self-contained HTML
def get_b64(path: Path) -> str:
    if path.is_file():
        mime = "image/png" if path.suffix == ".png" else "image/svg+xml"
        data = base64.b64encode(path.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{data}"
    return ""

DEV_IMG = get_b64(ROOT / "web" / "brand" / "developer.png")
LOGO_IMG = get_b64(ROOT / "web" / "brand" / "logo.svg")
RAW_DASH = get_b64(OUT_DIR / "dashboard_raw.png")

COMMON_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    width: 1920px;
    height: 1080px;
    background: #090b10;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #f1f5f9;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
}
.bg-glow {
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.25;
    pointer-events: none;
    z-index: 0;
}
.glow-cyan {
    width: 600px;
    height: 600px;
    background: #06b6d4;
    top: -150px;
    left: -100px;
}
.glow-purple {
    width: 700px;
    height: 700px;
    background: #6366f1;
    bottom: -200px;
    right: -100px;
}
.glow-emerald {
    width: 500px;
    height: 500px;
    background: #10b981;
    top: 30%;
    left: 45%;
    opacity: 0.15;
}
.container {
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    padding: 60px 80px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.brand-pill {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.15);
    padding: 8px 18px;
    border-radius: 9999px;
    backdrop-filter: blur(12px);
}
.brand-logo-img {
    height: 28px;
}
.badge-tag {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
    padding: 4px 10px;
    border-radius: 6px;
}
.dev-badge {
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(99, 102, 241, 0.3);
    padding: 8px 20px;
    border-radius: 9999px;
}
.dev-photo {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #38bdf8;
}
.dev-info {
    display: flex;
    flex-direction: column;
}
.dev-name {
    font-size: 15px;
    font-weight: 700;
    color: #f8fafc;
}
.dev-role {
    font-size: 12px;
    color: #94a3b8;
}
.slide-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    border-top: 1px solid rgba(148, 163, 184, 0.1);
}
.footer-links {
    display: flex;
    gap: 24px;
    font-size: 15px;
    color: #94a3b8;
}
.footer-links span {
    color: #38bdf8;
    font-weight: 600;
}
.slide-num {
    font-size: 14px;
    font-weight: 600;
    color: #64748b;
    letter-spacing: 2px;
}
"""

SLIDES = [
    # SLIDE 1: Hero & Overview
    f"""<!DOCTYPE html>
    <html>
    <head><style>{COMMON_CSS}
    .hero-content {{
        display: flex;
        gap: 60px;
        align-items: center;
        flex: 1;
        margin: 40px 0;
    }}
    .hero-left {{
        flex: 1.1;
        display: flex;
        flex-direction: column;
        gap: 24px;
    }}
    .hero-title {{
        font-size: 64px;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero-title span {{
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero-desc {{
        font-size: 22px;
        line-height: 1.5;
        color: #94a3b8;
    }}
    .tech-stack {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 10px;
    }}
    .tech-pill {{
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        color: #e2e8f0;
    }}
    .hero-right {{
        flex: 1;
        position: relative;
    }}
    .mockup-frame {{
        width: 100%;
        background: #0f172a;
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 40px rgba(56, 189, 248, 0.15);
        overflow: hidden;
    }}
    .mockup-header {{
        height: 36px;
        background: #1e293b;
        display: flex;
        align-items: center;
        padding: 0 16px;
        gap: 8px;
    }}
    .dot {{ width: 10px; height: 10px; border-radius: 50%; }}
    .dot-red {{ background: #ef4444; }}
    .dot-yellow {{ background: #f59e0b; }}
    .dot-green {{ background: #10b981; }}
    .mockup-img {{
        width: 100%;
        display: block;
        height: 480px;
        object-fit: cover;
        object-position: top;
    }}
    </style></head>
    <body>
        <div class="bg-glow glow-cyan"></div>
        <div class="bg-glow glow-purple"></div>
        <div class="container">
            <div class="header">
                <div class="brand-pill">
                    <img src="{LOGO_IMG}" class="brand-logo-img"/>
                    <span class="badge-tag">Open Source Video Studio</span>
                </div>
                <div class="dev-badge">
                    <img src="{DEV_IMG}" class="dev-photo"/>
                    <div class="dev-info">
                        <span class="dev-name">Md. Nayem Hossain</span>
                        <span class="dev-role">Full-Stack & AI Automation Engineer</span>
                    </div>
                </div>
            </div>
            <div class="hero-content">
                <div class="hero-left">
                    <h1 class="hero-title">Turn Raw Long Videos Into <span>Viral Shorts</span> Completely Locally.</h1>
                    <p class="hero-desc">An end-to-end self-hosted studio powered by local neural speech recognition, multi-LLM moment scouting, facial auto-reframing, and a quota-free YouTube scheduler.</p>
                    <div class="tech-stack">
                        <div class="tech-pill">⚡ Python 3.10+</div>
                        <div class="tech-pill">🚀 FastAPI</div>
                        <div class="tech-pill">🤖 Playwright Automation</div>
                        <div class="tech-pill">🎙️ Sherpa-ONNX (Local)</div>
                        <div class="tech-pill">🎬 FFmpeg Dual-Crop</div>
                        <div class="tech-pill">🧠 Bring-Your-Own-AI</div>
                    </div>
                </div>
                <div class="hero-right">
                    <div class="mockup-frame">
                        <div class="mockup-header">
                            <div class="dot dot-red"></div>
                            <div class="dot dot-yellow"></div>
                            <div class="dot dot-green"></div>
                        </div>
                        <img src="{RAW_DASH}" class="mockup-img"/>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <div class="footer-links">
                    <span>GitHub:</span> github.com/MdNayem-Dev/PulseCut-AI &nbsp;•&nbsp; 
                    <span>LinkedIn:</span> linkedin.com/in/md-nayem-dev
                </div>
                <div class="slide-num">01 / 05</div>
            </div>
        </div>
    </body></html>""",

    # SLIDE 2: Architecture & Workflow
    f"""<!DOCTYPE html>
    <html>
    <head><style>{COMMON_CSS}
    .slide-body {{
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin: 30px 0;
    }}
    .title-group {{
        text-align: center;
        margin-bottom: 40px;
    }}
    .section-title {{
        font-size: 46px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 12px;
    }}
    .section-subtitle {{
        font-size: 20px;
        color: #94a3b8;
    }}
    .pipeline {{
        display: flex;
        justify-content: space-between;
        align-items: stretch;
        gap: 20px;
        position: relative;
    }}
    .pipe-card {{
        flex: 1;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 30px 24px;
        display: flex;
        flex-direction: column;
        position: relative;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }}
    .pipe-card:hover {{
        border-color: rgba(56, 189, 248, 0.4);
    }}
    .step-badge {{
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #0284c7, #6366f1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 20px;
    }}
    .step-name {{
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
        color: #f8fafc;
    }}
    .step-desc {{
        font-size: 14px;
        line-height: 1.6;
        color: #94a3b8;
        flex: 1;
    }}
    .step-tag {{
        margin-top: 18px;
        font-size: 12px;
        font-weight: 700;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.08);
        padding: 6px 10px;
        border-radius: 6px;
        display: inline-block;
    }}
    </style></head>
    <body>
        <div class="bg-glow glow-cyan"></div>
        <div class="bg-glow glow-purple"></div>
        <div class="container">
            <div class="header">
                <div class="brand-pill">
                    <img src="{LOGO_IMG}" class="brand-logo-img"/>
                    <span class="badge-tag">Pipeline Architecture</span>
                </div>
                <div class="dev-badge">
                    <img src="{DEV_IMG}" class="dev-photo"/>
                    <div class="dev-info">
                        <span class="dev-name">Md. Nayem Hossain</span>
                        <span class="dev-role">Full-Stack & AI Automation Engineer</span>
                    </div>
                </div>
            </div>
            <div class="slide-body">
                <div class="title-group">
                    <h2 class="section-title">End-to-End Automated Pipeline</h2>
                    <p class="section-subtitle">How hours of raw broadcast footage transform into vertical Shorts without leaving your machine</p>
                </div>
                <div class="pipeline">
                    <div class="pipe-card">
                        <div class="step-badge">1</div>
                        <div class="step-name">Stream Ingestion</div>
                        <div class="step-desc">Accepts YouTube, Twitch, Kick links, or manual MP4 uploads. Implements live rolling buffer for active streams.</div>
                        <div class="step-tag">yt-dlp & Fast Ingest</div>
                    </div>
                    <div class="pipe-card">
                        <div class="step-badge">2</div>
                        <div class="step-name">On-Device Speech</div>
                        <div class="step-desc">100% offline speech recognition via Sherpa-ONNX & NVIDIA NeMo transducers. Zero audio leaves your hardware.</div>
                        <div class="step-tag">Zero Cloud Fees</div>
                    </div>
                    <div class="pipe-card">
                        <div class="step-badge">3</div>
                        <div class="step-name">AI Moment Scout</div>
                        <div class="step-desc">LLMs evaluate transcripts, emotional pitch, and chat activity to score virality, hooks, titles, and key moments.</div>
                        <div class="step-tag">Gemini / GPT / Claude</div>
                    </div>
                    <div class="pipe-card">
                        <div class="step-badge">4</div>
                        <div class="step-name">Dynamic 9:16 Render</div>
                        <div class="step-desc">Facecam border detection isolates the speaker and gameplay into vertical dual-layers with animated kinetic subtitles.</div>
                        <div class="step-tag">FFmpeg Hardware Accel</div>
                    </div>
                    <div class="pipe-card">
                        <div class="step-badge">5</div>
                        <div class="step-name">Quota-Free Bot</div>
                        <div class="step-desc">Playwright daemon interacts directly with YouTube Studio, scheduling 40–50+ Shorts/day without Google API quotas.</div>
                        <div class="step-tag">Zero API Bottleneck</div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <div class="footer-links">
                    <span>GitHub:</span> github.com/MdNayem-Dev/PulseCut-AI &nbsp;•&nbsp; 
                    <span>LinkedIn:</span> linkedin.com/in/md-nayem-dev
                </div>
                <div class="slide-num">02 / 05</div>
            </div>
        </div>
    </body></html>""",

    # SLIDE 3: The Quota-Free YouTube Studio Bot
    f"""<!DOCTYPE html>
    <html>
    <head><style>{COMMON_CSS}
    .slide-body {{
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin: 20px 0;
    }}
    .title-group {{
        margin-bottom: 35px;
    }}
    .section-title {{
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 10px;
    }}
    .section-title span {{
        color: #ef4444;
    }}
    .section-subtitle {{
        font-size: 20px;
        color: #94a3b8;
    }}
    .comparison-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
    }}
    .compare-card {{
        background: rgba(15, 23, 42, 0.8);
        border-radius: 18px;
        padding: 36px;
        border: 1px solid rgba(148, 163, 184, 0.15);
        display: flex;
        flex-direction: column;
        gap: 20px;
    }}
    .card-bad {{
        border-color: rgba(239, 68, 68, 0.3);
        background: rgba(239, 68, 68, 0.04);
    }}
    .card-good {{
        border-color: rgba(16, 185, 129, 0.4);
        background: rgba(16, 185, 129, 0.04);
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.08);
    }}
    .compare-header {{
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: 24px;
        font-weight: 700;
    }}
    .text-bad {{ color: #f87171; }}
    .text-good {{ color: #34d399; }}
    .points-list {{
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }}
    .point-item {{
        display: flex;
        align-items: flex-start;
        gap: 12px;
        font-size: 17px;
        line-height: 1.5;
        color: #cbd5e1;
    }}
    .point-icon {{
        font-size: 18px;
        margin-top: 2px;
    }}
    .highlight-stat {{
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 16px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
    }}
    </style></head>
    <body>
        <div class="bg-glow glow-cyan"></div>
        <div class="bg-glow glow-purple"></div>
        <div class="container">
            <div class="header">
                <div class="brand-pill">
                    <img src="{LOGO_IMG}" class="brand-logo-img"/>
                    <span class="badge-tag">Automation Breakthrough</span>
                </div>
                <div class="dev-badge">
                    <img src="{DEV_IMG}" class="dev-photo"/>
                    <div class="dev-info">
                        <span class="dev-name">Md. Nayem Hossain</span>
                        <span class="dev-role">Full-Stack & AI Automation Engineer</span>
                    </div>
                </div>
            </div>
            <div class="slide-body">
                <div class="title-group">
                    <h2 class="section-title">Overcoming YouTube's <span>10,000-Unit</span> Daily Quota</h2>
                    <p class="section-subtitle">How custom Playwright browser automation enables scaling from 4 videos to 50+ Shorts per day</p>
                </div>
                <div class="comparison-grid">
                    <div class="compare-card card-bad">
                        <div class="compare-header text-bad">
                            <span>❌ Standard YouTube Data API v3</span>
                        </div>
                        <ul class="points-list">
                            <li class="point-item"><span class="point-icon">⚠️</span> <b>Strict Costly Quota:</b> 1,600 units consumed per video upload against a 10,000 unit daily limit.</li>
                            <li class="point-item"><span class="point-icon">🛑</span> <b>Severe Hard Cap:</b> Automation is completely blocked after just 4–5 uploads every 24 hours.</li>
                            <li class="point-item"><span class="point-icon">📋</span> <b>Complex Bureaucracy:</b> Requires Google Cloud project verification, audit reviews, and high quotas are rarely approved.</li>
                        </ul>
                        <div class="highlight-stat text-bad">Result: Bottlenecks automated content channels and agencies.</div>
                    </div>
                    <div class="compare-card card-good">
                        <div class="compare-header text-good">
                            <span>✅ PulseCut YouTube Studio Bot</span>
                        </div>
                        <ul class="points-list">
                            <li class="point-item"><span class="point-icon">⚡</span> <b>Zero API Units Used:</b> Interfaces directly with YouTube Studio web interface using local headless/headed Playwright.</li>
                            <li class="point-item"><span class="point-icon">🚀</span> <b>40–50+ Shorts Daily:</b> Automated batch scheduling with custom intervals, release calendars, and privacy toggles.</li>
                            <li class="point-item"><span class="point-icon">🔒</span> <b>Persistent Session Auth:</b> Safely remembers your Google login via Chrome profile storage state without storing raw passwords.</li>
                        </ul>
                        <div class="highlight-stat text-good">Result: True enterprise-level scheduling with zero Google Cloud costs.</div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <div class="footer-links">
                    <span>GitHub:</span> github.com/MdNayem-Dev/PulseCut-AI &nbsp;•&nbsp; 
                    <span>LinkedIn:</span> linkedin.com/in/md-nayem-dev
                </div>
                <div class="slide-num">03 / 05</div>
            </div>
        </div>
    </body></html>""",

    # SLIDE 4: Core Engineering Features
    f"""<!DOCTYPE html>
    <html>
    <head><style>{COMMON_CSS}
    .slide-body {{
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin: 20px 0;
    }}
    .title-group {{
        text-align: center;
        margin-bottom: 35px;
    }}
    .section-title {{
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 10px;
    }}
    .section-subtitle {{
        font-size: 20px;
        color: #94a3b8;
    }}
    .features-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px;
    }}
    .feat-card {{
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 28px 32px;
        display: flex;
        gap: 20px;
        align-items: flex-start;
        backdrop-filter: blur(12px);
    }}
    .feat-icon {{
        width: 52px;
        height: 52px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(99, 102, 241, 0.2));
        border: 1px solid rgba(56, 189, 248, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        flex-shrink: 0;
    }}
    .feat-content {{
        display: flex;
        flex-direction: column;
        gap: 8px;
    }}
    .feat-title {{
        font-size: 22px;
        font-weight: 700;
        color: #f1f5f9;
    }}
    .feat-desc {{
        font-size: 15px;
        line-height: 1.6;
        color: #94a3b8;
    }}
    </style></head>
    <body>
        <div class="bg-glow glow-cyan"></div>
        <div class="bg-glow glow-purple"></div>
        <div class="container">
            <div class="header">
                <div class="brand-pill">
                    <img src="{LOGO_IMG}" class="brand-logo-img"/>
                    <span class="badge-tag">Core Modules</span>
                </div>
                <div class="dev-badge">
                    <img src="{DEV_IMG}" class="dev-photo"/>
                    <div class="dev-info">
                        <span class="dev-name">Md. Nayem Hossain</span>
                        <span class="dev-role">Full-Stack & AI Automation Engineer</span>
                    </div>
                </div>
            </div>
            <div class="slide-body">
                <div class="title-group">
                    <h2 class="section-title">Built for Production Reliability</h2>
                    <p class="section-subtitle">Engineered modules tailored for content agencies, streamers, and high-frequency publishing</p>
                </div>
                <div class="features-grid">
                    <div class="feat-card">
                        <div class="feat-icon">🎯</div>
                        <div class="feat-content">
                            <div class="feat-title">Smart Facecam Isolation</div>
                            <div class="feat-desc">Computer vision heuristics detect webcam borders and gameplay zones, automatically reframing wide content into dynamic stacked 9:16 vertical video.</div>
                        </div>
                    </div>
                    <div class="feat-card">
                        <div class="feat-icon">💬</div>
                        <div class="feat-content">
                            <div class="feat-title">Kinetic Word Typography</div>
                            <div class="feat-desc">Sub-second word-level alignment renders eye-catching active word highlights, bold uppercase hooks, and emoji integrations using FFmpeg filters.</div>
                        </div>
                    </div>
                    <div class="feat-card">
                        <div class="feat-icon">🛡️</div>
                        <div class="feat-content">
                            <div class="feat-title">100% Data Privacy (Local-First)</div>
                            <div class="feat-desc">All media encoding, database records, and speech inference happen on your local storage. Sensitive audio and unpublished leaks never leave your machine.</div>
                        </div>
                    </div>
                    <div class="feat-card">
                        <div class="feat-icon">⚡</div>
                        <div class="feat-content">
                            <div class="feat-title">Adaptive Fair-Queue Scheduler</div>
                            <div class="feat-desc">Async job processing dynamically monitors CPU temperature, free RAM, and disk space, staggering heavy FFmpeg encodes to prevent OS freeze.</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <div class="footer-links">
                    <span>GitHub:</span> github.com/MdNayem-Dev/PulseCut-AI &nbsp;•&nbsp; 
                    <span>LinkedIn:</span> linkedin.com/in/md-nayem-dev
                </div>
                <div class="slide-num">04 / 05</div>
            </div>
        </div>
    </body></html>""",

    # SLIDE 5: Production Dashboard Preview
    f"""<!DOCTYPE html>
    <html>
    <head><style>{COMMON_CSS}
    .slide-body {{
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }}
    .title-group {{
        text-align: center;
        margin-bottom: 25px;
    }}
    .section-title {{
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 8px;
    }}
    .section-subtitle {{
        font-size: 20px;
        color: #94a3b8;
    }}
    .frame-container {{
        width: 100%;
        max-width: 1400px;
        background: #0f172a;
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 50px rgba(56, 189, 248, 0.15);
        overflow: hidden;
    }}
    .frame-header {{
        height: 40px;
        background: #1e293b;
        display: flex;
        align-items: center;
        padding: 0 20px;
        gap: 10px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }}
    .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .dot-red {{ background: #ef4444; }}
    .dot-yellow {{ background: #f59e0b; }}
    .dot-green {{ background: #10b981; }}
    .url-bar {{
        margin-left: 20px;
        background: rgba(15, 23, 42, 0.6);
        padding: 4px 16px;
        border-radius: 6px;
        font-size: 13px;
        color: #94a3b8;
        font-family: monospace;
    }}
    .dash-full-img {{
        width: 100%;
        height: 540px;
        display: block;
        object-fit: cover;
        object-position: top;
    }}
    </style></head>
    <body>
        <div class="bg-glow glow-cyan"></div>
        <div class="bg-glow glow-purple"></div>
        <div class="container">
            <div class="header">
                <div class="brand-pill">
                    <img src="{LOGO_IMG}" class="brand-logo-img"/>
                    <span class="badge-tag">Creator Dashboard</span>
                </div>
                <div class="dev-badge">
                    <img src="{DEV_IMG}" class="dev-photo"/>
                    <div class="dev-info">
                        <span class="dev-name">Md. Nayem Hossain</span>
                        <span class="dev-role">Full-Stack & AI Automation Engineer</span>
                    </div>
                </div>
            </div>
            <div class="slide-body">
                <div class="title-group">
                    <h2 class="section-title">Production-Ready Single Page Studio</h2>
                    <p class="section-subtitle">Zero framework bloat • Instant real-time state syncing • Direct multi-channel scheduling</p>
                </div>
                <div class="frame-container">
                    <div class="frame-header">
                        <div class="dot dot-red"></div>
                        <div class="dot dot-yellow"></div>
                        <div class="dot dot-green"></div>
                        <div class="url-bar">http://localhost:8765/app</div>
                    </div>
                    <img src="{RAW_DASH}" class="dash-full-img"/>
                </div>
            </div>
            <div class="slide-footer">
                <div class="footer-links">
                    <span>GitHub:</span> github.com/MdNayem-Dev/PulseCut-AI &nbsp;•&nbsp; 
                    <span>LinkedIn:</span> linkedin.com/in/md-nayem-dev
                </div>
                <div class="slide-num">05 / 05</div>
            </div>
        </div>
    </body></html>"""
]

FILENAMES = [
    "01_hero_showcase.png",
    "02_architecture_workflow.png",
    "03_quota_free_youtube_bot.png",
    "04_core_features.png",
    "05_live_dashboard.png"
]

def render_slides():
    print("Launching Playwright to render 5 professional LinkedIn slides...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1.5)
        for i, (html, filename) in enumerate(zip(SLIDES, FILENAMES)):
            target = OUT_DIR / filename
            temp_html = OUT_DIR / f"temp_{i}.html"
            temp_html.write_text(html, encoding="utf-8")
            page.goto(temp_html.as_uri())
            page.wait_for_timeout(600)
            page.screenshot(path=str(target))
            temp_html.unlink(missing_ok=True)
            print(f"[{i+1}/5] Rendered: {filename}")
        browser.close()
    print("All LinkedIn showcase slides successfully generated!")

if __name__ == "__main__":
    render_slides()
