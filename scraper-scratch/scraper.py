import logging
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)


class BasicScraper:
    USER_AGENT = "tecwebuninabot"
    OUTPUT_DIR = "output/"

    def __init__(self, seed_urls=[], allowed_domains=[], ignore_robots_txt=False):
        self.frontier = seed_urls
        self.allowed_domains = allowed_domains
        self.ignore_robots_txt = ignore_robots_txt
        self.visited_urls = []
        self.current_extracted_data_counter = 0
        self.robots_policies_dict = {}

    def fetch(self, url):
        headers = {
            'User-Agent': self.USER_AGENT
        }
        return requests.get(url, headers=headers).text

    def explore(self, url):
        self.visited_urls.append(url)  # mark url as visited
        html = self.fetch(url)  # fetch html document at url
        self.extract_data(html)  # extract and save relevant data
        links = self.parse_links(url, html)  # parse html document and get outgoing links
        self.filter_and_append_links(links)

    def extract_data(self, html):
        document = BeautifulSoup(html, 'html.parser')
        for article in document.find_all('article', {'class': 'resource-item'}):
            title_element = article.find('a', {'class': 'pub-title'})
            href = title_element.get("href")
            title = title_element.text
            with open(f"{self.OUTPUT_DIR}/talks.csv", "a+", encoding="utf-8") as output:
                output.write(f"{self.current_extracted_data_counter}, {title}, {href}\n")
                logging.debug(f"Saved item {self.current_extracted_data_counter}, {title}, {href}")
                self.current_extracted_data_counter = self.current_extracted_data_counter + 1
        return

    def is_processing_allowed_by_robots_txt(self, link):
        if not self.ignore_robots_txt:
            robots_policy = self.get_robots_exclusion_policy(link)
            return robots_policy.can_fetch(self.USER_AGENT, link)
        else:
            return True

    def get_robots_exclusion_policy(self, url):
        robots_url = urljoin(url, "/robots.txt")
        if robots_url not in self.robots_policies_dict:
            robots_exclusion_policy = RobotFileParser(robots_url)
            logging.info(f"Parsing robots.txt from {robots_url}")
            robots_exclusion_policy.read()
            self.robots_policies_dict.update({robots_url: robots_exclusion_policy})

        return self.robots_policies_dict.get(robots_url)

    def filter_and_append_links(self, links):
        for link in links:
            # skip if link points to non-allowed domain
            if urlparse(link).netloc not in self.allowed_domains:
                logging.debug(f"Skipped non-allowed domain: {link}")
                continue

            # skip if automatic processing is forbidden by robots.txt specification
            if not self.is_processing_allowed_by_robots_txt(link):
                logging.info(f"Skipped because forbidden by robots.txt: {link}")
                continue
            else:
                logging.info(f"{link} allowed by robots.txt")

            if link not in self.visited_urls and link not in self.frontier:
                logging.debug(f"Appending to frontier: {link}")
                self.frontier.append(link)

    def parse_links(self, url, html):
        document = BeautifulSoup(html, 'html.parser')
        next = document.find('li', {'class': 'next'})
        next_link = next.find('a').get("href")
        if next_link and next_link.startswith('/'):
            next_link = urljoin(url, next_link)
        return [next_link]

    def start(self):
        while self.frontier:
            url = self.frontier.pop(0)
            logging.info(f"Crawling {url}")
            try:
                self.explore(url)
            except Exception as e:
                logging.exception(f"Failed to explore {url}: {e}")
            finally:
                self.visited_urls.append(url)
        logging.info("Crawl complete.")


if __name__ == '__main__':
    BasicScraper(seed_urls=["https://luistar.github.io/talks/"],
                 allowed_domains=["luistar.github.io"],
                 ignore_robots_txt=False
                 ).start()
