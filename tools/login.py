"""Interactive terminal tool to log in to YouTube Studio for PeakCut automation.
Run in terminal:
    python tools/login.py
"""
import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PROFILE_DIR = DATA_DIR / "youtube_profile"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)
AUTH_FILE = DATA_DIR / "youtube_auth.json"


def clean_locks():
    """Remove lock files from the profile directory."""
    for f in (PROFILE_DIR / "lockfile", PROFILE_DIR / "SingletonLock", PROFILE_DIR / "SingletonCookie", PROFILE_DIR / "SingletonSocket"):
        if f.exists():
            try:
                f.unlink(missing_ok=True)
            except Exception:
                pass


def import_cookies(cookie_file: Path) -> bool:
    """Import exported cookies (JSON or Netscape format) into the bot session."""
    if not cookie_file.is_file():
        print(f"[ERROR] Cookie file not found: {cookie_file}")
        return False
    
    content = cookie_file.read_text(encoding="utf-8").strip()
    cookies = []
    
    # Try JSON format (from Cookie-Editor extension)
    if content.startswith("["):
        try:
            raw = json.loads(content)
            for c in raw:
                # Convert to playwright cookie schema
                cookie = {
                    "name": c.get("name"),
                    "value": c.get("value"),
                    "domain": c.get("domain", ".youtube.com"),
                    "path": c.get("path", "/"),
                    "secure": c.get("secure", True),
                    "httpOnly": c.get("httpOnly", False),
                }
                if "sameSite" in c and c["sameSite"] in ("Strict", "Lax", "None"):
                    cookie["sameSite"] = c["sameSite"]
                cookies.append(cookie)
        except Exception as e:
            print(f"[ERROR] Failed to parse JSON cookies: {e}")
            return False
    else:
        # Netscape cookies.txt format
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 7:
                cookies.append({
                    "domain": parts[0],
                    "path": parts[2],
                    "secure": parts[3].upper() == "TRUE",
                    "name": parts[5],
                    "value": parts[6],
                })

    if not cookies:
        print("[ERROR] No valid cookies found in file.")
        return False

    auth_data = {"cookies": cookies, "origins": []}
    AUTH_FILE.write_text(json.dumps(auth_data, indent=2), encoding="utf-8")
    print(f"[SUCCESS] Successfully imported {len(cookies)} cookies into {AUTH_FILE.name}!")
    
    # Verify with headless browser
    print("Verifying session with YouTube Studio...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        ctx = browser.new_context(storage_state=str(AUTH_FILE))
        page = ctx.new_page()
        page.goto("https://studio.youtube.com", timeout=30000)
        url = page.url
        browser.close()
        if "studio.youtube.com" in url and "accounts.google.com" not in url and "signin" not in url:
            print("[SUCCESS] Verified! Bot is logged in to YouTube Studio.")
            return True
        else:
            print("[WARNING] Cookies loaded, but YouTube Studio redirected to sign in. The cookies may be expired or missing auth keys.")
            return False


def interactive_login(channel="chrome"):
    """Open a visible browser window for the user to log in."""
    clean_locks()
    print("\n====================================================================")
    print("   YouTube Studio Bot - Terminal Sign In Tool")
    print("====================================================================")
    print(f"Browser: {channel.upper()}")
    print(f"Profile: {PROFILE_DIR}")
    print("\nLaunching browser window...")

    with sync_playwright() as p:
        browser_type = getattr(p, "chromium")
        try:
            ctx = browser_type.launch_persistent_context(
                str(PROFILE_DIR.resolve()),
                channel=channel,
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--start-maximized",
                ],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
            )
        except Exception as e:
            if channel == "chrome":
                print(f"[NOTICE] Could not launch Chrome ({e}). Trying Microsoft Edge...")
                return interactive_login(channel="msedge")
            raise

        try:
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            # Anti-detection
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("Opening https://studio.youtube.com ...")
            page.goto("https://studio.youtube.com", timeout=60000)
            
            print("\n--------------------------------------------------------------------")
            print("  --> BROWSER WINDOW OPENED ON YOUR SCREEN! <--")
            print("  1. In the browser, log in to your Google / YouTube account.")
            print("  2. Select the YouTube channel you want to post to.")
            print("  3. Waiting for login completion (this script will detect it automatically)...")
            print("--------------------------------------------------------------------\n")

            for sec in range(300):
                time.sleep(3)
                try:
                    url = page.url
                except Exception:
                    print("\n[INFO] Browser was closed.")
                    break

                if "studio.youtube.com" in url and "accounts.google.com" not in url and "signin" not in url:
                    print("\n" + "="*60)
                    print("  [SUCCESS] LOGIN DETECTED & VERIFIED!")
                    print("="*60)
                    # Save storage state JSON as backup
                    try:
                        ctx.storage_state(path=str(AUTH_FILE))
                        print(f"  Saved backup session state to: {AUTH_FILE.name}")
                    except Exception:
                        pass
                    print("  Your session has been saved permanently.")
                    print("  You can now return to PeakCut dashboard to upload & schedule shorts!")
                    print("="*60 + "\n")
                    time.sleep(3)
                    return True
                
                if (sec + 1) % 10 == 0:
                    print(f"  [Waiting] Still waiting for sign-in ({sec * 3}s elapsed)...")

            print("\n[INFO] Timed out or finished waiting.")
            return False
        finally:
            ctx.close()


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] in ("--import", "-i"):
        import_cookies(Path(sys.argv[2]))
    else:
        interactive_login()
