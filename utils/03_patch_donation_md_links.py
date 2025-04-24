import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

base_url = "https://learn.lianglianglee.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
assets_dir = os.path.join(base_dir, "assets")
os.makedirs(assets_dir, exist_ok=True)

# 1. 下载捐赠.md，保存为捐赠.md.html
asset_url = base_url + "/assets/捐赠.md"
asset_save_path = os.path.join(assets_dir, "捐赠.md.html")

resp = requests.get(asset_url, headers=headers)
resp.encoding = resp.apparent_encoding
if resp.status_code != 200:
    # 如果 .md 失败，尝试 .md.html
    asset_url = base_url + "/assets/捐赠.md.html"
    resp = requests.get(asset_url, headers=headers)
    resp.encoding = resp.apparent_encoding

if resp.status_code == 200:
    html_content = resp.text
    soup = BeautifulSoup(html_content, "html.parser")

    # 2. 下载图片、视频、音频等静态资源并修正路径
    for tag in soup.find_all(["img", "video", "audio"]):
        src = tag.get("src")
        if src and not src.startswith("data:"):
            resource_url = urljoin(asset_url, src)
            resource_name = os.path.basename(urlparse(resource_url).path)
            # 如果文件名以点开头，去掉点
            if resource_name.startswith('.'):
                new_resource_name = resource_name[1:]
            else:
                new_resource_name = resource_name
            resource_path = os.path.join(assets_dir, new_resource_name)
            try:
                r = requests.get(resource_url, headers=headers)
                if r.status_code == 200:
                    with open(resource_path, "wb") as f:
                        f.write(r.content)
                    print(f"已下载静态资源: {resource_path}")
                    tag["src"] = f"./{new_resource_name}"
                else:
                    print(f"静态资源下载失败: {resource_url}，状态码：{r.status_code}")
            except Exception as e:
                print(f"静态资源下载异常: {resource_url}，原因：{e}")

    # 3. 保存修正后的 HTML
    html_str = str(soup)
    html_str = re.sub(r'(?<!\.)\.md(?![\w.])', '.md.html', html_str)
    with open(asset_save_path, "w", encoding="utf-8") as f:
        f.write(html_str)
    print(f"已保存：{asset_save_path}")
else:
    print(f"抓取失败：捐赠.md，状态码：{resp.status_code}") 