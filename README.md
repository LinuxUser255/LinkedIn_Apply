# LinkedIn_Apply

## A Python bot that will apply to the, "Easy Apply", jobs based on your preferences.

- I may be adding Streamlit and Ollama at somepoint. Therefore, they are in the requirements.txt

- This repo/codebase is a work in progress, & is intended to be an updated version of [my other linkedin bot](https://github.com/LinuxUser255/linkedin-application-bot)

<br>


## You will need to download the [Chrome Driver](https://googlechromelabs.github.io/chrome-for-testing/#stable) and palce it in the directory alongside the python files
https://googlechromelabs.github.io/chrome-for-testing/#stable

<br>

# TO DO - Fixes and Changes 

**In order of most to least important**

**Browser handling issues**
- [x] Eliminate launching a new browser/login session with each iteration.
- [x] Each URL is being visited in the same window
- [x] Conduct all searches and applications within one browser session.

<br>

**Completing the Easy apply section**
- [x] Resolve the click on "Easy apply" button: Works in `click_button_test.py`

- [ ]  Create functionality to handle the submit apply pop-up. 
	- [ ]  Filling the three fields, 
	- [ ] selecting your resume, 
	- [ ] clicking submit application and 
	- [ ] close the thank you for applying pop up, and repeat

- [ ] Integrate the four methods used to click the Easy Apply button into `linkedin.py`
  - [ ] _Do this using a nested function??_


- [ ] Tie it all together in `main.py`


<br>

  **After all of the Easy apply functionality is complete.
- [ ] Make bot able to apply on external links
- [ ] Make it able to register & logon to external job applications

<br>

  **Misc..**
- [x] Follow PEP 8 Syle Guide coding conventions:
- [x] Change all Variable and Function names to lower case
- [x] Avoid account login issues
- [x] Headless browser experience (Only the login and home page is shown. No link visitin.)
- [x] You can change this in the `config.py` file. Where it says `headless = True`

<br>

**Other**
- [x] Fix specified HTML element discovery issues
- [x] ~~Chromium not woking properly with Linux~~
- [ ] More robustness of the bot for different fields
- [ ] Add support to other major job seeking websites (Glassdoor, AngelCo, Greenhouse,
- [ ] Possibly need? Evade Anti-Bot detection
- [ ] If necessary, Maybe retrieve and use session cookies from the browser?

<br>

## Install & use

### Clone the repository & Install the requirments**
```shell

git clone https://github.com/LinuxUser255/LinkedIn_Apply.git

cd LinkedIn_Apply
```
<br>

#### Download & Activate the virtual enviroment
```shell
curl -LO https://raw.githubusercontent.com/LinuxUser255/LinkedIn_Apply/refs/heads/main/virtenv_acitvate.sh | sh virtenv_acitvate.sh 
```

<br>

### the install pip3 requirements
```shell
pip3 install -r requirements.yml
```
<br>

### The bot can run either by executing `main.py` or `linkedin.py`. Both ways work.**

<br>

