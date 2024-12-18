import requests
import pandas as pd
from bs4 import BeautifulSoup

from random import randint
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

#https://python-adv-web-apps.readthedocs.io/en/latest/scraping3.html
RUTA = 'C:/Users/Vercetto/comedia_chile/'
URL = 'https:/comedypass.online/'

driver = webdriver.Chrome()
driver.get(URL)

time.sleep(10)

for n in range(1):
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    try:
        
        button = driver.find_element(By.CLASS_NAME, "eael_load_more_text")
        button.click()

    except WebDriverException as e:
        print('oops. click failed')
    
    s = randint(5, 5)
    time.sleep(s)

page = driver.page_source   

TICKETERAS = 'tienda'
open(RUTA + 'OUTPUT/URLs.txt', 'w').close()
open(RUTA + 'OUTPUT/URLs_error.txt', 'w').close()

soup = BeautifulSoup(page, 'html.parser')
links = soup.find_all('a')

# Print the links
for link in links:
    pagina_web = link.get('href')
    #tickets = [x for x in pagina_web if('tienda' in x)]

    if 'tienda' in pagina_web:
        file = open(RUTA + '/OUTPUT/URLs.txt', 'a+') 
        file.write(pagina_web + '\n')
        file.close()
        print(pagina_web)
        
    else:
        file = open(RUTA + '/OUTPUT/URLs_error.txt', 'a+') 
        file.write(pagina_web + '\n')
        file.close()



   



