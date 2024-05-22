# %%
# 기본 세팅
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import random, time

# from selenium.webdriver.common.by import By

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('window-size=1920x1080')
service = Service(ChromeDriverManager().install())


# %%
# 스크롤 함수 정의의
def scroll(drive, page_limit):
    try:
        # `allow pasting` 크롬 개발도구에서 붙여넣기하기(보안적인 문제가 있어서 안하는게 좋긴함)
        # document.documentElement.scrollHeight 한번 가서 해보기
        # https://ko.javascript.info/size-and-scroll-window

        # 페이지 내 스크롤 높이를 받아 오는...
        last_page_height = drive.execute_script(
            "return document.documentElement.scrollHeight"
        )

        cnt = 1
        while True:
            # 사람처럼 보이기 위한 슬립타임
            pause_time = random.uniform(1, 2)

            # 있는 스크롤 크기만큼 내리고 잠시 쉬기
            drive.execute_script(
                "window.scrollTo(0,document.documentElement.scrollHeight);"
            )
            time.sleep(pause_time)

            # 로딩하는 동안 있는 스크롤에서 살짝 내리고 잠시 쉬기
            drive.execute_script(
                "window.scrollTo(0,document.documentElement.scrollHeight+50);"
            )
            time.sleep(pause_time)

            new_page_height = drive.execute_script(
                "return document.documentElement.scrollHeight"
            )

            if new_page_height == last_page_height: # 더 이상 없을 때 
                print("scroll finish!!!!")
                break
            else:
                last_page_height = new_page_height # 더 있을 때

            if cnt > page_limit: # 페이지 넘어갔는지 확인
                break
            cnt += 1
    except:
        print("Error ")


# %%
### main
# def main(search_word):
search_word = "페이커"
page_limit = 1

y_url = "https://www.youtube.com/results?search_query={}"

drive = webdriver.Chrome(options=chrome_options, service=service)
drive.implicitly_wait(3)  # 나올때까지 적당한 시간 기다리기
drive.get(
    y_url.format(search_word)
)  # ex) "https://www.youtube.com/results?search_query=페이커"
drive.implicitly_wait(3)
# 무한 스크롤링~~~
scroll(drive, page_limit)

html_source = drive.page_source
# %%

soup = bs(html_source, "html.parser")

# print(soup)

# %%
# 키워드 찾기
if search_word == "":
    c_list = soup.find_all(class_="style-scope ytd-rich-grid-media")
else:
    c_list = soup.find_all(class_="yt-simple-endpoint style-scope ytd-video-renderer")

# %%
# 원하는 요소 추출
y_link_list = []

for c in c_list:
    y_link_list.append(
        {"url": "https://www.youtube.com/" + c.get("href"), "title": c.text.strip()}
    )

# %%
# 저장
import json

with open("youtube.json", "w", encoding="UTF-8") as f:
    json.dump(y_link_list, f, ensure_ascii=False)
print("완료!!!!")


# %%
# if __name__ == "__main__":
#     search_word = input("검색할 단어를 알려주세요!")
#     main(search_word)
