import scrapy
from fitness_first.items import Product
from lxml import html

class Fitness_firstSpider(scrapy.Spider):
    name = "fitness_first"
    start_urls = ["https://www.fitnessfirst.co.uk/find-a-gym"]

    def parse(self, response):
        parser = html.fromstring(response.text)
        xpath_stores_urls = "//li[@class='location-list-item']/a/@href"
        stores_urls = parser.xpath(xpath_stores_urls)
        for each_url in stores_urls:
            yield Product(**{'url': each_url})