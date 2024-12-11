# simple python selenium "hello world", just to search google

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('http://www.google.com')

search = browser.find_element_by_name('q')
search.send_keys("exemplos de python selenium busca google")
search.send_keys(Keys.RETURN)  # hit return after you enter search text

time.sleep(10)  # wait 10 seconds, so you can see the results

browser.quit()  # close the browser
