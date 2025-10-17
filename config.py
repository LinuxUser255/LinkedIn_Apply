# General bot settings

# Chrome-only
browser = ["Chrome"]

# Optional: run in headless mode (background)
headless = False

# LinkedIn login creds (optional if using CHROME_PROFILE_PATH in .env)
email = ""
password = ""

# These settings are for running Linkedin job apply bot
LinkedinBotProPassword = ""

# Location(s) for job search - examples:
# ["Poland", "Singapore", "New York City Metropolitan Area", "Monroe County"]
# Continent shortcuts: ["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa"]
location = ["United States"]

# Keywords related to your job search
keywords = ["Penetration Tester", "Web App Penetration Tester", "API Security", "Cybersecurity", "BurpSuite", "Linux", "Mobile App Security", "Network Security", "Operating System Security"]

# Job experience Levels - e.g.: ["Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
experienceLevels = ["Entry level", "Mid-Senior level"]

# Years of experience - e.g.: ["1-3 years", "3-5 years", "5+ years"]
yearsOfExperience = ["5+ years"]

# Date posted - choose one: ["Any Time", "Past Month", "Past Week", "Past 24 hours"]
datePosted = ["Any Time"]

# Job type(s) - e.g.: ["Full-time", "Part-time", "Contract", "Temporary", "Volunteer", "Intership", "Other"]
jobType = ["Full-time", "Contract"]

# Workplace type(s): ["On-site", "Remote", "Hybrid"]
remote = ["Remote"]

# Salary preference - choose one label from the list in utils.salary()
salary = ["$100,000+"]

# Sort - choose one: ["Recent"] or ["Relevent"]
sort = ["Recent"]

# Blacklist companies you do not want to apply to
blacklist = ["NetSpi"]

# Blacklist keywords in title
blackListTitles = []

# Only apply to these companies (leave empty for all)
onlyApply = []

# Only apply to titles having these keywords (leave empty for all)
onlyApplyTitles = ["Penetration Tester", "Web App Penetration Tester", "API Security", "Cybersecurity"]

# Follow companies after successful application: True/False
followCompanies = False

# Your country code for the phone number - ex: 'us'
country_code = "us"

# Your phone number without identifier - ex: 123456789
phone_number = ""
