from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
PATH ="C:/Users/ddkil/OneDrive/שולחן העבודה/תוכנות/chromedriver.exe"

driver = webdriver.Chrome(PATH)

driver.get("https://tasty.co/")
search = driver.find_element_by_id("search-desktop")
search.send_keys("eggs garlic")
search.send_keys(Keys.RETURN)
time.sleep(5)
driver.quit()
