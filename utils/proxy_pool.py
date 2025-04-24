import random
import requests

# 代理账号信息
proxy_accounts = [
    ("yangyangmao-rotate", "yangyangmao"),
    ("iu7zso75luk-rotate", "iu7zso75luk"),
    ("shengshi-rotate", "shengshi"),
    ("xixiwenxuanhe-rotate", "xixiwenxuanhe"),
]

def get_random_proxy():
    """
    随机返回一个socks5代理配置（适用于requests的proxies参数）
    """
    username, password = random.choice(proxy_accounts)
    proxy_url = f"socks5://{username}:{password}@p.webshare.io:80"
    return {
        "http": proxy_url,
        "https": proxy_url,
    }

def test_all_proxies():
    test_url = "https://httpbin.org/ip"
    for username, password in proxy_accounts:
        proxy_url = f"socks5://{username}:{password}@p.webshare.io:80"
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        print(f"测试代理: {proxy_url}")
        try:
            resp = requests.get(test_url, proxies=proxies, timeout=10)
            print("  返回：", resp.text)
            print("  成功")
        except Exception as e:
            print("  失败：", e)

if __name__ == "__main__":
    test_all_proxies() 