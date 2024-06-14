import scrapy
from pathlib import Path
from bs4 import BeautifulSoup
import os
import re
from glob import glob
from scrapy.selector import Selector
import csv
from urllib.parse import urljoin
csv_input=list()
def browser_header(str):
        headers = dict()
        lines = str.splitlines()
        for kv in lines:
            if kv.strip() == '':
                continue
            key, value = kv.split(':', 1) if ':' in kv else (kv, None)
            headers[key] = value
        return headers
def scrape_links(response):
    html_content = response.body.decode("utf-8")
    selector = Selector(text=html_content)
    link = selector.css("span.global-reviews-all a.a-link-emphasis.a-text-bold::attr(href)").get(0)
    if not link:
        link = selector.css("a.a-link-emphasis.a-text-bold::attr(href)").get(0)
    if link:
        print(f"Found link in response: {link}")
        return link
    else:
        print(f"No matching link found in response")
        return None
def extract_text_and_links(response):
    # Extract HTML content from the response
    html_content = response.body.decode("utf-8")  # Assuming UTF-8 encoding
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    text_link_pairs = {}
    for span in soup.find_all('span', class_='a-size-medium a-color-base a-text-normal'):
        parent_a = span.find_parent('a', href=True)
        if parent_a:
            text = span.text.strip()
            link = parent_a['href']
            text_link_pairs[text] = link

    return text_link_pairs
