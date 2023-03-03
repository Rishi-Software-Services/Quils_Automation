from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--user-agent={customUserAgent}")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
driver=webdriver.Chrome(options=chrome_options,executable_path="chromedriver.exe")
# driver = webdriver.Chrome(options=chrome_options

options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


driver.get("https://quillbot.com/login")

time.sleep(15)
# Input_area = driver.find_element(by=By.XPATH, value="class='MuiFilledInput-input'")

# Input_area.send_keys("hello")

Input_area = driver.find_element(by=By.XPATH, value="//*[@id='mui-3']")
Input_area.send_keys("rajan@grimbyte.com")

Inputa_area = driver.find_element(by=By.XPATH, value="//*[@id='mui-4']")
Inputa_area.send_keys("Grimbyte123.")

Inputb_area = driver.find_element(by=By.XPATH, value="//*[@id='loginContainer']/div/div[5]/button")
Inputb_area.click()
# print(driver.page_source)
time.sleep(10)
print("SuccessFully Login")
driver.quit()