import os
import time
import re
from datetime import datetime

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# =========================
# Load configuration from .env
# =========================
load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    raise RuntimeError("NAUKRI_EMAIL or NAUKRI_PASSWORD not set in .env")


# =========================
# Browser setup
# =========================
def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless=new")  # uncomment if you want headless

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver


# =========================
# Login
# =========================
def login(driver):
    print("[INFO] Opening Naukri login page...")
    driver.get("https://www.naukri.com/mnjuser/login")
    time.sleep(3)

    # If not actually on login page, assume already logged in
    if "login" not in driver.current_url:
        print(f"[INFO] Already logged in (URL: {driver.current_url}). Skipping login.")
        return

    try:
        email_input = driver.find_element(By.ID, "usernameField")
        pwd_input = driver.find_element(By.ID, "passwordField")
    except Exception as e:
        print(f"[WARN] Login fields not found (maybe already logged in): {e}")
        return

    print("[INFO] Filling login form...")
    email_input.clear()
    email_input.send_keys(EMAIL)
    pwd_input.clear()
    pwd_input.send_keys(PASSWORD)

    login_btn = driver.find_element(
        By.XPATH,
        "//button[contains(., 'Login') or contains(., 'LOG IN') or contains(., 'log in')]"
    )
    login_btn.click()
    print("[INFO] Submitted login form...")
    time.sleep(5)
    print(f"[DEBUG] After login URL: {driver.current_url}")


# =========================
# Helpers for Resume Headline
# =========================
def find_resume_headline_edit_button(driver):
    """
    Try multiple XPaths to find the Resume Headline edit button.
    Returns the element or None.
    """
    xpaths = [
        # "Resume headline" text followed by edit icon
        "//span[contains(translate(., 'RESUME HEADLINE', 'resume headline'), 'resume headline')]/following::span[contains(@class,'edit')][1]",

        # In a section/card
        "//*[contains(translate(., 'RESUME HEADLINE', 'resume headline'), 'resume headline')]/ancestor::section[1]//span[contains(@class,'edit') or contains(.,'Edit')][1]",

        # In a div container
        "//*[contains(translate(., 'RESUME HEADLINE', 'resume headline'), 'resume headline')]/ancestor::div[1]//span[contains(@class,'edit') or contains(.,'Edit')][1]",

        # Fallback
        "//*[contains(.,'Resume headline') or contains(.,'Resume Headline')]/following::span[contains(@class,'edit') or contains(.,'Edit')][1]"
    ]

    for xp in xpaths:
        try:
            elem = driver.find_element(By.XPATH, xp)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            return elem
        except Exception:
            continue
    return None


def find_resume_headline_editor(driver):
    """
    Return (element, mode) where mode is 'textarea' or 'contenteditable'.
    """
    # Try textarea first
    textarea_xpaths = [
        "//textarea[contains(@placeholder,'Describe')]",
        "//textarea[contains(translate(@placeholder, 'HEADLINE', 'headline'),'headline')]",
        "//textarea[contains(@class,'resume') or contains(@id,'resume')]",
        "//textarea"
    ]
    for xp in textarea_xpaths:
        try:
            elem = driver.find_element(By.XPATH, xp)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            return elem, "textarea"
        except Exception:
            continue

    # Then try contenteditable divs
    contenteditable_xpaths = [
        "//div[@contenteditable='true']",
        "//div[contains(@class,'ql-editor')]",
        "//div[contains(@class,'resume') and @contenteditable='true']",
    ]
    for xp in contenteditable_xpaths:
        try:
            elem = driver.find_element(By.XPATH, xp)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            return elem, "contenteditable"
        except Exception:
            continue

    return None, None


