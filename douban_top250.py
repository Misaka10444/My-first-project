import requests
from bs4 import BeautifulSoup
import csv

# 豆瓣Top250的URL（只爬了第一页）
url = "https://movie.douban.com/top250"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
movies = soup.select(".item")

# 准备CSV文件
with open("douban_top250_first_page.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["排名", "电影名", "评分", "链接"])

print("豆瓣Top250电影列表（第一页）：\n")
for movie in movies:
    rank = movie.select_one(".pic em").text
    title = movie.select_one(".title").text
    rating = movie.select_one(".rating_num").text
    link = movie.select_one("a")["href"]

    print(f"{rank} {title} {rating}分")

    # 写入CSV
    with open("douban_top250_first_page.csv", "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([rank, title, rating, link])

print("\n第一页数据已保存到 douban_top250_first_page.csv")