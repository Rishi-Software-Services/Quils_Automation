from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# time.sleep(10)

def Paraphrase_Soup(Driver,New_text):
    delay = 10 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,"//div[@id='inputText']")))
            #print("Page is ready!")
    except TimeoutException:
        print("3Loading took too much time!")

    Text_paste = Driver.find_element(By.XPATH,value="//div[@id='inputText']").clear()
    Text_paste.send_keys(New_text)
    button_press = Driver.find_element(By.XPATH,value='//div[@class="css-0"]').click()
    timeout = 40
    try:
        myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-0"][text()="Rephrase"]')))
        print("paraphrase Page is ready!")
    except TimeoutException:
        print("4Loading took too much time!")
    copy_content = Driver.find_element(By.XPATH,value="//span[@id='editable-content-within-article']").text
    print(copy_content)
    print("======== Quil Successfully ==========")
    


def Quil_Login(Driver):
    print("========== Login Process ==============")

    ################## User Name and PassWord #############

    UserName = "rajan@grimbyte.com"
    PassWord = "Grimbyte123."

    ################### Login Process ######################
    Driver.get("https://quillbot.com/login")

    delay = 30
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='mui-3']")))
    except TimeoutException:
        print("1Loading took too much time!")
    Input_user = driver.find_element(by=By.XPATH, value="//input[@id='mui-3']")
    Input_user.send_keys(UserName)    
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='mui-4']")))
    except TimeoutException:
        print("1Loading took too much time!")

    Input_pass = driver.find_element(by=By.XPATH, value="//input[@id='mui-4']")
    Input_pass.send_keys(PassWord)

    Click_login_button = driver.find_element(By.XPATH,value="//button[normalize-space()='Log In']")
    Click_login_button.click()
    time.sleep(10)
    print("======= Login Successfully =======")

    

if "__main__" == __name__:
    print('======== Start QuilBot Proccess ========')

    ########################## Driver Settings ####################

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

    ####################### Add On Driver Path #####################
    driver_path=r'/usr/bin/chromedriver'
    # driver=webdriver.Chrome(options=chrome_options,executable_path="chromedriver.exe")
    # driver = webdriver.Chrome(options=chrome_options
    s = Service(driver_path)

    driver = webdriver.Chrome(options=chrome_options, service=s)
    options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    ##################### Quil Login Proccess #####################
    Quil_Login(driver)

    #################### Paraphase Processing #####################
    Str1 = "The group took a five-year pause after receiving the highest praise for “Is This It,” and then they released their fourth album, “Angles,” in 2011. The group released “Comedown Machine” in 2013, which served as their final record under their agreement with longstanding label RCA, and then in 2016, they released an EP called “Future Present Past” on Casablancas’ own label Cult Records."
    Paraphrase_Soup(driver,Str1)
    driver.quit()


