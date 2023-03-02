from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path="chromedriver.exe")

driver.get("https://omayo.blogspot.com/")

#sleep for 2 seconds
time.sleep(2)

#click on the link to get popup
popup_link = driver.find_element("xpath", '//*[@id="HTML37"]/div[1]/p/a').click()

#get instance of first pop up  window
whandle = driver.window_handles[1]

#switch to pop up window
driver.switch_to.window(whandle)

#get text of a element in pop window
print(driver.find_element("id","para1").text)

#sleep for 1 second
time.sleep(1)
# driver.get("https://quillbot.com/")


# #prints parent window title
# print("Parent window title: " + driver.title)

# #get current window handle
# # p = driver.current_window_handle
# driver.find_element(By.ID,'inputText').send_keys("The list items will be numbered with numbers (default)")
# time.sleep(3)
# driver.find_element(by=By.XPATH, value='//*[@id="outputBottomQuillControls-default"]/div/div/div/div/div/div[2]/div/div/div/div/button/div')
# p = driver.current_window_handle
# parent = driver.window_handles[0]
# chld = driver.window_handles[1]
# time.sleep(5)
# driver.switch_to.window(chld)
# driver.close()

# time.sleep(20)

# driver.close()