def build_new_headline_text(old_text: str) -> str:
    """
    Take the existing headline and append/refresh a small timestamp suffix so
    every run is guaranteed to be different.
    Example suffix: ' · upd 09Dec1523'
    """
    if not old_text:
        old_text = ""

    # Remove any existing suffix of form " · upd 09Dec1523"
    base = re.sub(r"\s*·\s*upd\s+\d{2}[A-Za-z]{3}\d{4}$", "", old_text).rstrip()

    timestamp = datetime.now().strftime("%d%b%H%M")  # e.g. 09Dec1523
    new_text = f"{base} · upd {timestamp}"
    return new_text


# =========================
# Refresh profile (Resume Headline only)
# =========================
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)

def refresh_profile_resume_headline(driver):
    """
    Refresh profile by editing resume headline with a timestamped change.
    This bumps 'Last updated' so your profile comes higher in HR search.
    """
    print("[INFO] Refreshing profile via resume headline...")

    driver.get("https://www.naukri.com/mnjuser/profile")
    wait = WebDriverWait(driver, 20)
    time.sleep(5)

    # 1) Find and click the Resume Headline edit button
    try:
        edit_btn = find_resume_headline_edit_button(driver)
        if not edit_btn:
            print("[WARN] Could not find Resume Headline edit button with any locator.")
            return

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_btn)
        driver.execute_script("arguments[0].click();", edit_btn)
        print("[DEBUG] Clicked Resume Headline edit.")
    except Exception as e:
        print(f"[WARN] Could not open Resume Headline edit box: {e}")
        return

    # 2) Wait for popup/editor to appear
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea | //div[@contenteditable='true']")
            )
        )
        time.sleep(2)
    except TimeoutException:
        print("[ERROR] Resume Headline editor did not appear.")
        return

    # 3) Find the editor (textarea or contenteditable)
    editor, mode = find_resume_headline_editor(driver)
    if not editor:
        print("[ERROR] Could not find Resume Headline editor (textarea/contenteditable).")
        return

    try:
        if mode == "textarea":
            old_text = editor.get_attribute("value") or ""
        else:
            old_text = editor.text or ""

        print(f"[DEBUG] Old headline: {old_text!r}")
        new_text = build_new_headline_text(old_text)
        print(f"[DEBUG] New headline: {new_text!r}")

        if mode == "textarea":
            editor.clear()
            editor.send_keys(new_text)
        else:
            driver.execute_script("arguments[0].innerText = arguments[1];", editor, new_text)

        time.sleep(1)

        # 4) Click Save — try multiple locators & use JS click
        save_xpaths = [
            "//button[normalize-space(.)='Save']",
            "//button[contains(., 'Save') or contains(., 'SAVE')]",
            "//div[contains(@class,'modal')]//button[contains(.,'Save')]",
            "(//button[contains(.,'Save') or contains(.,'SAVE')])[1]"
        ]

        save_clicked = False
        for sx in save_xpaths:
            try:
                save_btn = wait.until(
                    EC.element_to_be_clickable((By.XPATH, sx))
                )
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)
                try:
                    save_btn.click()
                except ElementClickInterceptedException:
                    print("[DEBUG] Normal click intercepted, trying JS click...")
                    driver.execute_script("arguments[0].click();", save_btn)

                save_clicked = True
                print(f"[INFO] Clicked Save using xpath: {sx}")
                break
            except Exception:
                continue

        if not save_clicked:
            print("[ERROR] Could not find/click any Save button. Headline text changed but not saved.")
            return

        # 5) Wait a bit for popup to close / page to settle
        time.sleep(4)
        print("[INFO] Resume headline refresh attempt finished (check Last Updated on profile).")

    except Exception as e:
        print(f"[ERROR] Failed to refresh resume headline: {e}")



# =========================
# Main
# =========================
def main():
    print("[DEBUG] job_agent.py main() starting...")
    driver = start_driver()
    try:
        login(driver)
        refresh_profile_resume_headline(driver)
        print("[INFO] Completed profile refresh run.")
    finally:
        driver.quit()
        print("[INFO] Browser closed.")


if __name__ == "__main__":
    print("[DEBUG] __main__ block reached, calling main()")
    main()
