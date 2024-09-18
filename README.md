# LinkedIn_Apply

## A Python bot that will apply to the, "Easy Apply", jobs based on your preferences.

- I may be adding Streamlit and Ollama at somepoint. Therefore, they are in the requirements.txt

- This repo/codebase is a work in progress, & is intended to be an updated version of [my other linkedin bot](https://github.com/LinuxUser255/linkedin-application-bot)


- You will need to download the Chrome Driver and palce it in the same directory as the python files/scripts
https://googlechromelabs.github.io/chrome-for-testing/#stable

<br>

# TO DO - Fixes and Changes 

**In order of most to least important**


- [x] Eliminate launching a new browser/login session with each iteration.
- [x] Conduct all searches and applications within one browser session.
- [ ] Add ability to add a custom URL, such as a search you did, and apply to every job in that result
- [ ] If not easy apply, then Make bot able to follow external links
- [ ] Make it able to register & logon to external job applications
- [ ] Apply to the jobs on external sites 
- [x] Follow PEP 8 Syle Guide coding conventions:
- [x] Change all Variable and Function names to lower case
- [x] Avoid account login issues:
- [ ] Possibly need? Evade Anti-Bot detection
- [ ] If necessary, Maybe retrieve and use session cookies from the browser?
- [x] Fix specified HTML element discovery issues
- [x] Chromium not woking properly with Linux
- [x] Headless browser experience (Only the login and home page is shown. No link visitin.)
- [ ] You can change this in the `config.py` file. Where it says `headless = True`
- [ ] More robustness of the bot for different fields
- [ ] Output not completed fields in Linkedin
- [ ] Add support to other major job seeking websites (Glassdoor, AngelCo, Greenhouse, Monster, GLobalLogic, djinni)

<br>

## Install & use

**Clone the repository & Install the requirments**
```shell
git clone https://github.com/LinuxUser255/LinkedIn_Apply.git

cd LinkedIn_Apply
```
<br>

- Create a virtual evniroment, then install the requirements

```shell
pip3 install -r requirements.txt
```
<br>

**- The bot can run either by executing `main.py` or `linkedin.py`. Both ways work.**

<br>
