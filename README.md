

# LinkedIn Job Application Bot


![linkedin-logo-02](https://github.com/user-attachments/assets/8829660c-8021-49a2-951f-241ea62394e4)


**Built with**

![PythonLogo](https://github.com/user-attachments/assets/4c25054e-c5b1-4577-b1cc-35930bc6cae6)    
![SeleniumLoge](https://github.com/user-attachments/assets/cef6469b-8193-41ac-b663-992b2a788c0a)

**[Selenium docs](https://selenium-python.readthedocs.io/)**



<br>



## A Python bot that will apply to the, "Easy Apply", jobs based on your preferences.

- I may be adding Ollama at some point in the future.

- This repo/codebase is a work in progress, & is intended to be an updated version of [my other linkedin bot](https://github.com/LinuxUser255/linkedin-application-bot)

<br>

# Test script:  [test_apply_working_full.py](https://github.com/LinuxUser255/LinkedIn_Apply/blob/main/Test_Scripts/test_apply_working_full.py)


<br>


## You will need to download the [Chrome Driver](https://googlechromelabs.github.io/chrome-for-testing/#stable) and palce it in the directory alongside the python files
**https://googlechromelabs.github.io/chrome-for-testing/#stable**

<br>

# TO DO - Most recent: See [TODO.md](https://github.com/LinuxUser255/LinkedIn_Apply/blob/main/TODO.md)
```
Many of the important ones are complete.
The next thing is integrating much of the test_apply script functionality into linkedin.py
```

**Additional items. Some completed.**

<br>

**Browser handling issues**
- [x] Eliminate launching a new browser/login session with each iteration.
- [x] Each URL is being visited in the same window
- [x] Conduct all searches and applications within one browser session.

<br>

**Primary purpose of the Bot: Completion of the Easy apply section**
- [x] Currently troubleshooting XPath click using:
  
## Try it here: [test_apply_working_full.py](https://github.com/LinuxUser255/LinkedIn_Apply/blob/main/Test_Scripts/test_apply_working_full.py) script
- [ ] Once the above is working, itegrate it's functionality into `linkedin.py`
- [x] Resolve the click on "Easy apply" button: Works in `click_button_test.py`
- [x] Implement separation of concerns for finding and clicking elements
- [x] Create module for testing sign in
- [x] Create a module to test login and apply

- [x]  Create functionality to handle the submit apply pop-up.  
	- [x] clicking Next (submit application) and 
	- [x] click review
	- [x] Modify test_apply.py to be re-run without repeating the login everytime

- [ ] Integrate the four methods used to click the Easy Apply button into `linkedin.py`


- [x] Tie it all together in `main.py`


<br>

  **Cool ideas might try: After all of the Easy apply functionality is complete.**
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
- [x] More robustness of the bot for different fields
- [ ] Much later, maybe add support to other major job seeking websites (Glassdoor, AngelCo, Greenhouse,
- [ ] Possibly need? Evade Anti-Bot detection

<br>

## Installation and Use

### Clone the repository & Install the requirments**
```shell
git clone https://github.com/LinuxUser255/LinkedIn_Apply.git

cd LinkedIn_Apply
```
<br>

## Set up scripts: virtual env and pip3

### To set up a virtual enviroment
```shell
chmod +x virtenv_activate.sh
./virtenv_activate.sh
```
<br>

### Automate pip3 updates and install requirements

```shell
chmod +x update_and_install.sh
./update_and_install.sh
````

<br>

## To run the bot as of now, use: [test_apply_working_full.py](https://github.com/LinuxUser255/LinkedIn_Apply/blob/main/Test_Scripts/test_apply_working_full.py)  


When complete use:

`main.py` 

**OR**

`linkedin.py`.


<br>

