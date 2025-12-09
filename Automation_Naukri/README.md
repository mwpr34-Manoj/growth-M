Automation_Naukri

A complete automation toolkit built using Python + Selenium to manage and optimize your Naukri.com job search workflow.
This project includes:

Auto-login

Auto-refresh of resume headline

Auto-update salary (+₹1 trick)

Intelligent job filtering + AI-based matching

Auto-apply to relevant job postings

Highly configurable settings through .env

🚀 Features Overview
1. Auto Refresh Profile (Resume Headline)

Script: job_agent.py

Opens Naukri profile

Finds "Resume Headline" section

Makes a tiny modification (adds or removes .)

Saves the change → updates Last Updated timestamp

Helps rank higher in recruiter searches


job_agent

2. Auto Apply to Recommended Jobs

Script: job_agent.py

Opens Recommended Jobs

Iterates through job cards

Opens each job

Checks if "Apply" is available

If not already applied → applies automatically

Closes job tab, returns to main window


job_apply

3. Intelligent Job Filtering + Auto Apply

Script: job_apply.py
This is an advanced search-based auto-apply engine:

Searches: DevOps Engineer jobs in Bengaluru

Filters jobs using:

Keywords include/exclude lists

Experience band (8–12 years for your profile)

Allowed locations

Job age (<30 days)

Automatically applies to relevant jobs

Avoids job types not matching your skills


job_update

4. Auto Salary Updater (+₹1 Hack)

Script: update_salary.py

Opens employment section

Reads current/fixed/variable salary

Adds ₹1 to bump profile activity

Saves automatically


update_salary

🗂️ Project Structure
Automation_Naukri/
│── job_agent.py          # Refresh profile + apply recommended jobs
│── job_apply.py          # Search-based auto apply with filtering
│── job_update.py         # Advanced apply + salary update
│── update_salary.py      # Salary +1 updater only
│── .env                  # Credentials + settings
│── README.md             # Project documentation

🔧 Setup Instructions
1. Install Dependencies
pip install selenium python-dotenv

2. Download ChromeDriver

Ensure ChromeDriver version matches your Chrome browser.

Place it in:

/usr/local/bin  (Mac/Linux)
C:\chromedriver\ (Windows)

🔐 3. Configure .env File

Your .env file format (based on your uploaded file):


.env

NAUKRI_EMAIL=your_email
NAUKRI_PASSWORD=your_password
MAX_APPLICATIONS_PER_DAY=500
APPLIED_JOBS_FILE=applied_jobs.json

TOTAL_EXPERIENCE_YEARS=9
KUBERNETES_EXPERIENCE_YEARS=5
AWS_EXPERIENCE_YEARS=5
SHELL_EXPERIENCE_YEARS=5
PYTHON_EXPERIENCE_YEARS=3

NOTICE_PERIOD_DAYS=60
CURRENT_LOCATION="Bangalore"
MAX_JOBS_PER_RUN=500
ENABLE_SALARY_UPDATE=true

OPENAI_API_KEY=your_key   # optional

▶️ How to Run Each Script
1. Refresh Resume + Apply Recommended Jobs
python job_agent.py

2. Apply Using Intelligent Filtering
python job_apply.py

3. Update Salary + Apply Jobs (Advanced)
python job_update.py

4. Only Update Salary
python update_salary.py

⚙️ Cron Automation (Optional)

Run everyday at 9 AM:

0 9 * * * /usr/bin/python3 /path/to/job_agent.py

📌 Notes / Recommendations

Make sure popup blockers are disabled.

Keep Chrome logged in for smoother automation.

Avoid running all scripts too frequently → Naukri may block temporary access.

Salary +1 trick is optional but boosts visibility.