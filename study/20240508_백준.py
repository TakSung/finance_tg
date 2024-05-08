# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from markdownify import markdownify
from icecream import ic
from bs4 import BeautifulSoup
import os
import argparse

# %%
# Chrome WebDriver 다운로드 및 관리
service = Service(ChromeDriverManager().install())


# %%
def get_driver_source(url):
    # Selenium 웹 드라이버 설정
    options = Options()
    # options.add_argument('--headless')  # 브라우저를 표시하지 않고 실행

    # Chrome WebDriver 시작
    driver = webdriver.Chrome(service=service, options=options)

    # 페이지 열기
    driver.get(url)

    # 페이지 소스 가져오기
    page_source = driver.page_source

    # 웹 드라이버 종료
    driver.quit()

    return page_source


# %%
def replace_str(text):
    index = text.find("힌트")
    if index != -1:
        # "힌트" 이후의 문자열을 삭제
        new_text = text[:index]  # "힌트" 이후의 모든 문자열을 삭제
    else:
        new_text = text[:]
    new_text = new_text.replace(" 복사\n-----------\n\n\n\n\n```", "```css")
    new_text = new_text.replace("\n\n```", "\n```")
    new_text = new_text.replace("\n\n\n\n", "\n\n")
    new_text = new_text.replace("\n\n\n", "\n")
    new_text = new_text.replace("예제", "### 예제")
    return new_text


# %%
def make_markdown_file(filename, contents):
    # Markdown 파일 생성 및 내용 쓰기
    with open(filename, "w", encoding="utf-8") as file:
        file.write(contents + "\n\n")
    print(f"Markdown 파일 '{filename}'이 생성되었습니다.")


# %%
problem_number = 10808
target_path = "."

# 백준 문제 페이지 URL
url = f"https://www.acmicpc.net/problem/{problem_number}"

try:
    page_source = get_driver_source(url)
except:
    try:
        page_source = get_driver_source(url)
    except:
        raise ValueError()
try:
    remaked_source = remake_html_source(page_source)
except ValueError:
    ic(problem_number, "error remake_html_source")
    remaked_source = None

if remaked_source is None:
    ic(problem_number)
    make_markdown_file(f"error_{problem_number}.txt", page_source)
    raise ValueError()
markdown_text = markdownify(remaked_source)

postprocess_text = replace_str(markdown_text)
make_markdown_file(target_path, postprocess_text)
