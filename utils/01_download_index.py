import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url = "https://learn.lianglianglee.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding  # 自动识别编码

# 计算上一级目录的 index.html 路径
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
save_path = os.path.join(base_dir, "index.html")

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # 下载CSS
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href")
        if href:
            css_url = urljoin(url, href)
            css_name = os.path.basename(urlparse(css_url).path)
            css_dir = os.path.join(base_dir, "static")
            os.makedirs(css_dir, exist_ok=True)
            css_path = os.path.join(css_dir, css_name)
            try:
                css_content = requests.get(css_url, headers=headers).text
                with open(css_path, "w", encoding="utf-8") as f:
                    f.write(css_content)
                print(f"已保存CSS: {css_path}")
                # 替换HTML中的路径
                link['href'] = os.path.relpath(css_path, base_dir)
            except Exception as e:
                print(f"下载CSS失败: {css_url}，原因: {e}")

    # 下载图片
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            img_url = urljoin(url, src)
            img_name = os.path.basename(urlparse(img_url).path)
            img_dir = os.path.join(base_dir, "static")
            os.makedirs(img_dir, exist_ok=True)
            img_path = os.path.join(img_dir, img_name)
            try:
                img_content = requests.get(img_url, headers=headers).content
                with open(img_path, "wb") as f:
                    f.write(img_content)
                print(f"已保存图片: {img_path}")
                # 替换HTML中的路径
                img['src'] = os.path.relpath(img_path, base_dir)
            except Exception as e:
                print(f"下载图片失败: {img_url}，原因: {e}")

    # 下载JS
    for script in soup.find_all("script"):
        src = script.get("src")
        if src:
            js_url = urljoin(url, src)
            js_name = os.path.basename(urlparse(js_url).path)
            js_dir = os.path.join(base_dir, "static")
            os.makedirs(js_dir, exist_ok=True)
            js_path = os.path.join(js_dir, js_name)
            try:
                js_content = requests.get(js_url, headers=headers).text
                with open(js_path, "w", encoding="utf-8") as f:
                    f.write(js_content)
                print(f"已保存JS: {js_path}")
                # 替换HTML中的路径
                script['src'] = os.path.relpath(js_path, base_dir)
            except Exception as e:
                print(f"下载JS失败: {js_url}，原因: {e}")

    # 替换所有a标签中以.md结尾的href为.md.html
    for a in soup.find_all("a"):
        href = a.get("href")
        if href and href.strip().endswith(".md"):
            a["href"] = href + ".html"

    # 保存修改后的HTML
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"已保存为 {save_path}")
else:
    print("请求失败，状态码：", response.status_code) 