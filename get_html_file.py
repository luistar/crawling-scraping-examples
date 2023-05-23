import requests

headers = {
    'User-Agent': "tecwebuninabot"
}

# try to scrape a Single Page React app
html_page = requests.get("https://tecweb-2023-scraping-examples.tiiny.site/scraping-v3/").text
print(html_page)  # not much content there!