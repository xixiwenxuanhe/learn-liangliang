import os
import re
import requests
from bs4 import BeautifulSoup

# 获取 index.html 路径（上一级目录）
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# index_path = os.path.join(base_dir, "index.html")
column_name = "专栏"  # 处理专栏
index_path = os.path.join(base_dir, column_name, "index.html")   # 处理专栏

base_url = "https://learn.lianglianglee.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def safe_filename(name):
    # 替换文件名中的非法字符
    return re.sub(r'[\\/:*?"<>|]', '_', name)

# 读取 index.html
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 提取所有菜单项
menu_items = []
for a in soup.find_all("a", class_="menu-item"):
    menu_id = a.get("id")
    href = a.get("href")
    if menu_id and href:
        menu_items.append((menu_id, href))

print(f"共发现 {len(menu_items)} 个菜单项，开始处理...")

for menu_id, href in menu_items:
    # dir_path = os.path.join(base_dir, menu_id)
    dir_path = os.path.join(base_dir, column_name, menu_id) # 处理专栏
    os.makedirs(dir_path, exist_ok=True)
    save_path = os.path.join(dir_path, "index.html")
    url = base_url + href
    try:
        resp = requests.get(url, headers=headers)
        resp.encoding = resp.apparent_encoding
        if resp.status_code == 200:
            html_content = resp.text
            # 替换 .md" 为 .md.html"
            html_content = re.sub(r'(\.md)(")', r'\1.html\2', html_content)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"已保存：{save_path}")
        else:
            print(f"抓取失败：{menu_id}，状态码：{resp.status_code}")
    except Exception as e:
        print(f"抓取异常：{menu_id}，原因：{e}")

print("全部菜单 index.html 抓取完成。")
