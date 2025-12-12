#!/usr/bin/env python3
"""
hirist_apply.py
Robust Hirist auto apply with debugging artifacts.
Saves screenshots and page HTML to ./debug_hirist_<timestamp>.*
"""

import os
import time
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# ---- Load config ----
load_dotenv()
HIRIST_EMAIL = os.getenv("HIRIST_EMAIL")
HIRIST_PASSWORD = os.getenv("HIRIST_PASSWORD")
HIRIST_SEARCH_URL = os.getenv("HIRIST_SEARCH_URL", "https://www.hirist.tech/")
HIRIST_MAX_JOBS_PER_RUN = int(os.getenv("HIRIST_MAX_JOBS_PER_RUN", "5"))

if not HIRIST_EMAIL or not HIRIST_PASSWORD:
    raise RuntimeError("HIRIST_EMAIL or HIRIST_PASSWORD not set in .env")

# ---- Helpers ----
def debug_dump(driver, prefix="hirist_debug"):
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    png = f"{prefix}_{ts}.png"
    html = f"{prefix}_{ts}.html"
    try:
        driver.save_screenshot(png)
    except Exception as e:
        print(f"[DEBUG] save_screenshot failed: {e}")
    try:
        with open(html, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    except Exception as e:
        print(f"[DEBUG] write page_source failed: {e}")
    print(f"[DEBUG] Wrote debug files: {png}, {html}")

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    # For cron you may want headless later, but while debugging keep GUI visible:
    # chrome_options.add_argument("--headless=new")
    # Use a persistent profile if you prefer to keep login cookies between runs:
    # chrome_options.add_argument("--user-data-dir=/home/manoj/.chrome-hirist-profile")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(8)
    return driver

def click_jobseeker_login(driver):
    try:
        # Try common selectors for the Jobseeker Login button
        btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Jobseeker Login') or contains(.,'Jobseeker') or //a[contains(.,'Jobseeker Login')]]"))
        )
        driver.execute_script("arguments[0].click();", btn)
        print("[INFO] Clicked Jobseeker Login.")
        time.sleep(2)
        return True
    except TimeoutException:
        print("[WARN] Jobseeker Login button not found via XPATH; trying alternate selectors.")
    except Exception as e:
        print(f"[WARN] clicking Jobseeker Login raised: {e}")
    # fallback: try header button or link by text
    try:
        for txt in ("Jobseeker Login", "Login", "Sign in"):
            elems = driver.find_elements(By.XPATH, f"//*[contains(text(),'{txt}')]")
            for el in elems:
                try:
                    driver.execute_script("arguments[0].click();", el)
                    print(f"[INFO] Clicked login element with text '{txt}'.")
                    time.sleep(2)
                    return True
                except Exception:
                    continue
    except Exception as e:
        print(f"[WARN] fallback click attempt failed: {e}")
    return False

def locate_login_fields_and_submit(driver):
    """
    Try to find email/password inputs and login button.
    If OTP-only flow or different structure, dump debug artifacts and return False.
    """
    try:
        # Wait for an input that looks like email
        email = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@type,'email') or contains(@placeholder,'Email') or contains(@name,'email')]"))
        )
        # find password if present
        try:
            pwd = driver.find_element(By.XPATH, "//input[contains(@type,'password') or contains(@placeholder,'Password') or contains(@name,'password')]")
        except NoSuchElementException:
            # OTP-only or stepwise login
            print("[WARN] Password field not found - Hirist might be using OTP-only login or different flow.")
            debug_dump(driver, prefix="hirist_login_otp_detected")
            return False

        # Fill fields
        email.clear(); email.send_keys(HIRIST_EMAIL)
        pwd.clear(); pwd.send_keys(HIRIST_PASSWORD)

        # Click a button named Login, Log In, SUBMIT etc
        btn_candidates = driver.find_elements(By.XPATH, "//button[contains(.,'Login') or contains(.,'LOG IN') or contains(.,'Sign in') or contains(.,'Submit')]")
        if not btn_candidates:
            print("[WARN] Login button not found after filling credentials.")
            debug_dump(driver, prefix="hirist_no_login_btn")
            return False

        # click first visible candidate
        for btn in btn_candidates:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)
                print("[INFO] Clicked login submit.")
                time.sleep(4)
                return True
            except Exception:
                continue

        print("[WARN] Could not click any login button candidates.")
        debug_dump(driver, prefix="hirist_login_btn_click_fail")
        return False

    except TimeoutException:
        print("[ERROR] Login fields never appeared. Dumping debug info.")
        debug_dump(driver, prefix="hirist_login_fields_missing")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error locating login fields: {e}")
        debug_dump(driver, prefix="hirist_login_unexpected")
        return False

