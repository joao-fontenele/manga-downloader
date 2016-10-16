import time
from selenium import webdriver

#driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')  # Optional argument, if not specified will search path.
driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/xhtml');
#driver.get('http://bato.to/reader#32ebe1a658eabee9');
time.sleep(2) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
