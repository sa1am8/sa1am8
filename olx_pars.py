from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re
import requests
import simplejson



options = Options()
options.add_argument('--headless')
quantity = 1


while not quantity == 10:
    z = list()
    r = requests.get('https://www.olx.ua/') 
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find_all('a', attrs = {'href': re.compile('https://www')})
    obyavleniya = list()
    for link in a:
        if 'obyavlenie' in link.get('href'):
            if not link.get('href') in obyavleniya:
                obyavleniya.append(link.get('href'))
    driver = webdriver.Firefox(options = options, executable_path='C:\geckodriver\geckodriver.exe')
    for single_page in obyavleniya:
        driver.get(single_page)
        wait = WebDriverWait(driver, 10)
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
        if '\n' in button.text:
            button2 = re.split('\n', button.text)
            for q in button2:
                z.append(q)
                z.append(name[0])
        else:
            z.append(button.text)
            z.append(name[0])
        print(' + ')
    print(z)
    with open('phones.txt', 'a') as f:
        for item in z:
            f.write("%s\n" % item)
    quantity += 1

   
    driver.quit()
    print('end')



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

