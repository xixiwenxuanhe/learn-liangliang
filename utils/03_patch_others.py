import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import time
import random
from proxy_pool import proxy_accounts
import argparse

# 配置
'''
- 可选参数
    - 恋爱必修课
    - 极客时间
    - 文章

'''
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


base_url = "https://learn.lianglianglee.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def get_links():
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    # 只提取class包含menu-item且href以.md.html结尾的a标签
    links = []
    for a in soup.find_all("a", href=True, class_=True):
        if "menu-item" in a.get("class", []):
            href = a["href"]
            if href.endswith(".md.html"):
                links.append(href)
    return links

def download_static_resources(html, base_url, html_file_dir, proxies, base_dir):
    soup = BeautifulSoup(html, "html.parser")
    column_rel_path = os.path.relpath(html_file_dir, base_dir)
    for p in soup.find_all("p"):
        img = p.find("img", src=True)
        if img:
            src = img["src"]
            if src.startswith("assets/"):
                full_url = f"{base_url}/{column_rel_path}/{src}"
                local_path = os.path.join(html_file_dir, src)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                if os.path.exists(local_path):
                    print(f"      已存在: {local_path}")
                    continue
                try:
                    resp = requests.get(full_url, headers=headers, timeout=20, proxies=proxies)
                    if resp.status_code == 200:
                        with open(local_path, "wb") as f:
                            f.write(resp.content)
                        print(f"      下载成功: {local_path}")
                    elif resp.status_code == 429:
                        print(f"      被限流(429): {full_url}")
                    else:
                        print(f"      下载失败，状态码: {resp.status_code}，URL: {full_url}")
                except Exception as e:
                    print(f"      网络异常: {e} ({full_url})")
    return str(soup)

def main():
    links = get_links()
    total = len(links)
    print(f"共发现 {total} 个文件")
    if total == 0:
        return
    success = 0
    proxy_idx = 0
    num_proxies = len(proxy_accounts)
    for idx, href in enumerate(links, 1):
        # 每处理两个文件切换一次代理
        if (idx - 1) % 2 == 0:
            proxy_idx = ((idx - 1) // 2) % num_proxies
        username, password = proxy_accounts[proxy_idx]
        proxy_url = f"socks5://{username}:{password}@p.webshare.io:80"
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        print(f"进度: {idx}/{total} (当前代理: {username})")
        # 下载.md，保存为.md.html
        url_path = unquote(href)
        if url_path.endswith('.md.html'):
            md_url_path = url_path[:-5]  # 去掉.html
        else:
            md_url_path = url_path
        url = urljoin(base_url, md_url_path)
        filename = os.path.basename(url_path)
        save_path = os.path.join(column_dir, filename)
        assets_dir = os.path.dirname(save_path)  # 传递.md.html文件所在目录
        if os.path.exists(save_path):
            print(f"    已存在，跳过: {filename}")
            success += 1
            continue
        print(f"    正在处理: {filename}")
        retry = 0
        max_retry = 5
        wait_times = [5, 8, 16, 16, 16]
        while retry < max_retry:
            # 每次请求前固定延时1秒
            time.sleep(1)
            try:
                resp = requests.get(url, headers=headers, timeout=20, proxies=proxies)
                resp.encoding = resp.apparent_encoding
                if resp.status_code == 200:
                    html = resp.text
                    # 下载静态资源并修改src为本地路径
                    html = download_static_resources(html, base_url, assets_dir, proxies, base_dir)
                    # 全局替换.md为.md.html
                    html = re.sub(r'(?<!\.)\.md(?![\w.])', '.md.html', html)
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(html)
                    print(f"    已保存: {filename}")
                    success += 1
                    break
                elif resp.status_code == 429:
                    wait = wait_times[retry] if retry < len(wait_times) else 16
                    print(f"    被限流，{wait}s后重试（第{retry+1}次）...")
                    time.sleep(wait)
                    retry += 1
                else:
                    print(f"    下载失败，状态码: {resp.status_code}")
                    break
            except Exception as e:
                wait = wait_times[retry] if retry < len(wait_times) else 16
                print(f"    下载异常: {e}，{wait}s后重试（第{retry+1}次）...")
                time.sleep(wait)
                retry += 1
        else:
            print(f"    最多重试{max_retry}次，放弃: {filename}")
    print(f"保存率: {success}/{total} = {success/total:.2%}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量下载专栏内容")
    parser.add_argument("--column", type=str, default="恋爱必修课", help="专栏目录名，默认'恋爱必修课'")
    args = parser.parse_args()
    column_name = args.column
    global index_path, column_dir
    index_path = os.path.join(base_dir, column_name, "index.html")
    column_dir = os.path.join(base_dir, column_name)
    main()


# python utils/03_patch_others.py --column "恋爱必修课"

# python utils/03_patch_others.py --column "专栏/10x程序员工作法"