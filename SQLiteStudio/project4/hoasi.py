from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains,ScrollOrigin
from time import sleep
import re
import sqlite3



######################################################
# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('painters.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE painter (
            id integer primary key autoincrement,
            name text,
            birth text,
            death text,
            nationality text
        )
    ''')
except Exception as e:
    print(e)

def them(name, birth, death, nationality):
    conn = sqlite3.connect('painters.db')
    c = conn.cursor()
    # Them vao co so du lieu
    c.execute('''
        INSERT INTO painter(name, birth, death, nationality)
        VALUES (:name, :birth, :death, :nationality)
    ''',
      {
          'name': name,
          'birth': birth,
          'death': death,
          'nationality': nationality,
      })
    conn.commit()
    conn.close()

######################################################
# I. Tai noi chua links vaf Tao dataframe rong
all_links = []
######################################################
# II. Lay ra tat ca duong dan de truy cap den painters
# Khởi tạo Webdriver
driver= webdriver.Chrome()



for i in range(70, 71):
    # Khởi tạo driver
    driver = webdriver.Chrome()
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22"+chr(i)+"%22"
    try:

        # Mở trang
        driver.get(url)

        # Đợi một chút để trang tải
        sleep(3)

        # Lay ra tat cac ca the ul
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        # print(len(ul_tags))

        # Chon the ul thu 21
        ul_painters = ul_tags[20]  # list start with index=0

        # Lay ra tat ca the <li> thuoc ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # Tao danh sach cac url
        links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        for x in links:
            all_links.append(x)
    except:
        print("Error!")

    # Dong webdrive
    driver.quit()

######################################################
# III. Lay thong tin cua tung hoa si
count =0;
for link in all_links:
    # if (count>3):
    #     break
    # count=count+1;

    # print(link)
    try:
        # Khoi tao webdriver
        driver = webdriver.Chrome()
        # Mo trang
        url = link
        driver.get(url)

        # Doi 2 giay
        sleep(2)

        # Lay ten hoa si
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""
        # Lay ngay sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            
            birth = re.findall(r'\d{1,2} [A-Za-z]+ \d{4}|\d{4}', birth_element.text)[0]
        except:
            birth = ""
        # Lay ngay mat
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            
            death = re.findall(r'\d{1,2} [A-Za-z]+ \d{4}|\d{4}', death_element.text)[0]
        except:
            death = ""
        # Lay ngay mat
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = ""

        them(name,birth, death, nationality)

        # Dong web driver
        driver.quit()
    except Exception as e:
        print(e)

