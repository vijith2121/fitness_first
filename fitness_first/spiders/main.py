import scrapy
# from fitness_first.items import Product
from lxml import html

class Fitness_firstSpider(scrapy.Spider):
    name = "fitness_first"
    start_urls = ["https://example.com"]

    def parse(self, response):
        parser = html.fromstring(response.text)
        print("Visited:", response.url)
