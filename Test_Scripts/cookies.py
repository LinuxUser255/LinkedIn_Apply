# EXTRA
# In case using session cookies are needed in the future,(maintaing a session)
# Here is some boilerplate code for that

# Stay logged in until user closes the browser, store cookies
#cookies = browser.get_cookies()
#with open('data/cookies.json', 'w', encoding="utf-8") as file:
#    for cookie in cookies:
#        file.write(f"{cookie['name']}={cookie['value']}\n")

#with open('data/cookies.json', 'r', encoding="utf-8") as file:
#    cookies = [cookie.strip().split("=") for cookie in file]
#    for cookie in cookies:
#        self.driver.add_cookie({
#            'name': cookie[0],
#            'value': cookie[1],
#            'domain': '.linkedin.com'
#        })
#
#    # add cookies to the seleium session
#    for cookie in cookies:
#        driver.add_cookie({})
#
#    # Verify cookie persistence
#    driver.get('https://www.linkedin.com/jobs/')
#    assert driver.title == 'LinkedIn'
