import os
import time
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
        # Original guess: span 'Resume headline' followed by edit span
        "//span[contains(translate(., 'RESUME HEADLINE', 'resume headline'), 'resume headline')]/following::span[contains(@class,'edit')][1]",

        # "Resume headline" text somewhere, then an edit icon/button nearby in same section
        "//*[contains(translate(., 'RESUME HEADLINE', 'resume headline'), 'resume headline')]/ancestor::section[1]//span[contains(@class,'edit') or contains(.,'Edit')][1]",

        # In case it's in a div/card
        "//*[contains(translate(., 'RESUME HEADLINE', 'resume headline'), 'resume headline')]/ancestor::div[1]//span[contains(@class,'edit') or contains(.,'Edit')][1]",

        # Fallback: any element with text 'Resume headline', then following edit span/button
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


def find_resume_headline_textarea(driver):
    """
    Try multiple XPaths to find the Resume Headline textarea.
    """
    xpaths = [
        "//textarea[contains(@placeholder,'Describe')]",           # common placeholder
        "//textarea[contains(translate(@placeholder, 'HEADLINE', 'headline'),'headline')]",
        "//textarea[contains(@class,'resume') or contains(@id,'resume')]",
        "//textarea"  # last resort – first textarea on popup
    ]
    for xp in xpaths:
        try:
            elem = driver.find_element(By.XPATH, xp)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            return elem
        except Exception:
            continue
    return None


# =========================
# Refresh profile (Resume Headline only)
# =========================
def refresh_profile_resume_headline(driver):
    """
    Refresh profile by editing resume headline with a tiny change.
    This bumps 'Last updated' so your profile comes higher in HR search.
    """
    print("[INFO] Refreshing profile via resume headline...")

    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(5)

    # 1) Find and click the Resume Headline edit button
    try:
        edit_btn = find_resume_headline_edit_button(driver)
        if not edit_btn:
            print("[WARN] Could not find Resume Headline edit button with any locator.")
            return

        driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(3)
    except Exception as e:
        print(f"[WARN] Could not open Resume Headline edit box: {e}")
        return

    # 2) Find the textarea
    try:
        textarea = find_resume_headline_textarea(driver)
        if not textarea:
            print("[ERROR] Could not find Resume Headline textarea.")
            return

        text = textarea.get_attribute("value") or ""

        # Tiny change: toggle trailing dot
        if text.endswith("."):
            new_text = text[:-1]
        else:
            new_text = text + "."

        textarea.clear()
        textarea.send_keys(new_text)
        time.sleep(1)

        # 3) Click Save
        try:
            save_btn = driver.find_element(
                By.XPATH,
                "//button[contains(., 'Save') or contains(., 'SAVE')]"
            )
        except Exception:
            # fallback: any visible button in popup
            try:
                save_btn = driver.find_element(
                    By.XPATH,
                    "(//button[contains(.,'Save') or contains(.,'SAVE')])[1]"
                )
            except Exception as e:
                print(f"[ERROR] Could not find Save button: {e}")
                return

        driver.execute_script("arguments[0].click();", save_btn)

        print("[INFO] Resume headline refreshed successfully (profile updated).")
        time.sleep(3)
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

