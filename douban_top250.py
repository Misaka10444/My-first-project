import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 创建带重试机制的session
session = requests.Session()
retry = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 准备CSV文件头
with open("douban_top250_full.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["排名", "电影名", "评分", "评价人数", "导演", "年份", "国家/地区", "链接"])

all_data = []

for page in range(10):
    start = page * 25
    url = f"https://movie.douban.com/top250?start={start}"

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        movies = soup.select(".item")

        if not movies:
            print(f"第{page + 1}页未获取到数据，可能被反爬")
            break

        print(f"正在抓取第{page + 1}页...")

        for movie in movies:
            try:
                # 排名
                rank = movie.select_one(".pic em").text.strip()

                # 电影名（中文名）
                title_elem = movie.select_one(".title")
                title = title_elem.text.strip() if title_elem else "未知"

                # 评分
                rating_elem = movie.select_one(".rating_num")
                rating = rating_elem.text.strip() if rating_elem else "未知"

                # 评价人数
                num_elem = movie.select_one(".star span:last-child")
                if num_elem:
                    num = re.search(r'(\d+)', num_elem.text)
                    num = num.group(1) if num else "未知"
                else:
                    num = "未知"

                # 详细信息
                info = movie.select_one(".bd p:first-child")
                info_text = info.text.strip() if info else ""

                # 提取导演
                director = "未知"
                if "导演:" in info_text:
                    director_match = re.search(r'导演:\s*([^\d主]+)', info_text)
                    if director_match:
                        director = director_match.group(1).strip()

                # 提取年份和国家
                year = "未知"
                country = "未知"
                year_match = re.search(r'(\d{4})', info_text)
                if year_match:
                    year = year_match.group(1)
                    # 提取国家（在年份后面括号中的内容）
                    country_match = re.search(r'\(\d{4}\s*([^)]*)\)', info_text)
                    if country_match:
                        country = country_match.group(1).strip()

                # 链接
                link_elem = movie.select_one("a")
                link = link_elem["href"] if link_elem else ""

                all_data.append([rank, title, rating, num, director, year, country, link])
                print(f"  已抓取：{rank} {title} {rating}分")

            except Exception as e:
                print(f"  解析某部电影时出错：{e}")
                continue

        time.sleep(2)  # 增加延时，降低被封风险

    except requests.exceptions.RequestException as e:
        print(f"第{page + 1}页请求失败：{e}")
        continue

# 写入所有数据
if all_data:
    with open("douban_top250_full.csv", "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(all_data)
    print(f"\n全部{len(all_data)}部电影抓取完成！")
else:
    print("未抓取到任何数据")

print("请打开 douban_top250_full.csv 查看。")