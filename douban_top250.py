import requests
from bs4 import BeautifulSoup
import csv
import time

# 准备CSV文件头
with open("douban_top250_full.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["排名", "电影名", "评分", "评价人数", "导演", "年份", "国家", "链接"])

# 循环爬取10页
for page in range(10):
    start = page * 25
    url = f"https://movie.douban.com/top250?start={start}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.select(".item")

    for movie in movies:
        # 排名
        rank = movie.select_one(".pic em").text

        # 电影名（中文名）
        title = movie.select_one(".title").text

        # 评分
        rating = movie.select_one(".rating_num").text

        # 评价人数
        num_elem = movie.select_one(".star span:last-child")
        num = num_elem.text[:-3] if num_elem else "未知"

        # 其他信息（导演、年份、国家）
        info = movie.select_one(".bd p:first-child").text.strip()
        if "导演:" in info:
            director = info.split("导演:")[1].split(" 主演")[0].split("主")[0].strip()
        else:
            director = "未知"

        if "(" in info:
            year_country = info.split("(")[1].split(")")[0]
            year = year_country[:4] if year_country[:4].isdigit() else "未知"
            country = year_country[4:] if len(year_country) > 4 else "未知"
        else:
            year = "未知"
            country = "未知"

        link = movie.select_one("a")["href"]

        # 写入CSV
        with open("douban_top250_full.csv", "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([rank, title, rating, num, director, year, country, link])

        print(f"已抓取：{rank} {title} {rating}分")

    time.sleep(1)

print("全部250部电影抓取完成！请打开 douban_top250_full.csv 查看。")