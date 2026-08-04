import requests
from bs4 import BeautifulSoup

# 豆瓣Top250的URL
url = "https://movie.douban.com/top250"

# 模拟浏览器访问，防止被拒绝
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 发送请求
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 找到所有电影条目
movies = soup.select(".item")

print("豆瓣Top250电影列表：\n")
for movie in movies:
    # 提取标题
    title = movie.select_one(".title").text
    # 提取评分
    rating = movie.select_one(".rating_num").text
    # 提取链接
    link = movie.select_one("a")["href"]

    print(f"电影：{title}")
    print(f"评分：{rating}")
    print(f"链接：{link}")
    print("-" * 40)