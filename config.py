# General bot settings

# Some of the following, are general template/examples, edit according to your needs.
browser = ["Chrome"]

# Optional! run browser in headless mode, no browser screen will be shown it will work in background.
headless = True

# Linkedin login creds
email = ""
password = ""

# These settings are for running Linkedin job apply bot
LinkedinBotProPassword = ""

# location you want to search the jobs - ex : ["Poland", "Singapore", "New York City Metropolitan Area", "Monroe County"]
# continent locations:["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa", "Australia"]
location = ["United States"]

# keywords related with your job search
keywords = ["lead developer", "chief technical officer", "cto", "python"]

#job experience Level - ex:  ["Internship", "Entry level" , "Associate" , "Mid-Senior level" , "Director" , "Executive"]
experienceLevels = ["Entry level", "Mid level"]

#job posted date - ex: ["Any Time", "Past Month" , "Past Week" , "Past 24 hours"] - select only one
datePosted = ["Past 24 hours"] 

#job type - ex:  ["Full-time", "Part-time" , "Contract" , "Temporary", "Volunteer", "Intership", "Other"]
jobType = ["Full-time", "Part-time", "Contract"]

#remote  - ex: ["On-site" , "Remote" , "Hybrid"]
remote = ["Remote"]

#salary - ex:["$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", "$140,000+", "$160,000+", "$180,000+", "$200,000+" ] - select only one
salary = ["100,000"]

#sort - ex:["Recent"] or ["Relevent"] - select only one
sort = ["Recent"]

#Blacklist companies you dont want to apply - ex: ["Apple","Google"]
blacklist = ["EPAM Anywhere"]

#Blaclist keywords in title - ex:["manager", ".Net"]
blackListTitles = ["", "", ""]

#Only Apply these companies -  ex: ["Apple","Google"] -  leave empty for all companies
onlyApply = [""]

#Only Apply titles having these keywords -  ex:["web", "remote"] - leave empty for all companies
onlyApplyTitles = ["programming", "remote", "Penetration Tester", "Application Security"]

#Follow companies after sucessfull application True - yes, False - no
followCompanies = False

# your country code for the phone number - ex: fr
country_code = ""

# Your phone number without identifier - ex: 123456789
phone_number = ""
