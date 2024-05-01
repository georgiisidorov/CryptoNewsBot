import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, StaleElementReferenceException
from urllib3.exceptions import NewConnectionError, MaxRetryError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.service import Service


def cryptonews_selenium_getter():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--no-sandbox')

    browser = webdriver.Chrome(service=Service('/home/ubuntu/Cryptonews_bot/chromedriver'), options=chrome_options)

    # ------------------------------ O  K  X -----------------------------------

    browser.get('https://www.okx.com/support/hc/en-us/sections/360000030652-Latest-Announcements')

    time.sleep(3)
    
    list_of_news = []

    links0 = browser.find_elements(By.XPATH,'//a[@data-monitor="article"]')
    links1 = [link.get_attribute('href') for link in links0]

    for news in links1:
        if 'OKX-will' in news:
            list_of_news.append(news)

    time.sleep(3)

    # -------------------------------- B I N A N C E -----------------------------------

    browser.get('https://www.binance.com/ru/support/announcement/c-48')

    time.sleep(3)
    
    links2 = browser.find_elements(By.XPATH, '//a')
    links3 = [link.get_attribute('href') for link in links2]

    for news in links3:
        if '/ru/support/announcement' in news:
            list_of_news.append(news)

    browser.close()
    browser.quit() 

    # -----------------------------

    with open('/home/ubuntu/Cryptonews_bot/newssaved.txt', 'r') as r:
        newssaved = r.readlines()
        newssaved_list = list(map(lambda x: x.strip('\n'), newssaved))

    a = set(list_of_news).difference(set(newssaved_list))
    a = list(a)

    if a != []:
        with open('/home/ubuntu/Cryptonews_bot/newssaved.txt', 'a') as f:
            for link in a:
                f.write(f'{link}\n')

    return a


