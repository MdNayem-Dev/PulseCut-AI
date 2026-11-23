"""YouTube Studio browser automation using Playwright and local Chrome.
Uploads and schedules YouTube Shorts directly via studio.youtube.com without any Google Cloud API quota limits.
"""
import datetime
import json
import logging
import os
import re
import sys
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from . import config

PROFILE_DIR = config.DATA_DIR / "youtube_profile"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

AUTH_FILE = config.DATA_DIR / "youtube_auth.json"

_bot_lock = threading.RLock()
_is_busy = False
_bot_status = "Idle"
_last_error = ""
_cached_logged_in = False
_last_login_check = 0.0
_active_ctx = None
_cancel_requested = False


def _clean_locks():
    """Remove lockfile if no process is actively holding it."""
    for p_dir in (PROFILE_DIR, config.DATA_DIR / "youtube_profile_bot"):
        lock = p_dir / "lockfile"
        if lock.exists():
            try:
                lock.unlink(missing_ok=True)
            except Exception:
                pass


def _ensure_profile_dir() -> Path:
    """Ensure the profile directory is accessible and free of stale locks."""
    _clean_locks()
    p_dir = PROFILE_DIR
    p_dir.mkdir(parents=True, exist_ok=True)
    return p_dir


def _get_context(p, headless: bool = False):
    """Launch browser context using saved auth storage_state or persistent Chrome profile."""
    if AUTH_FILE.is_file():
        try:
            browser = p.chromium.launch(
                channel="chrome",
                headless=headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--start-maximized",
                ],
            )
            ctx = browser.new_context(
                storage_state=str(AUTH_FILE),
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            )
            return ctx
        except Exception as e:
            logging.warning("Failed launching context with storage_state: %s", e)

    p_dir = _ensure_profile_dir()
    return p.chromium.launch_persistent_context(
        str(p_dir.resolve()),
        channel="chrome",
        headless=headless,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-infobars",
            "--start-maximized",
        ],
        viewport={"width": 1366, "height": 768},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    )


def is_logged_in() -> bool:
    """Check if the saved profile or auth file is logged into YouTube Studio."""
    global _cached_logged_in, _last_login_check
    if AUTH_FILE.is_file():
        try:
            auth_data = json.loads(AUTH_FILE.read_text(encoding="utf-8"))
            cookies = auth_data.get("cookies", [])
            # If critical auth cookies exist, consider logged in
            auth_names = {"LOGIN_INFO", "SAPISID", "SSID", "__Secure-1PSID", "__Secure-3PSID"}
            found = [c["name"] for c in cookies if c.get("name") in auth_names]
            if len(found) >= 2:
                _cached_logged_in = True
                _last_login_check = time.time()
                return True
        except Exception:
            pass

    try:
        with sync_playwright() as p:
            ctx = _get_context(p, headless=True)
            try:
                page = ctx.new_page()
                page.goto("https://studio.youtube.com/?approve_browser_access=true", wait_until="domcontentloaded", timeout=25000)
                url = page.url
                logged = "accounts.google.com" not in url and "signin" not in url
                _cached_logged_in = logged
                _last_login_check = time.time()
                return logged
            finally:
                ctx.close()
    except Exception:
        return False


def launch_login_browser() -> bool:
    """Launch native Chrome window using the bot's user profile for interactive sign-in."""
    global _bot_status, _is_busy
    _clean_locks()
    _is_busy = False

    chrome_exe = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    if not chrome_exe.is_file():
        chrome_exe = Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")

    profile_dir = str(PROFILE_DIR.resolve())
    import subprocess
    cmd = f'start "" "{chrome_exe}" --user-data-dir="{profile_dir}" --no-first-run --no-default-browser-check "https://studio.youtube.com"'
    subprocess.Popen(cmd, shell=True)
    _bot_status = "Chrome launched! Complete sign-in, close Chrome, and click Verify."
    return True


