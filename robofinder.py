import requests
from bs4 import BeautifulSoup
import re
import time

def get_robot_urls(domain):
    # درخواست اولیه برای به‌دست‌آوردن ایندکس‌های موجود از robots.txt در آرشیو وب
    index_url = f"https://web.archive.org/cdx/search/cdx?url={domain}/robots.txt&output=json&fl=timestamp,original"
    response = requests.get(index_url)
    
    if response.status_code != 200:
        print("Failed to retrieve index data.")
        return []

    data = response.json()[1:]  # اولین عنصر، عنوان است؛ آن را نادیده می‌گیریم
    urls = [f"https://web.archive.org/web/{item[0]}/{item[1]}" for item in data]
    return urls

def fetch_robot_content(url):
    # درخواست برای به‌دست‌آوردن محتوای robots.txt ذخیره‌شده در آرشیو وب
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

def extract_paths(content):
    # استفاده از regex برای استخراج مسیرهای disallowed
    paths = re.findall(r"Disallow: (/[^\s]*)", content)
    return paths

def main(domain):
    robot_urls = get_robot_urls(domain)
    all_paths = set()  # برای جلوگیری از تکراری بودن مسیرها

    print(f"Found {len(robot_urls)} archive entries for robots.txt files.")
    
    for url in robot_urls:
        print(f"Fetching: {url}")
        content = fetch_robot_content(url)
        paths = extract_paths(content)
        all_paths.update(paths)
        time.sleep(0.5)  # برای جلوگیری از محدودیت‌های درخواست‌های مکرر

    # چاپ خروجی مرتب و بدون تکرار
    print("\nUnique Disallowed Paths:")
    for path in sorted(all_paths):
        print(path)

if __name__ == "__main__":
    # به جای 'example.com' آدرس سایت مورد نظر را وارد کنید
    url = input('<https://example.com>: ')
    main(url)