class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://flipkart.com/search?q=Intel&page="]
    def start_requests(self):
        header="""Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: session-id=257-4625196-3471332; session-id-time=2082787201l; lc-acbin=en_IN; urtk=%7B%22at%22%3A%22Atna%7CEwICIBU0JA2jtCl1xCyP8Nkv1JfHXE7-YGgCZAnaDcBqe-KgSePx2i2ZIGOlfGCZFYfvL2Ddrow66aVb9FJiV69BhrWknEcsjmh84Wte0OeyMVSKBPx3Drc7dQyNW4r6_6foG-3a2iYEK3coa3As8PiIprtZBjrgp9GusOBldLvYQsNff36lVC3Y3w78X3yYnKgrXQQI6Bhmc0spO9eHPar9Tbq9A55qMWAW_bxK57womurkTh1BZTH5hBeV7s_10cI1BDLTHhEFt1ODVBKoHtw3SMIeKyJoLhyvLvQ_EAJ4rDsyjBy8eono6uulTRoX2rhutrY%22%2C%22atTtl%22%3A1690231742682%2C%22rt%22%3A%22Atnr%7CEwICIBnsTYgMomDpv9xfzv4133k2v8uVQgFsIEbe4hsQsq8pR9FXoBzUcOikJBF1_o-suof3lIENvf0--f8XCs647LXOtAj7aTb698OeoomJJHTM9yifZ0OaIHjT3U_XQTNwij9iweh1btoYvcPYmGbqu1eajJWOrTHYxjLANWKzRXqs7IQXkdr27-INc1EGBHbpUaE4uJpMzWzsMqwb8jR1zEgO7xNkPSP-BR17Lkq7pFv3rhWb3ojhIqPq9HmLsEEEIZaSXvMsc4vfwe1Z9rIiGk5g5rMxHjjF60j88Z0MrWeMqmJwR9nhu4Z9VGVvaQXWpZtYVLkQ4gsFlZo43R6ZQ6d1%22%7D; ubid-acbin=257-1312609-7306730; i18n-prefs=INR; session-token=aBa+d3oYhYeyZYtzXFYH+wofgekTYJP+hZUChR1BdebKJp4EHJ5yKZ7fqTrQfqexNgRaLwvkJPBCOldzRnq0Ra50SyKwfgAarKARANhdaLWIAhFllQ45y7aPueQhY9C0qaPZCQd55sp/3Kbs7C1G+pIi44fp7L0g7+jhWE0/3EwU4jJ9zF8BFZ1gbxH+O/BsQuvUrtKvUskjpGT0o8UZYMz4otFBfLEsCj/6ZTP1DkPqRoiZYZFUbbqg/SZVZuppCyOio5VPvTd4Ns1IlwmXHct4E40cVN4divjoFI4mhX+qEQmmiNjFStgV8wlTMMnonYivJ5Jo+Ty2yreNxRsfYsK6dgKTy097; csm-hit=tb:ZQSKX1MXGQ7EKZDZYZDH+s-ZQSKX1MXGQ7EKZDZYZDH|1716531140745&t:1716531140745&adb:adblk_no
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
"""
        headers=browser_header(header)
        #Starting to scrape amazon.in/Intel
        urls = [f"{FlipkartSpider.start_urls}{page}" for page in range(1, 31)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={'site_name':'flipkart'})

    def parse(self, response):
        header="""Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: session-id=257-4625196-3471332; session-id-time=2082787201l; lc-acbin=en_IN; urtk=%7B%22at%22%3A%22Atna%7CEwICIBU0JA2jtCl1xCyP8Nkv1JfHXE7-YGgCZAnaDcBqe-KgSePx2i2ZIGOlfGCZFYfvL2Ddrow66aVb9FJiV69BhrWknEcsjmh84Wte0OeyMVSKBPx3Drc7dQyNW4r6_6foG-3a2iYEK3coa3As8PiIprtZBjrgp9GusOBldLvYQsNff36lVC3Y3w78X3yYnKgrXQQI6Bhmc0spO9eHPar9Tbq9A55qMWAW_bxK57womurkTh1BZTH5hBeV7s_10cI1BDLTHhEFt1ODVBKoHtw3SMIeKyJoLhyvLvQ_EAJ4rDsyjBy8eono6uulTRoX2rhutrY%22%2C%22atTtl%22%3A1690231742682%2C%22rt%22%3A%22Atnr%7CEwICIBnsTYgMomDpv9xfzv4133k2v8uVQgFsIEbe4hsQsq8pR9FXoBzUcOikJBF1_o-suof3lIENvf0--f8XCs647LXOtAj7aTb698OeoomJJHTM9yifZ0OaIHjT3U_XQTNwij9iweh1btoYvcPYmGbqu1eajJWOrTHYxjLANWKzRXqs7IQXkdr27-INc1EGBHbpUaE4uJpMzWzsMqwb8jR1zEgO7xNkPSP-BR17Lkq7pFv3rhWb3ojhIqPq9HmLsEEEIZaSXvMsc4vfwe1Z9rIiGk5g5rMxHjjF60j88Z0MrWeMqmJwR9nhu4Z9VGVvaQXWpZtYVLkQ4gsFlZo43R6ZQ6d1%22%7D; ubid-acbin=257-1312609-7306730; i18n-prefs=INR; session-token=aBa+d3oYhYeyZYtzXFYH+wofgekTYJP+hZUChR1BdebKJp4EHJ5yKZ7fqTrQfqexNgRaLwvkJPBCOldzRnq0Ra50SyKwfgAarKARANhdaLWIAhFllQ45y7aPueQhY9C0qaPZCQd55sp/3Kbs7C1G+pIi44fp7L0g7+jhWE0/3EwU4jJ9zF8BFZ1gbxH+O/BsQuvUrtKvUskjpGT0o8UZYMz4otFBfLEsCj/6ZTP1DkPqRoiZYZFUbbqg/SZVZuppCyOio5VPvTd4Ns1IlwmXHct4E40cVN4divjoFI4mhX+qEQmmiNjFStgV8wlTMMnonYivJ5Jo+Ty2yreNxRsfYsK6dgKTy097; csm-hit=tb:ZQSKX1MXGQ7EKZDZYZDH+s-ZQSKX1MXGQ7EKZDZYZDH|1716531140745&t:1716531140745&adb:adblk_no
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
"""
        headers=browser_header(header)
        site_name = response.meta.get('site_name')
        sanitized_site_name = re.sub(r'[^\w\-.]', '', site_name)[:75]
        extracted_texts = extract_text_and_links(response) #Stores names of products and also their links
        base_url = "https://www.flipkart.com/" 
        for product_name, link in extracted_texts.items():
           full_url = f"{base_url}/{link}"
           yield scrapy.Request(url=full_url, callback=self.parse_sectier, headers=headers, meta={'site_name': product_name})
