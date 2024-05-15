
#%%
import random, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#chrome_options.add_argument('--headless')
#chrome_options.add_argument('window-size=1920x1080')
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())

def scroll(drv,page_limit):
    try:
        # 페이지 내 스크롤 높이를 받아 오는...
        last_page_height = drv.execute_script('return document.documentElement.scrollHeight')

        cnt = 1
        while True:
            pause_time = random.uniform(1,2)
            drv.execute_script('window.scrollTo(0,document.documentElement.scrollHeight);')
            time.sleep(pause_time)
            drv.execute_script('window.scrollTo(0,document.documentElement.scrollHeight+50);')
            time.sleep(pause_time)
            new_page_height = drv.execute_script('return document.documentElement.scrollHeight')

            if new_page_height == last_page_height:
                print('scroll finish!!!!')
                break
            else:
                last_page_height = new_page_height

            if cnt > page_limit:
                break
            cnt+=1
    except:
        print('Error ')

### main

def main(search_word):
    #search_word = '오징어 게임'
    page_limit = 3


    y_url = 'https://www.youtube.com/results?search_query={}'

    drv =  webdriver.Chrome(options=chrome_options, service=service)
    drv.implicitly_wait(3)
    drv.get(y_url.format(search_word))
    drv.implicitly_wait(3)
    # 무한 스크롤링~~~
    scroll(drv,page_limit)

    html_source = drv.page_source
    #%%

    soup = BeautifulSoup(html_source,'html.parser')

    #print(soup)

    # %%

    if search_word == '':
        c_list = soup.find_all(class_='yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media')
    else:
        c_list = soup.find_all(class_='yt-simple-endpoint style-scope ytd-video-renderer')

    y_link_list = []

    for c in c_list:
        y_link_list.append(
            {
                "url": "https://www.youtube.com/" +c.get('href'),
                "title": c.text
            }
        )

    import json
    with open('youtube.json','w') as f:
        json.dump(y_link_list, f)
    print('완료!!!!')   

# %%
if __name__=='__main__':
    search_word = input('검색할 단어를 알려주세요!')
    main(search_word)