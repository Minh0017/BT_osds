from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
import re
import sqlite3
all_links =[] 
musician_links=[]
# 0. Tạo cơ sở dữ liệu
nsi = sqlite3.connect('musicians.db')
c = nsi.cursor()
try:
    c.execute('''
        CREATE TABLE painter (
            id integer primary key autoincrement,
            name_of_the_band text,
            year_active text
            
        )
    ''')
except Exception as e:
    print(e)
def add(name_of_the_band, year_active):
    nsi = sqlite3.connect('musicians.db')
    c = nsi.cursor()
    # Them vao co so du lieu
    c.execute('''
        INSERT INTO painter(name_of_the_band, year_active)
        VALUES (:name_of_the_band, :year_active)
    ''',
      {
          'name_of_the_band': name_of_the_band, 
        'year_active': year_active,
      })
    nsi.commit()
    nsi.close()
# url
driver = webdriver.Chrome()
url = "https://en.wikipedia.org/wiki/Lists_of_musicians#A"
    
try:
        #mo trang web
        driver.get(url)
        #doi khoang chung 3s
        sleep(3)
        #lay ra tat ca the ul
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        #chon ul thu 22
        ul_painters = ul_tags[21] #dem tu 0
        #lay tat ca the <li> thuoc ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
        # #tao danh sach cac url
        links = [tag.find_element(By.TAG_NAME,"a").get_attribute("href") for tag in li_tags]
        for x in links:
            all_links.append(x)
        #tao danh sach cac title
        titles = [tag.find_element(By.XPATH, "//div[contains(@class,'div-col')]").get_attribute("title") for tag in li_tags]
except:
        print("Error!")
#tat man hinh
driver.quit()
artists_driver = webdriver.Chrome()
artists_driver.get(all_links[0])

sleep(3)
try:
    #lấy tất cả các the ul của list of acid rock artists
    ul_artists_tags = artists_driver.find_elements(By.TAG_NAME, "ul")
    print(len(ul_artists_tags))

    #chọn ul thứ 25
    ul_artist = ul_artists_tags[24]
    #lấy tất cả link chứa thông tin thuộc artists
    li_artist = ul_artist.find_elements(By.TAG_NAME, "li")
    print(len(li_artist))

    # tạo danh sách các url của artist
    links_artist = [artist_tag.find_element(By.TAG_NAME,"a").get_attribute("href") for artist_tag in li_artist]
    for x in links_artist:
        musician_links.append(x)
except Exception as e:
    print(f"Error!!:{e}")
artists_driver.quit()

count = 0
for link in musician_links:
    # if(count >= 2):
    #     break
    # count += 1
    
    try:
        #khoi tao webdriver
        driver = webdriver.Chrome()
        #mo trang
        url = link
        driver.get(url)
        sleep(2)
        #lay ten nhac si/ban nhac
        try:
            name_of_the_band = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name_of_the_band = ""

        #lay năm hoat dong
        try:
            year_element = driver.find_element(By.XPATH, value='//span[contains(text(),"Years active")]/parent::*/following-sibling::td')
            year_active = year_element.text
            
        except:
            year_active = ""
        add(name_of_the_band, year_active)
        
    except Exception as e:
        print(f'error: {e}')

        