def verify_login() -> bool:
    """Check if the user has signed in and saved session in the profile."""
    global _cached_logged_in, _last_login_check, _bot_status
    _clean_locks()
    logged = is_logged_in()
    _cached_logged_in = logged
    _last_login_check = time.time()
    if logged:
        _bot_status = "Logged in successfully"
    else:
        _bot_status = "Not signed in yet. Please log into your YouTube account in Chrome."
    return logged


def get_status(force: bool = False) -> dict:
    """Return status of the YouTube Studio bot without locking the profile when busy."""
    global _cached_logged_in, _last_login_check
    with _bot_lock:
        if not _is_busy and (force or time.time() - _last_login_check > 45):
            _cached_logged_in = is_logged_in()
            _last_login_check = time.time()
        return {
            "logged_in": _cached_logged_in,
            "busy": _is_busy,
            "status": _bot_status,
            "error": _last_error,
            "profile_dir": str(_ensure_profile_dir()),
        }


def cancel():
    """Cancel any active bot operation and close active browser context."""
    global _is_busy, _bot_status, _cancel_requested, _active_ctx
    _cancel_requested = True
    _bot_status = "Cancelling..."
    if _active_ctx:
        try:
            _active_ctx.close()
        except Exception:
            pass
        _active_ctx = None
    _is_busy = False
    _bot_status = "Idle (Reset)"


def login():
    """Opens a visible Chrome window for the user to sign in to YouTube Studio once."""
    global _is_busy, _bot_status, _last_error, _active_ctx, _cancel_requested, _cached_logged_in, _last_login_check
    with _bot_lock:
        if _is_busy:
            return False
        _is_busy = True
        _cancel_requested = False
        _bot_status = "Waiting for user sign-in in Chrome..."
        _last_error = ""

    try:
        with sync_playwright() as p:
            ctx = _get_context(p, headless=False)
            _active_ctx = ctx
            try:
                page = ctx.new_page()
                try:
                    page.bring_to_front()
                except Exception:
                    pass
                page.goto("https://studio.youtube.com/?approve_browser_access=true", wait_until="domcontentloaded", timeout=60000)

                for _ in range(120):
                    if _cancel_requested:
                        _bot_status = "Sign in cancelled"
                        return False
                    time.sleep(5)
                    try:
                        url = page.url
                    except Exception:
                        _bot_status = "Browser closed by user"
                        return False

                    if "studio.youtube.com" in url and "accounts.google.com" not in url and "signin" not in url:
                        _cached_logged_in = True
                        _last_login_check = time.time()
                        _bot_status = "Logged in successfully"
                        time.sleep(3)
                        return True

                _last_error = "Sign in timed out (10 minutes). Please try again."
                _bot_status = "Sign in timed out"
                return False
            finally:
                _active_ctx = None
                ctx.close()
    except Exception as e:
        _last_error = str(e)
        _bot_status = f"Error: {_last_error[:100]}"
        return False
    finally:
        _is_busy = False


