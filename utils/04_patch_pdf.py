import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import time
import random
from proxy_pool import proxy_accounts

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
index_path = os.path.join(base_dir, "PDF", "index.html")
pdf_dir = os.path.join(base_dir, "PDF")
base_url = "https://learn.lianglianglee.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def get_pdf_links():
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for li in soup.find_all("li"):
        a = li.find("a", href=True, class_="menu-item")
        if a and a["href"].lower().endswith(".pdf"):
            links.append(a["href"])
    # 去重
    links = list(dict.fromkeys(links))
    return links

def main():
    links = get_pdf_links()
    total = len(links)
    print(f"共发现 {total} 个PDF文件")
    if total == 0:
        return
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
        url = urljoin(base_url, href)
        filename = os.path.basename(unquote(href))
        save_path = os.path.join(pdf_dir, filename)
        if os.path.exists(save_path):
            print(f"    已存在，跳过: {filename}")
            continue
        print(f"    正在下载: {filename}")
        retry = 0
        max_retry = 5
        wait_times = [5, 8, 16, 16, 16]
        while retry < max_retry:
            time.sleep(1)
            try:
                resp = requests.get(url, headers=headers, timeout=30, proxies=proxies)
                if resp.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(resp.content)
                    print(f"    已保存: {filename}")
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

if __name__ == "__main__":
    main()
