from glob import glob
from scrapy.selector import Selector


def scrape_links(directory):
    link_list=list()
    for filename in glob(f"{directory}/*.html"):
        if filename != f"{directory}/amazon.html":
            with open(filename, 'r', encoding="utf-8") as f:
                html_content = f.read()
            selector = Selector(text=html_content)
            link = selector.css("span.global-reviews-all a.a-link-emphasis.a-text-bold::attr(href)").getall()
            if not link:
                link = selector.css("a.a-link-emphasis.a-text-bold::attr(href)").get(0)
            if link:
                link_list.append(link)
                print(f"Found link in {filename}: {link}")
            else:
                print(f"No matching link found in {filename}")
    return link_list

directory="sites"
scrape_links(directory)