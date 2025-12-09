import os
import time
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# =========================
# Load .env configuration
# =========================
load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    raise RuntimeError("NAUKRI_EMAIL or NAUKRI_PASSWORD not set in .env")

def _get_int_env(name: str, default: int) -> int:
    val = os.getenv(name)
    try:
        return int(val) if val is not None else default
    except ValueError:
        return default

NOTICE_PERIOD_DAYS = _get_int_env("NOTICE_PERIOD_DAYS", 90)
MAX_JOBS_PER_RUN = _get_int_env("MAX_JOBS_PER_RUN", 5)
ENABLE_SALARY_UPDATE = os.getenv("ENABLE_SALARY_UPDATE", "true").lower() == "true"


# =========================
# Helpers
# =========================

def parse_salary(text: str) -> int:
    """Convert '29,00,001' -> 2900001 (int)."""
    digits = "".join(ch for ch in (text or "") if ch.isdigit())
    return int(digits) if digits else 0


# =========================
# Browser setup
# =========================

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless=new")  # uncomment for headless

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
    print(f"[DEBUG] After login URL: https://www.naukri.com/mnjuser/login -> {driver.current_url}")


# =========================
# Salary update (+₹1)
# =========================

def update_salary_plus_one(driver):
    print("[INFO] Opening profile page to update salary...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    wait = WebDriverWait(driver, 20)

    time.sleep(5)

    # 1) Click the Employment quick-link (left label "Employment" row)
    try:
        print("[DEBUG] Trying to open Employment section from Quick links...")

        # Find the row that has the word "Employment"
        employment_row = driver.find_element(
            By.XPATH,
            "//*[normalize-space(text())='Employment']/ancestor::li[1]"
        )

        # In that row, click the Add/Edit/Update link or button
        employment_link = employment_row.find_element(
            By.XPATH,
            ".//a[contains(.,'Add') or contains(.,'Edit') or contains(.,'Update')]"
        )

        driver.execute_script("arguments[0].click();", employment_link)
        time.sleep(3)
    except Exception as e:
        print(f"[WARN] Could not click Employment quick link: {e}")

    # 2) Now wait for salary fields to appear
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[contains(normalize-space(.), 'Current salary')]")
            )
        )
        print("[INFO] Salary form visible, updating values...")
    except TimeoutException:
        print("[ERROR] Current salary field not found. Cannot update salary.")
        return

    def get_input_by_label_text(text):
        xpath = f"//label[contains(normalize-space(.),'{text}')]/following::input[1]"
        return driver.find_element(By.XPATH, xpath)

    try:
        current_input = get_input_by_label_text("Current salary")
        fixed_input = get_input_by_label_text("Fixed salary")
        variable_input = get_input_by_label_text("Variable salary")
    except Exception as e:
        print(f"[ERROR] Could not locate salary inputs: {e}")
        return

    # --- parse existing values ---
    current = parse_salary(current_input.get_attribute("value"))
    fixed = parse_salary(fixed_input.get_attribute("value"))
    variable = parse_salary(variable_input.get_attribute("value"))

    print(f"[DEBUG] Before update: current={current}, fixed={fixed}, variable={variable}")

    if fixed == 0 and current > 0 and variable == 0:
        # Only current filled; treat current as fixed
        current += 1
        fixed = current
    else:
        fixed += 1
        current = fixed + variable

    print(f"[DEBUG] After update (+₹1): current={current}, fixed={fixed}, variable={variable}")

    def set_salary_field(elem, value: int):
        elem.click()
        elem.clear()
        elem.send_keys(str(value))

    try:
        set_salary_field(current_input, current)
        set_salary_field(fixed_input, fixed)
        set_salary_field(variable_input, variable)
    except Exception as e:
        print(f"[ERROR] Failed setting salary fields: {e}")
        return

    # Save
    try:
        save_btn = driver.find_element(
            By.XPATH, "//button[contains(., 'Save') or contains(., 'SAVE') or contains(., 'save')]"
        )
        driver.execute_script("arguments[0].click();", save_btn)
        print("[INFO] Clicked Save on salary form.")
    except Exception as e:
        print(f"[WARN] Could not find/save salary form: {e}")
        return

    time.sleep(3)
    print("[INFO] Salary updated by ₹1 successfully (best effort).")


