from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import re
import os
import logging
import mysql.connector

def Quilled_Data_Process(content,soup,mydb,count,x):
    mycursor = mydb.cursor()
    quilled_text=content.split('\n\n\n')

    out_tagaaa = {}
    key_list=[]
    value_list12=[]
    p=soup.findAll() 
    for tag in p:
        if(tag.name=="a" and tag.has_attr('href')):
            value_list12.append(tag['href'])
            key_list.append(tag.text)
    out_tagaaa.clear() 
    for key, value in zip(key_list, value_list12):
        if key=="":
            continue
        # elif 'a href="http' in value and "rel" not in value:
        #     ind = value.index('>',0)
        #     value = value[:ind-1]+'" rel="noopener nofollow'+value[ind-1:]
        #     out_tagaaa[key] = value
        # elif 'a href="http' in value and 'rel="tag"'  in value:
        #     continue
        else:
            out_tagaaa[key] = value
    # print(out_tagaaa)
    i=-1
    j=0
    flag=1
    for tag in p:
        i+=1
        if(tag.name=="script"):
                tag.decompose()
        if(tag.name=="script"):
                continue
        if(tag.name=='p'):
            if(tag.findParent().name=='blockquote'):
                continue
            if(len(tag.findChildren('p'))>0):
                continue
            if(tag.text=='' or tag.get_text(strip=True)==''):
                continue
            #newtext=newtext + tag.text + "\n\n\n"
            #newtext[i]=tag.find(text=True, recursive=False)
            try:
                p[i].string=quilled_text[j]
                j+=1


            except IndexError:
                mycursor.execute("update bulk_feed_content set content_modify=%s,status=0 where bfc_id=%s", (str(soup),x[0]))
                mydb.commit()
                print("exception")
                time.sleep(2)
                flag=0
                break

    print("The End")

    new_article1=str(soup)
    for word, link in out_tagaaa.items():
        if word in new_article1:
            if "youtube" in link:
                new_link = f"<a href='{link}' >{word}</a>"
            else:
                new_link = f"<a href='{link}' rel='noopener nofollow'>{word}</a>"
            new_article1 = new_article1.replace(word, new_link, 1)

    if flag==1:
        try:
            mycursor.execute("update bulk_feed_content set content_modify=%s,status=1 where bfc_id=%s", (new_article1,x[0]))
            Success_log.info("Content SeccessFully Quil status=1 where bfc_id=%s", (x[0]))
        except:
            mycursor.execute("update bulk_feed_content set content_modify=%s,status=0 where bfc_id=%s", (None,x[0]))
            print("Status = 0") 
        mydb.commit()
          
    if count==50:
        return False 

