import os
import time
import re
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -----------------------------
# CONFIG – edit if needed
# -----------------------------

DRY_RUN = False  # set True → checks only, no apply click

INCLUDE_KEYWORDS = [
    "devops",
    "dev ops",
    "platform engineer",
    "platform engineering",
    "site reliability",
    "sre",
    "cloud engineer",
    "aws",
    "amazon web services",
    "kubernetes",
    "docker",
    "terraform",
    "infrastructure as code",
    "iac",
    "cicd",
    "ci/cd",
    "jenkins",
    "github actions",
    "gcp",
    "google cloud",
]

EXCLUDE_KEYWORDS = [
    "java developer",
    "frontend",
    "react",
    "angular",
    "php",
    "dotnet",
    ".net",
    "support engineer",
    "manual testing",
    "bpo",
    "sales",
    "data entry",
]

ALLOWED_LOCATIONS = [
    "bengaluru",
    "bangalore",
    "bengaluru/bangalore",
    "bengaluru / bangalore",
    "bangalore urban",
    "remote",
    "work from home",
    "wfh",
]

# Experience band for ~9 yrs profile
MIN_EXPERIENCE_YEARS = 8
MAX_EXPERIENCE_YEARS = 12

SEARCH_QUERY = "devops engineer"
SEARCH_LOCATION = "bengaluru"

SEARCH_URL = (
    f"https://www.naukri.com/{SEARCH_QUERY.replace(' ', '-')}"
    f"-jobs-in-{SEARCH_LOCATION.replace(' ', '-')}"
)

# -----------------------------
# FILTER LOGIC
# -----------------------------
def is_relevant_job(page_text: str) -> bool:
    text = page_text.lower()

    # 0) Skip old jobs
    age_match = re.search(r"posted[^0-9]*(\d+)\s+day", text)
    if age_match:
        days = int(age_match.group(1))
        if days > 30:
            print(f"[FILTER] skip: too old ({days} days)")
            return False

    # 1) Include keyword check
    if not any(kw in text for kw in INCLUDE_KEYWORDS):
        print("[FILTER] skip: no INCLUDE_KEYWORDS matched")
        return False

    # 2) Exclude keyword check
    if any(bad in text for bad in EXCLUDE_KEYWORDS):
        print("[FILTER] skip: contains EXCLUDE_KEYWORDS")
        return False

    # 3) Location check
    if not any(loc in text for loc in ALLOWED_LOCATIONS):
        print("[FILTER] skip: location not in ALLOWED_LOCATIONS")
        return False

    # 4) Experience parsing
    years = []

    for m in re.finditer(r"(\d+)\s*[-–]\s*(\d+)\s*(?:yrs|years|yr)", text):
        y1, y2 = int(m.group(1)), int(m.group(2))
        years.extend([y1, y2])

    for m in re.finditer(r"(\d+)\s*\+\s*(?:yrs|years|yr)", text):
        years.append(int(m.group(1)))

    if years:
        min_exp, max_exp = min(years), max(years)
        if max_exp < MIN_EXPERIENCE_YEARS or min_exp > MAX_EXPERIENCE_YEARS:
            print(f"[FILTER] skip: experience {min_exp}-{max_exp} outside {MIN_EXPERIENCE_YEARS}-{MAX_EXPERIENCE_YEARS}")
            return False

    return True

# -----------------------------
# MAIN SCRIPT
# -----------------------------
def main():
    load_dotenv()
    email = os.getenv("NAUKRI_EMAIL")
    password = os.getenv("NAUKRI_PASSWORD")

    if not email or not password:
        raise RuntimeError("Please set NAUKRI_EMAIL and NAUKRI_PASSWORD in .env")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        # LOGIN
        driver.get("https://www.naukri.com/")
        time.sleep(5)

        try:
            login_btn = driver.find_element(By.LINK_TEXT, "Login")
            login_btn.click()
            time.sleep(3)

            email_input = driver.find_element(
                By.XPATH,
                "//input[contains(@placeholder,'Email') or contains(@placeholder,'Username')]",
            )
            pass_input = driver.find_element(
                By.XPATH,
                "//input[@type='password' or contains(@placeholder,'password')]",
            )

            email_input.send_keys(email)
            pass_input.send_keys(password)
            pass_input.send_keys(Keys.ENTER)
            time.sleep(6)

        except NoSuchElementException:
            pass  # already logged in

        # SEARCH
        driver.get(SEARCH_URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)

        print("[INFO] Search URL:", driver.current_url)
        print("[INFO] Page title:", driver.title)

        applied_count = 0
        checked_count = 0

        visited = set()

        # LOOP PAGES
        for page in range(1, 5):
            time.sleep(4)
            print(f"[INFO] On page {page}")

            job_links_elems = driver.find_elements(
                By.XPATH,
                "//a[contains(@href,'/job-listings-') and @title]"
            )

            job_hrefs = []
            for el in job_links_elems:
                href = el.get_attribute("href")
                if href and href not in visited:
                    visited.add(href)
                    job_hrefs.append(href)

            print(f"[INFO] Found {len(job_hrefs)} job links on this page")

            # OPEN JOBS
            for href in job_hrefs:
                checked_count += 1

                try:
                    driver.execute_script("window.open(arguments[0]);", href)
                    driver.switch_to.window(driver.window_handles[-1])
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    time.sleep(3)

                    body_text = driver.find_element(By.TAG_NAME, "body").text

                    if not is_relevant_job(body_text):
                        print(f"[SKIP] {href}")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        continue

                    if DRY_RUN:
                        print(f"[MATCH] (dry run) {href}")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        continue

                    # APPLY LOGIC
                    applied_here = False
                    for xpath in [
                        "//button[contains(.,'Apply')]",
                        "//a[contains(.,'Apply')]",
                    ]:
                        try:
                            btn = driver.find_element(By.XPATH, xpath)
                            btn.click()
                            time.sleep(5)

                            after_text = driver.find_element(By.TAG_NAME, "body").text.lower()

                            if "error while processing" in after_text:
                                print(f"[NAUKRI ERROR] Apply failed for {href}")
                                applied_here = False
                            else:
                                applied_here = True

                            break

                        except:
                            continue

                    if applied_here:
                        applied_count += 1
                        print(f"[APPLIED] {href}")
                    else:
                        print(f"[SKIP / FAILED APPLY] {href}")

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                except Exception as e:
                    print(f"[ERROR job] {href} -> {e}")
                    if len(driver.window_handles) > 1:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    continue

            # NEXT PAGE
            try:
                next_btn = driver.find_element(
                    By.XPATH,
                    "//a[contains(.,'Next') or contains(@aria-label,'Next')]",
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_btn)
            except:
                break

        print(f"[DONE] Checked {checked_count} jobs, applied to {applied_count} relevant ones.")

    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()