# =========================
# Apply to jobs
# =========================

def apply_jobs(driver, max_jobs: int = 5):
    print("[INFO] Opening Recommended Jobs page...")
    driver.get("https://www.naukri.com/mnjuser/recommendedjobs")
    wait = WebDriverWait(driver, 20)

    # Wait for any job card
    try:
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//article[contains(@class,'jobTuple')]"
                    " | //div[contains(@class,'cust-job-tuple')]"
                    " | //div[contains(@class,'jobTuple')]"
                )
            )
        )
    except TimeoutException:
        print("[ERROR] No job cards found on Recommended Jobs page.")
        return

    applied = 0
    main_window = driver.current_window_handle
    idx = 0

    while applied < max_jobs:
        job_cards = driver.find_elements(
            By.XPATH,
            "//article[contains(@class,'jobTuple')]"
            " | //div[contains(@class,'cust-job-tuple')]"
            " | //div[contains(@class,'jobTuple')]"
        )

        if idx >= len(job_cards):
            print("[INFO] No more job cards to process.")
            break

        card = job_cards[idx]
        idx += 1

        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", card
            )
            time.sleep(0.5)

            print(f"[INFO] Opening job card #{idx}...")
            driver.execute_script("arguments[0].click();", card)
            time.sleep(2)

            # If a new tab opened, switch to it; else we navigated in same tab
            handles = driver.window_handles
            if len(handles) > 1:
                driver.switch_to.window(handles[-1])
            else:
                # same tab, wait for job listing URL
                try:
                    wait.until(
                        EC.url_contains("/job-listings-")
                    )
                except TimeoutException:
                    print("[INFO] Job page did not load as expected, going back.")
                    driver.back()
                    time.sleep(2)
                    driver.switch_to.window(main_window)
                    continue

            # Now we are on the job page (detail)
            try:
                apply_btn = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(., 'Apply') or contains(., 'APPLY')]"
                            " | //a[contains(., 'Apply') or contains(., 'APPLY')]"
                        )
                    )
                )
            except TimeoutException:
                print("[INFO] No Apply button found on this job page, closing.")
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(main_window)
                else:
                    driver.back()
                time.sleep(2)
                continue

            # Check if already applied
            already_applied = driver.find_elements(
                By.XPATH,
                "//*[contains(translate(., 'APPLIED', 'applied'),'applied')]"
            )
            if already_applied:
                print("[INFO] This job looks already applied, closing.")
            else:
                try:
                    driver.execute_script("arguments[0].click();", apply_btn)
                    print("[INFO] Clicked Apply on this job.")
                    applied += 1
                except Exception as e:
                    print(f"[WARN] Could not click Apply: {e}")

            time.sleep(3)

            # Close job page and go back to Recommended Jobs
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(main_window)
            else:
                driver.back()
            time.sleep(2)

        except Exception as e:
            print(f"[WARN] Unexpected error while processing a job card: {e}")
            try:
                driver.switch_to.window(main_window)
            except Exception:
                pass

    print(f"[INFO] Finished applying. Total jobs applied this run: {applied}")


# =========================
# Main
# =========================

def main():
    print("[DEBUG] job_agent.py main() starting...")
    driver = start_driver()
    try:
        login(driver)
        if ENABLE_SALARY_UPDATE:
            update_salary_plus_one(driver)
        else:
            print("[INFO] Salary update disabled by config.")
        apply_jobs(driver, max_jobs=MAX_JOBS_PER_RUN)
        print("[INFO] Completed run.")
    finally:
        driver.quit()
        print("[INFO] Browser closed.")


if __name__ == "__main__":
    print("[DEBUG] __main__ block reached, calling main()")
    main()

