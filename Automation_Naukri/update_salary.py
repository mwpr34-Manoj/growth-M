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
# Load credentials from .env
# =========================

load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    raise RuntimeError("NAUKRI_EMAIL or NAUKRI_PASSWORD not set in .env")


# =========================
# Helpers
# =========================

def parse_salary(text: str) -> int:
    """Convert something like '29,00,001' -> 2900001 (int)."""
    digits = "".join(ch for ch in (text or "") if ch.isdigit())
    return int(digits) if digits else 0


def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless=new")  # uncomment to run headless

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def login(driver):
    print("[INFO] Opening Naukri login page...")
    driver.get("https://www.naukri.com/mnjuser/login")
    time.sleep(3)

    if "login" not in driver.current_url:
        print("[INFO] Already logged in (no login page).")
        return

    email_input = driver.find_element(By.ID, "usernameField")
    pwd_input = driver.find_element(By.ID, "passwordField")

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


def update_salary_plus_one(driver):
    """Open profile → Employment → salary section and add ₹1 to salary."""
    print("[INFO] Opening profile page...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    wait = WebDriverWait(driver, 20)
    time.sleep(5)

    # 1) Open Employment section from Quick links
    try:
        print("[DEBUG] Opening Employment section from Quick links...")
        employment_row = driver.find_element(
            By.XPATH,
            "//*[normalize-space(text())='Employment']/ancestor::li[1]"
        )
        employment_link = employment_row.find_element(
            By.XPATH,
            ".//a[contains(.,'Add') or contains(.,'Edit') or contains(.,'Update')]"
        )
        driver.execute_script("arguments[0].click();", employment_link)
        time.sleep(3)
    except Exception as e:
        print(f"[ERROR] Could not open Employment section: {e}")
        return

    # 2) Wait for salary fields
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

    # helper to get input by label text
    def get_input_by_label(text):
        xpath = f"//label[contains(normalize-space(.),'{text}')]/following::input[1]"
        return driver.find_element(By.XPATH, xpath)

    try:
        current_input = get_input_by_label("Current salary")
        fixed_input = get_input_by_label("Fixed salary")
        variable_input = get_input_by_label("Variable salary")
    except Exception as e:
        print(f"[ERROR] Could not locate salary input fields: {e}")
        return

    # 3) Read existing values
    current = parse_salary(current_input.get_attribute("value"))
    fixed = parse_salary(fixed_input.get_attribute("value"))
    variable = parse_salary(variable_input.get_attribute("value"))

    print(f"[DEBUG] Existing salary: current={current}, fixed={fixed}, variable={variable}")

    # 4) Add ₹1 logic
    if fixed == 0 and current > 0 and variable == 0:
        # Only current filled
        current += 1
        fixed = current
    else:
        fixed += 1
        current = fixed + variable

    print(f"[DEBUG] New salary (+₹1): current={current}, fixed={fixed}, variable={variable}")

    # 5) Write new values
    def set_field(elem, value: int):
        elem.click()
        elem.clear()
        elem.send_keys(str(value))

    try:
        set_field(current_input, current)
        set_field(fixed_input, fixed)
        set_field(variable_input, variable)
    except Exception as e:
        print(f"[ERROR] Failed writing salary fields: {e}")
        return

    # 6) Save the form
    try:
        save_btn = driver.find_element(
            By.XPATH,
            "//button[contains(., 'Save') or contains(., 'SAVE') or contains(., 'save')]"
        )
        driver.execute_script("arguments[0].click();", save_btn)
        print("[INFO] Clicked Save on salary form.")
    except Exception as e:
        print(f"[WARN] Could not find Save button: {e}")
        return

    time.sleep(3)
    print("[INFO] Salary updated by ₹1 (best effort).")


def main():
    print("[DEBUG] update_salary.py main() starting...")
    driver = start_driver()
    try:
        login(driver)
        update_salary_plus_one(driver)
        print("[INFO] Salary update script finished.")
    finally:
        driver.quit()
        print("[INFO] Browser closed.")


if __name__ == "__main__":
    main()

