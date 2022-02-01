'''
Author : Pratik Joshi
Date: 2/1/2021
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import requests
import datetime

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://www.powerlanguage.co.uk/wordle/"

def find_word(cur_date,wordle_lst):
    base_dt = datetime.date(2021, 5, 19)
    word_len = len(wordle_lst)
    day_bw=(cur_date-base_dt).days-31
    idx=day_bw%word_len
    return idx

def fetch_future():
    page = driver.find_elements(By.TAG_NAME, 'script')
    page_src=[]
    for i in page:
        page_src.append(i.get_attribute('src'))
    driver.close()
    resp=requests.get(page_src[-1])
    resp_txt=resp.text
    word_lst_pat=resp_txt.split('var La=')
    wordle_str=word_lst_pat[1].split(',Ta=')[0]
    wordle_lst=wordle_str.strip('][').split(',')

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    tomorrow = today + datetime.timedelta(1)

    today_word = wordle_lst[find_word(today,wordle_lst)]
    yestr_word = wordle_lst[find_word(yesterday,wordle_lst)]
    tom_word = wordle_lst[find_word(tomorrow,wordle_lst)]

    print('\nTomorrows Wordle:')
    print('---------------------------')
    print(tom_word.strip('"').upper())

def main():
    driver.get(url)
    ##To Reveal Today Wordle
    val=driver.execute_script("return localStorage.getItem('gameState')")
    print('\nTodays Wordle:')
    print('---------------------------')
    print(json.loads(val)['solution'].upper())

    fetch_future()

if __name__=='__main__':
    main()