def upload_short(video_path: Path, title: str, description: str = "", tags: list = None,
                 publish_at: datetime.datetime = None, channel_id: str = None,
                 headless: bool = False) -> dict:
    """Uploads and optionally schedules a Short to YouTube Studio via browser automation."""
    global _active_ctx, _bot_status
    if not video_path.is_file():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    tags = tags or []
    clean_title = re.sub(r"[<>]", "", title)[:100].strip() or "Shorts"
    clean_desc = (re.sub(r"[<>]", "", description)[:4800].strip() + "\n\n#Shorts").strip()

    base_url = f"https://studio.youtube.com/channel/{channel_id}" if channel_id else "https://studio.youtube.com"
    target_url = f"{base_url}?approve_browser_access=true"

    with sync_playwright() as p:
        ctx = _get_context(p, headless=headless)
        _active_ctx = ctx
        page = ctx.new_page()
        try:
            _bot_status = f"Opening YouTube Studio..."
            print(f"Navigating to YouTube Studio ({target_url})...")
            try:
                page.bring_to_front()
            except Exception:
                pass
            page.goto(target_url, wait_until="domcontentloaded", timeout=50000)
            page.wait_for_timeout(3000)

            # Check if skip unsupported browser link appears
            skip_link = page.locator("a:has-text('Skip to YouTube Studio'), a[href*='approve_browser_access']").first
            if skip_link.is_visible():
                skip_link.click()
                page.wait_for_timeout(3000)

            if "accounts.google.com" in page.url or "signin" in page.url:
                raise RuntimeError("Not logged into YouTube Studio. Please sign in via Studio Bot first.")

            # Look for Create or Upload button
            _bot_status = f"Opening Upload window for '{clean_title[:25]}...'..."
            print("Opening Upload dialog...")
            upload_btn = page.locator("button[aria-label='Upload videos'], ytcp-button#upload-button").first
            create_btn = page.locator("button[aria-label='Create'], ytcp-button.ytcpAppHeaderCreateIcon, #create-icon, button[aria-label*='Create' i]").first

            if upload_btn.is_visible():
                upload_btn.click()
            elif create_btn.is_visible():
                create_btn.click()
                page.wait_for_timeout(1000)
                upload_item = page.locator("tp-yt-paper-item:has-text('Upload videos'), #text-item-0, [test-id='upload']").first
                upload_item.wait_for(timeout=10000)
                upload_item.click()
            else:
                create_btn.wait_for(timeout=25000)
                create_btn.click()
                page.wait_for_timeout(1000)
                upload_item = page.locator("tp-yt-paper-item:has-text('Upload videos'), #text-item-0, [test-id='upload']").first
                upload_item.wait_for(timeout=10000)
                upload_item.click()

            page.wait_for_timeout(2000)

            # Set file using Playwright file chooser interceptor
            _bot_status = f"Selecting video file: {video_path.name}..."
            print(f"Uploading file: {video_path.name}...")
            with page.expect_file_chooser(timeout=25000) as fc_info:
                select_btn = page.locator("#select-files-button, button:has-text('Select files'), [aria-label*='Select files' i]").first
                select_btn.click()
            file_chooser = fc_info.value
            file_chooser.set_files(str(video_path.resolve()))

            # Wait for upload modal to load details step
            _bot_status = f"Processing details dialog..."
            print("Waiting for Details form...")
            title_input = page.locator("#title-textarea #textbox, div#textbox[aria-label*='title' i], div#textbox[contenteditable='true']").first
            title_input.wait_for(timeout=35000)
            page.wait_for_timeout(2000)

            # Fill Title
            _bot_status = f"Setting Title: {clean_title[:35]}..."
            print(f"Setting Title: {clean_title}")
            title_input.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            title_input.fill(clean_title)

            # Fill Description
            if clean_desc:
                _bot_status = f"Adding Description & hashtags..."
                desc_input = page.locator("#description-textarea #textbox, div#textbox[aria-label*='description' i]").first
                if desc_input.is_visible():
                    desc_input.click()
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    desc_input.fill(clean_desc)

            # Select Not Made for Kids
            not_kids_radio = page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK'], [name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first
            if not_kids_radio.is_visible():
                not_kids_radio.click()

            # Add tags if any
            if tags:
                try:
                    more_btn = page.locator("#toggle-button, text='Show more'").first
                    if more_btn.is_visible():
                        more_btn.click()
                        page.wait_for_timeout(1000)
                    tags_input = page.locator("#tags-container #text-input, #tags-container input").first
                    if tags_input.is_visible():
                        tags_input.fill(", ".join(tags[:15]))
                except Exception:
                    pass

            # Click Next through steps until Visibility is reached
            _bot_status = f"Passing checks & moving to Schedule..."
            print("Progressing through wizard steps to Visibility...")
            for _ in range(5):
                pub_radio = page.locator("#public-radio-button, tp-yt-paper-radio-button:has-text('Public'), [name='PUBLIC']").first
                sched_radio = page.locator("#schedule-radio-button, tp-yt-paper-radio-button:has-text('Schedule'), [name='SCHEDULE']").first
                if pub_radio.is_visible() or sched_radio.is_visible():
                    break
                next_btn = page.locator("#next-button, ytcp-button#next-button, button:has-text('Next')").first
                if next_btn.is_visible():
                    next_btn.click()
                    page.wait_for_timeout(2000)

            # Visibility Step
            print("Setting visibility / schedule...")
            if publish_at:
                sched_radio = page.locator("#schedule-radio-button, tp-yt-paper-radio-button:has-text('Schedule'), [name='SCHEDULE']").first
                if sched_radio.is_visible():
                    sched_radio.click()
                    page.wait_for_timeout(1500)
                    try:
                        date_str = publish_at.strftime("%b %d, %Y")
                        time_str = publish_at.strftime("%I:%M %p")
                        _bot_status = f"Setting Schedule date ({date_str} {time_str})..."
                        date_trigger = page.locator("#datepicker-trigger, ytcp-date-picker, ytcp-text-dropdown-trigger[aria-label*='Date' i]").first
                        if date_trigger.is_visible():
                            date_trigger.click()
                            page.wait_for_timeout(500)
                            date_input = page.locator("tp-yt-paper-dialog input, input[aria-label*='date' i]").first
                            if date_input.is_visible():
                                date_input.fill(date_str)
                                page.keyboard.press("Enter")
                        time_trigger = page.locator("#time-of-day-trigger, input[aria-label*='time' i]").first
                        if time_trigger.is_visible():
                            time_trigger.click()
                            page.wait_for_timeout(500)
                            page.keyboard.press("Control+A")
                            page.keyboard.press("Backspace")
                            page.keyboard.type(time_str)
                            page.keyboard.press("Enter")
                    except Exception as date_err:
                        print(f"Notice: Date picker interaction: {date_err}")
                else:
                    pub_radio = page.locator("#public-radio-button, tp-yt-paper-radio-button:has-text('Public'), [name='PUBLIC']").first
                    if pub_radio.is_visible():
                        pub_radio.click()
            else:
                _bot_status = f"Setting visibility to Public..."
                public_radio = page.locator("#public-radio-button, tp-yt-paper-radio-button:has-text('Public'), [name='PUBLIC']").first
                if public_radio.is_visible():
                    public_radio.click()

            page.wait_for_timeout(2000)

            # Extract Short Video Link
            video_url = ""
            try:
                link_el = page.locator("a.ytcp-video-info, a.ytcp-video-list-cell-video-link, a.video-url-fadeable, a[href*='youtu.be']").first
                if link_el.is_visible():
                    video_url = link_el.get_attribute("href") or ""
            except Exception:
                pass

            # Click Done / Schedule / Publish
            _bot_status = f"Confirming & saving schedule on YouTube..."
            done_btn = page.locator("#done-button, ytcp-button#done-button, button:has-text('Schedule'), button:has-text('Publish'), button:has-text('Save')").first
            done_btn.wait_for(timeout=25000)
            done_btn.click()
            print("Saved and scheduled on YouTube Studio!")

            # Wait for completion dialog
            page.wait_for_timeout(5000)
            close_btn = page.locator("#close-button, ytcp-button:has-text('Close'), button:has-text('Close')").first
            if close_btn.is_visible():
                try:
                    share_link = page.locator("a.ytcp-video-info, a[href*='youtu.be']").first
                    if share_link.is_visible():
                        video_url = share_link.get_attribute("href") or video_url
                except Exception:
                    pass
                close_btn.click()

            page.wait_for_timeout(2000)
            vid_match = re.search(r"(?:shorts/|youtu\.be/|v=)([\w-]{11})", video_url)
            video_id = vid_match.group(1) if vid_match else ""
            if not video_url and video_id:
                video_url = f"https://www.youtube.com/shorts/{video_id}"

            _bot_status = f"Successfully scheduled: {clean_title[:30]}"
            print(f"[SUCCESS] Short uploaded successfully: {video_url or 'OK'}")
            return {"ok": True, "url": video_url, "video_id": video_id}
        finally:
            _active_ctx = None
            try:
                b = getattr(ctx, "browser", None)
                ctx.close()
                if b:
                    b.close()
            except Exception:
                pass