def get_from_database(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM destination_website where status = 1 ")
    myresult = mycursor.fetchall()
    listt=[]
    for des_id in myresult:
        listt.append(des_id[0])
    # print(listt)
    bfw_li=[]
    for des in listt:
        mycursor.execute("SELECT * FROM bulk_feed_website where des_id=(%s)" %  (des))
        websites = mycursor.fetchall()
        bfw_li.extend(websites)
    alll=[]
    for bfw_idd in bfw_li:
        mycursor.execute("SELECT * FROM bulk_feed_content where bfw_id=(%s) and status is Null " % (bfw_idd[0]) )
        webs = mycursor.fetchall()
        alll.extend(webs)
    #//div[5]/div[3]/div/div[1]/button/svg
    # print(mycursor.rowcount, "record fetched.")
    print("Record Fetched. =", len(alll))
    return alll

def find_replacement(m,out_tagaaa):
    return out_tagaaa[m.group(1)]

def remove_non_ascii_1(data):
    return ''.join([i if ord(i) < 128 else ' ' for i in data])

def Paraphrase_Soup(Driver,New_text):
    print("========== ParaPhrase Proccess ============")
    Driver.refresh()
    time.sleep(10)
    delay = 30 # seconds
    try:
        myElem = WebDriverWait(Driver, delay).until(EC.presence_of_element_located((By.XPATH,"//div[@id='inputText']")))
        print("get xpath")
            #print("Page is ready!")
    except TimeoutException:
        print("3Loading took too much time!")

    try:
        Text_paste = Driver.find_element(By.XPATH,value="//div[@id='inputText']").clear()
    except:
        pass    

    Text_paste = Driver.find_element(By.XPATH,value="//div[@id='inputText']")
    Text_paste.send_keys(New_text)
    delay = 20 # seconds
    try:
        button_press = WebDriverWait(Driver, delay).until(EC.presence_of_element_located((By.XPATH,"//div[@class='css-0']")))
        button_press.click()
    except TimeoutException:
        print("3Loading took too much time!")
    timeout = 80
    try:
        myElem = WebDriverWait(Driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//button/div[text()="Rephrase"]')))
        print("paraphrase Page is ready!")
    except TimeoutException:
        print("4Loading took too much time!")
    copy_content = Driver.find_element(By.XPATH,value="//span[@id='editable-content-within-article']").text
    print("======== Quil Successfully ==========")
    time.sleep(30)
    return copy_content

def process_soup(soup):
    # global out_tag
    """ def findchild(tag):
        print(tag.name)
        if(len(tag.findChildren())>0):
            for childtag in tag.findAll():
                findchild(childtag)

    for tag in soup.findAll(recursive=False):
        findchild(tag)
    """

    # key_list=[]
    # value_list=[]
    for tag in soup.findAll():
        # if(tag.name=="img"):
        #     tag.decompose()
        if(tag.name=="script"):
                tag.decompose()
        if(tag.name=="script"):
                continue
    #     if(tag.name=="a" and tag.has_attr('href')):
    #         value_list.append(str(tag))
    #         key_list.append(tag.text)
    # out_tag.clear()
    # for key, value in zip(key_list, value_list):
    #     out_tag[key] = value
        # if(tag.name=="img"):
        #     tag.decompose()
        # if(tag.name=="a" and tag.has_attr('href')):
        #     if('twitter' in tag['href'] or 'instagram' in tag['href'] or 't.co' in tag['href']):
        #         continue
        #     tag.parent.a.unwrap()
        # if(tag.name=='li'):
        #     if(len(tag.findChildren('a'))>0):
        #         tag.decompose()
    p=soup.findAll()
    newtext=[None]*len(p)
    i=-1
    for tag in p:
        i+=1
        if(tag.name=="script"):
                tag.decompose()
        if(tag.name=="script"):
                continue
        if(tag.name=='p'):
            if(tag.findParent().name=='blockquote'):
                continue
            if(len(tag.findChildren('p'))>0):
                continue
            if(tag.text=='' or tag.get_text(strip=True)==''):
                continue
            #newtext=newtext + tag.text + "\n\n\n"
            #newtext[i]=tag.find(text=True, recursive=False)
            newtext[i]=tag.get_text(strip=True)

    #list=[str(newtext.index(x))+"."+x for x in newtext if x is not None and x is not '']
    list=[x for x in newtext if x != None and x != '']
    print("quilling p count:",len(list))
    str1=""
    for ele in list:
        str1 += ele + "\n\n\n"
    print("word count:-",len(str1.split()))
    
    return str1

def Quil_Login(Driver):
    print("========== Login Process ==============")

    ################## User Name and PassWord #############

    UserName = "rajan@grimbyte.com"
    PassWord = "Grimbyte123."

    ################### Login Process ######################
    Driver.get("https://quillbot.com/login")

    delay = 30
    try:
        myElem = WebDriverWait(Driver, delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='mui-3']")))
    except TimeoutException:
        print("1Loading took too much time!")
    Input_user = Driver.find_element(by=By.XPATH, value="//input[@id='mui-3']")
    Input_user.send_keys(UserName)    
    try:
        myElem = WebDriverWait(Driver, delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='mui-4']")))
    except TimeoutException:
        print("1Loading took too much time!")

    Input_pass = Driver.find_element(by=By.XPATH, value="//input[@id='mui-4']")
    Input_pass.send_keys(PassWord)

    Click_login_button = Driver.find_element(By.XPATH,value="//button[normalize-space()='Log In']")
    Click_login_button.click()
    time.sleep(30)
    print("======= Login Successfully =======")

def Driver_settings(driver_path):    
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
    s = Service(driver_path)
    driver = webdriver.Chrome(options=chrome_options, service=s)
    options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return driver

def main(mydb):

    ############################################

    driver = Driver_settings(Chrome_driver_path)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    ##################### Get Data From Data Base #####################
    print("=============== Get Data From Database =============")
    alll = get_from_database(mydb)
    if len(alll) == 0:
        Success_log.info("=========== No Record Get ========")
        print("zero record get")
        return True
    ########################## Login Process ##########################
    try:
        Quil_Login(driver)
        Success_log.info(" =========== Quil_Bot Successfully login ============")
    except Exception as be:
        Error_log.exception(be)    
    
    mycursor = mydb.cursor()
    count=0
    for x in alll:
        
        if x[4] is None or x[5] is None:
            mycursor.execute("update bulk_feed_content set status=0 where bfc_id=%s"% (x[0]))
            mydb.commit()
            continue
        print(len(x))
        print(x[2])
        print("send2",x[0],x[1],x[-2],x[3])
        mycursor.execute("SELECT * FROM Total_posts where Destination_id=(%s)" %  (x[11]))
        total_quill_all = mycursor.fetchall()[-1][3]

        print("all",total_quill_all)

        newdata=remove_non_ascii_1(x[4])

        soup = BeautifulSoup(newdata, 'html.parser')

        str1=process_soup(soup)
        # print(out_tag)
        if(len(str1.split())>1600):
            print(" =======  Article Is Long =======")
            mycursor.execute("update bulk_feed_content set content_modify=%s,status=0 where bfc_id=%s", (None,x[0]))
            mydb.commit()
            continue
        try:
            content= Paraphrase_Soup(driver,str1)
        except Exception as ae:
            Error_log.exception(ae)  
            time.sleep(10)
            driver.quit()
            os.system("pkill chrome")
            time.sleep(120)
            return False

        ######################### Send Quil Content to  Data Base #################
        try:
            process_status = Quilled_Data_Process(content,soup,mydb,count,x)
        except Exception as ce:
            Error_log.exception(ce)     
        if process_status != False:
            print(" ======== All Processing Complated ========")
            count+=1
        else:
            return True
    return True

################ Loges File Settings ##############
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

Script_Path = os.path.dirname(os.path.abspath(__file__))
log_files = os.path.join(Script_Path,"logs_file")
if not os.path.exists(log_files):
    os.mkdir(log_files)

Error_file = os.path.join(log_files,"Error_.log")
Success_file = os.path.join(log_files,"Successful_Quil.log")

#################### Logs Files ###################
Error_log = setup_logger("Error_files",Error_file)
Success_log = setup_logger("Successful_files",Success_file)


if "__main__" == __name__:
    print('======== Start QuilBot Proccess ========')

    ################### Driver #########################

    Chrome_driver_path = "/usr/bin/chromedriver"

    ##################### Data Base ##############################
    # mydb = mysql.connector.connect(
    #     host="3.140.57.116",
    #     user="wp_raj1",
    #     password="rajPassword95$",
    #     database="automation00"
    # )

    ####################################################
    while True:
        while True:
            try:
                ################ Data Base #################
                mydb = mysql.connector.connect(
                    host="3.140.57.116",
                    user="wp_raj1",
                    password="rajPassword95$",
                    database="automation"
                )

                driver = main(mydb)
                if driver == True:
                    break
                mydb.close()
            except Exception as e:
                Error_log.exception(e)
            time.sleep(122)
