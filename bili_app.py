#!/home/ubuntu/.pyenv/shims/python

import sys
import csv
import json
import requests
import random
from time import sleep
import chromedriver_binary 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template
from flask import request

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('bili_scraper.html')

@app.route('/scraper', methods=["POST"])
def scraper():
    print('ajax scceed')
    data = request.json
    file_name = data['file_name']
    url = data['vdo_url']
    if 'https://' not in url:
        url = 'https://' + url
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    options.binary_location = '/usr/bin/google-chrome'
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(1200,1000)
    print('start scraper')

    try:
        driver.get(url)
        sleep(5)

        res_list = []
        user_list = []
        while True:
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            print('scrolling')


            if last_height == new_height:
                break

        res_list = []
        user_list = []
        comments = driver.find_elements(by=By.CSS_SELECTOR, value='#comment > div > div.comment > div > div.comment-list > div')
        for comment in comments:
            user = comment.find_element(by=By.CSS_SELECTOR, value='div.con > div.user > a').text
            content = comment.find_element(by=By.CSS_SELECTOR, value='div.con > p').text
            up_name = f'英雄下班后'
            if user != up_name and user not in user_list:
                res_list.append([user, content])
                user_list.append(user)

        driver.quit()

        f_write = open('/var/www/html/app/static/' + file_name, 'a', newline='', encoding='utf-8')
        res_csv_writer = csv.writer(f_write, delimiter=',')
        for res in res_list:
            res_csv_writer.writerow(res)
        f_write.close()
        luk_num = random.randrange(len(user_list))
        print(user_list[luk_num])
        
        return user_list[luk_num]

    except:
        driver.quit()
        return 'error!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000, threaded=True)