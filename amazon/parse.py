from bs4 import BeautifulSoup
import os

def extract_links(html_file):
  if not os.path.exists(html_file):
    print(f"Error: HTML file not found: {html_file}")
    return None
  with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()
  soup = BeautifulSoup(html_content, 'html.parser')
  links = soup.find_all('a', class_=['a-link-emphasis', 'a-text-bold'])
  extracted_hrefs = [link['href'] for link in links]
  return extracted_hrefs

html_file = 'amaze-B0BCF54SR1.html'
extracted_hrefs = extract_links(html_file)

if extracted_hrefs:
  print("Extracted hrefs:")
  print(len(extracted_hrefs))
  for href in extracted_hrefs:
    print(href)
else:
  print("No links with the specified classes found")
