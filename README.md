# Web Crawling Examples

This repository contains some crawling/scraping examples in Python. 
Prerequisites: create a virtual environment and install the requirements in requirements.txt.

## Web Crawling from scratch
This example includes a simple crawler written from scratch.
The crawler uses BeautifulSoup to parse web pages, and supports basic enforcements of 
`robots.txt` files. The crawler starts from a set of user-provided seed urls, 
and visits all links in a breadth-first fashion.
Each visited web page is saved in `crawler-scratch/output/` as an html file.
To start the crawler, run `crawler-scratch/crawler.py`. 

## Web Scraping from scratch
This example includes a simple scraper written from scratch, to extract talks data from 
https://luistar.github.io/talks/.
The scraper extends the Crawler of the previous example, supports basic pagination, and 
saves title and url of each talk in a csv file in `scraper-scratch/output`.
To start the scraper, run `scraper-scratch/scraper.py`. 

## Crawling and Scraping with Scrapy
The above examples have also been implemented using the well-known 
[Scrapy](https://scrapy.org) Python library.

### Web Crawling with Scrapy
The code for the Crawling example with Scrapy is in `crawler-scraper-scrapy/crawler/spiders/crawler.py`.
To start a crawl, move 
with a terminal to the `crawler-scraper-scrapy` directory, and run the command: `scrapy crawl crawler`.
Each visited page is saved as an html file.
Don't forget to change the path to the desired output directory in `crawler-scrapy/crawler/spiders/fetch_data.py`.

### Web Scraping with Scrapy
The code for the Scraping example with Scrapy is in `crawler-scraper-scrapy/crawler/spiders/talks_scraper.py`
To start the scraping, move with a terminal to the `crawler-scraper-scrapy` directory, 
and run the command:
`scrapy crawl talks_scraper -O output/talks.json`. Output will be saved to the `talks.json`
file in the `crawler-scraper-scrapy/output/` directory.