def collect_job_links(driver):
    print(f"[INFO] Opening search/listing: {HIRIST_SEARCH_URL}")
    driver.get(HIRIST_SEARCH_URL)
    time.sleep(4)
    debug_dump(driver, prefix="hirist_listing_before_collect")
    try:
        # Job cards can be anchor tags; collect candidates
        anchors = driver.find_elements(By.XPATH, "//a[contains(@href,'/j/') or contains(@href,'/job-') or contains(@href,'/jobs/')]")
        hrefs = []
        for a in anchors:
            href = a.get_attribute("href")
            if href and "hirist.tech" in href and "login" not in href and href not in hrefs:
                hrefs.append(href)
        print(f"[INFO] Collected {len(hrefs)} job links (filtered).")
        return hrefs
    except Exception as e:
        print(f"[ERROR] collecting job links failed: {e}")
        debug_dump(driver, prefix="hirist_collect_links_err")
        return []

def apply_on_job_page(driver, url):
    print(f"[INFO] Opening job: {url}")
    driver.get(url)
    time.sleep(3)
    debug_dump(driver, prefix="hirist_job_open")
    # Try multiple apply patterns
    xpaths = [
        "//button[contains(.,'Apply') or contains(.,'APPLY')]",
        "//a[contains(.,'Apply') or contains(@href,'apply')]",
        "//button[contains(@class,'apply') or contains(@id,'apply')]",
    ]
    for xp in xpaths:
        try:
            el = driver.find_element(By.XPATH, xp)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.6)
            driver.execute_script("arguments[0].click();", el)
            print("[INFO] Clicked apply button.")
            time.sleep(3)
            debug_dump(driver, prefix="hirist_applied")
            return True
        except NoSuchElementException:
            continue
        except Exception as e:
            print(f"[WARN] clicking xpath {xp} failed: {e}")
    print("[INFO] No Apply button found on this job page.")
    return False

def auto_apply_hirist(driver):
    links = collect_job_links(driver)
    if not links:
        print("[ERROR] No job links found, exiting.")
        return
    applied = 0
    for link in links:
        if applied >= HIRIST_MAX_JOBS_PER_RUN:
            break
        try:
            ok = apply_on_job_page(driver, link)
            if ok:
                applied += 1
        except Exception as e:
            print(f"[WARN] error processing {link}: {e}")
    print(f"[INFO] Completed auto-apply. Applied: {applied}")

def main():
    print("[DEBUG] hirist_apply.py main starting...")
    driver = start_driver()
    try:
        driver.get("https://www.hirist.tech/")
        time.sleep(2)
        if not click_jobseeker_login(driver):
            print("[WARN] Could not click Jobseeker login - maybe already on login or logged in.")
        else:
            # try to fill normal email/password login
            ok = locate_login_fields_and_submit(driver)
            if not ok:
                print("[INFO] Manual login may be required (OTP flows or different popup). Exiting early to allow manual login.")
                # dump debug and exit rather than trying to auto-apply while logged out
                debug_dump(driver, prefix="hirist_after_failed_login")
                return

        # small wait after login
        time.sleep(4)
        print(f"[DEBUG] After login URL: {driver.current_url}")
        auto_apply_hirist(driver)
    finally:
        print("[INFO] quitting driver.")
        try:
            driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    main()
