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
# time.sleep(10)
import mysql.connector

def Quilled_Data_Process(content,soup):
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
            print("status = 1")
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
    print(mycursor.rowcount, "record fetched.")
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
    timeout = 40
    try:
        myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//button/div[text()="Rephrase"]')))
        print("paraphrase Page is ready!")
    except TimeoutException:
        print("4Loading took too much time!")
    copy_content = Driver.find_element(By.XPATH,value="//span[@id='editable-content-within-article']").text
    print("======== Quil Successfully ==========")
    time.sleep(10)
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

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    ##################### Data Base ##############################
    mydb = mysql.connector.connect(
        host="3.140.57.116",
        user="wp_raj1",
        password="rajPassword95$",
        database="automation00"
    )
    ########################## Login Process ##########################
    Quil_Login(driver)
    ##################### Get Data From Data Base #####################
    print("=============== Get Data From Database =============")
    alll = get_from_database(mydb)
    mycursor = mydb.cursor()
    count=0
    for x in alll:
        print(len(x))
        print(x[2])
        print("send2",x[0],x[1],x[3])
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
        except Exception as e:
            print("Error ==",e)  
            time.sleep(120) 
            driver.quit()
            Quil_Login(driver)

            continue

        ######################### Send Quil Content to  Data Base #################

        process_status = Quilled_Data_Process(content,soup)
        if process_status != False:
            print(" ======== All Processing Complated ========")
            count+=1
        else:
            break    

    driver.quit()