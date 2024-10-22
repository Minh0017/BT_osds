from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

import re
driver = webdriver.Chrome()


# Tạo url
url = 'http://pythonscraping.com/pages/javascript/ajaxDemo.html'

# Truy cập
driver.get(url)

# In ra nội dung của trang web
print("Before: ================================\n")
print(driver.page_source)


# Tạm dừng khoảng 3 giây
time.sleep(3)

# In lai
print("\n\n\n\nAfter: ================================\n")
print(driver.page_source)


# Đóng browser
driver.quit()