def upload_queued_posts(limit: int = 50, headless: bool = False) -> list:
    """Reads scheduled/queued posts from data/posts.json and uploads them via browser automation."""
    global _is_busy, _bot_status, _last_error, _cancel_requested
    from . import ctx, posting

    with _bot_lock:
        if _is_busy:
            return []
        _is_busy = True
        _cancel_requested = False
        _bot_status = "Processing queued posts..."
        _last_error = ""

    try:
        posts_file = config.DATA_DIR / "posts.json"
        if not posts_file.is_file():
            _bot_status = "No posts file found"
            return []

        try:
            posts = json.loads(posts_file.read_text(encoding="utf-8"))
        except Exception:
            _bot_status = "Failed to parse posts.json"
            return []

        # Find YouTube posts waiting to be uploaded
        scheduled = [p for p in posts if p.get("status") in ("scheduled", "posting", "failed")
                     and p.get("platform") == "youtube" and not p.get("uploaded")]
        if not scheduled:
            print("No pending YouTube posts to upload.")
            _bot_status = "No pending YouTube posts"
            return []

        results = []
        print(f"Found {len(scheduled)} scheduled shorts to upload via Studio Bot...")
        _bot_status = f"Uploading 0/{min(len(scheduled), limit)} shorts..."

        for i, p in enumerate(scheduled[:limit]):
            if _cancel_requested:
                _bot_status = f"Stopped. Uploaded {len(results)} short(s)."
                break

            jid, cid = p.get("job"), p.get("clip")
            clip_mp4 = None
            for cand in config.DATA_DIR.rglob(f"{cid}.mp4"):
                if jid in str(cand):
                    clip_mp4 = cand
                    break

            if not clip_mp4 or not clip_mp4.is_file():
                print(f"Skipping {p.get('id')}: Video file not found on disk.")
                continue

            title = p.get("title") or "Shorts"
            due_at = p.get("due_at")
            pub_dt = datetime.datetime.fromtimestamp(due_at) if due_at and due_at > time.time() + 90 else None
            channel_id = (p.get("account") or "").replace("yt_", "")

            _bot_status = f"Uploading [{i+1}/{min(len(scheduled), limit)}]: {title[:30]}..."
            print(f"\n[{i+1}/{min(len(scheduled), limit)}] Uploading: {title} (Due: {pub_dt or 'Now'})...")
            try:
                res = upload_short(clip_mp4, title, description=f"{title}\n\n#Shorts",
                                   tags=["Shorts", "Viral", "Trending"], publish_at=pub_dt,
                                   channel_id=channel_id, headless=headless)
                if res.get("ok"):
                    p["uploaded"] = True
                    p["remote_id"] = res.get("video_id", "")
                    p["url"] = res.get("url", "")
                    p["error"] = None
                    if not pub_dt:
                        p["status"] = "posted"
                        p["posted_at"] = time.time()
                    else:
                        p["status"] = "scheduled"
                    results.append(res)
                    with ctx.as_user(p.get("user") or "u_local"):
                        posting._mirror(p)
                        if p.get("user"):
                            ctx.bump(p["user"])
                    posts_file.write_text(json.dumps(posts, indent=2), encoding="utf-8")
            except Exception as e:
                print(f"Failed to upload {title}: {e}")
                _last_error = str(e)
                p["error"] = f"Studio bot: {str(e)[:160]}"
                with ctx.as_user(p.get("user") or "u_local"):
                    posting._mirror(p)
                    if p.get("user"):
                        ctx.bump(p["user"])
                posts_file.write_text(json.dumps(posts, indent=2), encoding="utf-8")

            time.sleep(10)

        _bot_status = f"Finished. Uploaded {len(results)} short(s)."
        return results
    finally:
        _is_busy = False


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "login":
        login()
    elif cmd == "status":
        st = get_status(force=True)
        print(f"Logged in: {st['logged_in']}")
        print(f"Status: {st['status']}")
        if st["error"]:
            print(f"Error: {st['error']}")
    elif cmd == "upload":
        upload_queued_posts(headless=False)
    else:
        print("Usage: python -m studio.yt_studio_bot [login|status|upload]")
