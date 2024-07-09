# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

import time


# %%
def load_source(url):
    main_url = "https://www.aladin.co.kr"
    res = requests.get(main_url + url)
    html = res.text
    soup = bs(html, "html.parser")
    return soup


# %%
first_url = "/shop/common/wbest.aspx?" "BranchType=1&start=we"
soup = load_source(first_url)

# %%
# 페이지 링크 수집
page_link = []
page_link.append(first_url)
for p in soup.find(class_="megaseller_rank").find_all("a")[1:-1]:
    page_link.append(p.get("href"))

# %%
# 책 정보 수집
books = []
for link in page_link:
    time.sleep(1)
    soup = load_source(link)
    book_list = soup.find_all(class_="ss_book_box")
    for book_info in book_list:
        book = {}
        book["img_src"] = book_info.img.get("src")
        book["link_addr"] = book_info.find(class_="bo3").get("href")
        book["book_title"] = book_info.find(class_="bo3").text
        books.append(book)

# %%
# 데이터프레임으로 변환
df = pd.DataFrame(books)

# %%
# CSV 파일로 저장
df.to_csv("aladdin_bestseller.csv", index=False)
