from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from .models import ContactInfo

import re
import requests


def driver_init():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options = options ,executable_path='C:\geckodriver\geckodriver.exe')
    return driver


def parse():
    for k in range(0, 5):
        driver = driver_init()
        driver.get('https://www.olx.ua/')
        wait = WebDriverWait(driver, 10)
        main_page_ads_element = wait.until(EC.presence_of_element_located((By.ID, 'mainpageAds')))
        main_page_ads_html = main_page_ads_element.get_attribute('innerHTML') 
        b = driver.find_element_by_id('mainpageAds')
        soup = BeautifulSoup(main_page_ads_html, 'html.parser')
        a = soup.find_all('a')
        obyavleniya = list()
        for link in a:
            if 'obyavlenie' in link.get('href'):
                if not link.get('href') in obyavleniya:
                    obyavleniya.append(link.get('href'))
        for single_page in obyavleniya:
            driver.get(single_page)
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@data-rel='phone']")))
            except:
                continue
            try:
                button = driver.find_element_by_xpath("//div[@data-rel='phone']")
                button.click()
            except:
                continue
            name1 = driver.find_element_by_class_name("offer-user__details").text
            name = re.split(r'\n', name1)
            if 'показать' or 'xxx' in button.text:
                try:
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@data-rel='phone']")))
                    button.click()
                except:
                    continue
            if '\n' in button.text:
                button2 = re.split('\n', button.text)
                for q in button2:
                    ContactInfo.objects.get_or_create(contact_name=name[0], 
                                                    phone_number=button.text)
            else:
                ContactInfo.objects.get_or_create(contact_name=name[0],
                                                phone_number=button.text)       
            print(' + ')
        print('end')
        
        driver.quit()
        

#/html/body/div[2]/section/div[3]/div/div[1]/div[2]/div/div[2]/div[2]/h4/a
#/html/body/div[2]/section/div[3]/div/div[1]/div[2]/div/div[3]/div/div/h4/a
#/html/body/div[2]/section/div[3]/div/div[1]/div[2]/div/div[4]/div[2]/h4/a
#/html/body/div[2]/section/div[3]/div/div[1]/div[2]/div/div[5]/div[2]/h4/a
#/html/body/div[2]/section/div[3]/div/div[1]/div[2]/div/div[3]/div[2]/h4/a
#search_name = driver.find_element_by_css_selector('#offeractions > div:nth-child(5) > div.offer-user__details > h4 > a')
#print(search_name)
#driver.find_element_by_xpath('//a[@href="https://"]')
#continue_link = driver.find_element_by_partial_link_text('https://www.')
#Закрытие фичи про куки:
#element_2 = wait.until(EC.element_to_be_clickable((By.XPATH,'//[@id="cookiesBar"]/a')))
#cookies = driver.find_element_by_xpath('//[@id="cookiesBar"]/a')
#cookies.click()
#except(ElementNotVisibleException, NoSuchElementException, TimeoutException):
#with open('phones.txt', 'a') as f:
#        for item in z:
#            f.write("%s\n" % item)