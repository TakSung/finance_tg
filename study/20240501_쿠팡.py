# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup as bs

import time

# %%
# Chrome WebDriver 다운로드 및 관리
service = Service(ChromeDriverManager().install())

# %%
def load_source(url):
    main_url = "https://www.coupang.com"
    # Selenium 웹 드라이버 설정
    options = Options()
    options.add_experimental_option("detach", True)
    # options.add_argument('--headless')  # 브라우저를 표시하지 않고 실행

    # Chrome WebDriver 시작
    driver = webdriver.Chrome(service=service, options=options)
    
    # 페이지 열기
    print("target url : ",main_url+url)
    driver.get(main_url + url)
    
    # 페이지 소스 가져오기
    html = driver.page_source
    
    # soup 으로 해석
    soup = bs(html, "html.parser")
    
    # 웹 드라이버 종료
    driver.quit()
    
    return soup


# %%
first_url = "/np/campaigns/82/components/185569"
soup = load_source(first_url)

# %%
print(soup)

# %%
# 페이지 링크 수집
page_link = []
page_link.append(first_url)
# for p in soup.find(class_="megaseller_rank").find_all("a")[1:-1]:
#     page_link.append(p.get("href"))

# %%
# 상품 정보 수집
products = []
for link in page_link:
    time.sleep(1)
    soup = load_source(link)
    product_list = soup.find_all(class_="baby-product renew-badge ")
    for product_info in product_list:
        book = {}
        book["img_src"] = product_info.img.get("src")
        book["link_addr"] = product_info.get("href")
        book["book_title"] = product_info.find(class_="bo3").text
        products.append(book)

# %%
# 데이터프레임으로 변환
df = pd.DataFrame(products)

# %%
# CSV 파일로 저장
df.to_csv("aladdin_bestseller.csv", index=False)
