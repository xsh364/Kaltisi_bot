import telegram
import requests
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from bs4 import BeautifulSoup 
from selenium import webdriver
import urllib.request as req
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
API_key='knI%2FsEhuhoIf37FOmsc8uCq6qdcCXaJU9%2BKHEwgtLzMWGJ7A7LtC3w3Z3JvKzcE4cSrxn6reCcJi2FzIcKvKAQ%3D%3D'
 
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver  = webdriver.Chrome("./chromedriver.exe", options = options) 
def covid_num_crawling():
    code = req.urlopen("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%95%EC%A7%84%EC%9E%90")
    soup = BeautifulSoup(code, "html.parser")
    info_num = soup.select("div.status_info em")
    result = info_num[0].string
    return result
 
def covid_news_crawling():
    code = req.urlopen("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%BD%94%EB%A1%9C%EB%82%98")
    soup = BeautifulSoup(code, "html.parser")
    title_list = soup.select("a.news_tit")
    output_result = ""
    for i in title_list:
        title = i.text
        news_url = i.attrs["href"]
        output_result += title + "\n" + news_url + "\n\n"
        if title_list.index(i) == 2:
            break
    return output_result
 
def covid_image_crawling(image_num=5):
    if not os.path.exists("./코로나이미지"):
        os.mkdir("./코로나이미지")
 
    browser = webdriver.Chrome("./chromedriver")
    browser.implicitly_wait(3)
    wait = WebDriverWait(browser, 10)
 
    browser.get("https://search.naver.com/search.naver?where=image&section=image&query=%EC%BD%94%EB%A1%9C%EB%82%98&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=0&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&datetype=1&startdate=&enddate=&gif=0&optStr=d&nq=&dq=&rq=&tq=")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.photo_group._listGrid div.thumb img")))
    img = browser.find_elements_by_css_selector("div.photo_group._listGrid div.thumb img")
    for i in img:
        img_url = i.get_attribute("src")
        req.urlretrieve(img_url, "./코로나이미지/{}.png".format(img.index(i)))
        if img.index(i) == image_num-1:
            break
    browser.close()
 
 
 

token = "5071867858:AAGXM83qMK3JLR6yXzoAVD3GhprZuxRoIKU"
id = "5046503865"
 
bot = telegram.Bot(token)
info_message = '''- 오늘의 확진자 수를 확인하려면 '코로나'를 입력하면 된다.
- 코로나 관련 뉴스를 읽고싶다면 '뉴스'를 입력하도록.
- 마지막으로 코로나 관련 이미지를 확인하려면 '이미지'를 입력하면 확인할 수 있다. '''
bot.sendMessage(chat_id=id, text=info_message)
 
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()
 

def handler(update, context):
    user_text = update.message.text
 
    if (user_text == "코로나"):
        covid_num = covid_num_crawling()
        bot.send_message(chat_id=id, text='''오늘의 확진자수는 {}명이다. 
박사또한 방역수칙을 잘 지키도록.'''.format(covid_num))
        bot.sendMessage(chat_id=id, text=info_message)

    elif (user_text == "뉴스"):
        covid_news = covid_news_crawling()
        bot.send_message(chat_id=id, text=covid_news)
        bot.sendMessage(chat_id=id, text=info_message)
 
    elif (user_text == "이미지"):
        bot.send_message(chat_id=id, text='''최신 이미지를 불러오는 중이다.
박사, 최고의 판단을 위해서는 인내심 또한 필요한 법이다.
하지만 박사에겐 아직은 없어 보이는군.''')
        covid_image_crawling(image_num=10)

        photo_list = []
        for i in range(len(os.walk("./코로나이미지").__next__()[2])):
            photo_list.append(telegram.InputMediaPhoto(open("./코로나이미지/{}.png".format(i), "rb")))
        bot.sendMediaGroup(chat_id=id, media=photo_list)
        bot.sendMessage(chat_id=id, text=info_message)
      
    
        
echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)
