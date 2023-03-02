from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_options = Options()
chrome_options.add_argument("--user-agent={customUserAgent}")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")

driver_path=r'/usr/bin/chromedriver'
# driver=webdriver.Chrome(options=chrome_options,executable_path="chromedriver.exe")
# driver = webdriver.Chrome(options=chrome_options
s = Service(driver_path)

driver = webdriver.Chrome(options=chrome_options, service=s)

options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


driver.get("https://www.pelhamplus.com/")

print(driver.title)

driver.quit()