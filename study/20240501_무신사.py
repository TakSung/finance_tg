# %%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


# %%
def load_source(url):
    main_url = "https://www.musinsa.com"
    res = requests.get(main_url + url)
    html = res.text
    soup = bs(html, "html.parser")
    return soup


# %%
first_url = "/categories/item/002002"
soup = load_source(first_url)


# %%
# 페이지 링크 수집
page_link = []
page_link.append(first_url)
# for i in range(2, 4):
#     page_link.append(
#         f"/categories/item/002002?d_cat_cd=002002&brand=&list_kind=small&sort=pop_category&sub_sort=&page={i}&display_cnt=90&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="
#     )

# %%
# 책 정보 수집
items = []
for link in page_link:
    time.sleep(1)
    soup = load_source(link)
    item_list = soup.find_all(class_="li_box")
    for item_info in item_list:
        item = {}
        item["img_src"] = item_info.img.get("data-original")
        item["link_addr"] = "https:" + item_info.find(class_="img-block").get("href")
        item["item_title"] = str(item_info.find(class_="list_info").text).strip()
        items.append(item)

# %%
# 데이터프레임으로 변환
df = pd.DataFrame(items)

# %%
# CSV 파일로 저장
df.to_csv("musinsa_jaket.csv", index=False)
