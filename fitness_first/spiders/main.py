import scrapy
from fitness_first.items import Storelocation_Others, Storelocation
from lxml import html
import json

class Fitness_firstSpider(scrapy.Spider):
    name = "fitness_first"
    start_urls = ["https://www.fitnessfirst.co.uk/find-a-gym"]

    def parse(self, response):
        parser = html.fromstring(response.text)
        xpath_stores_urls = "//li[@class='location-list-item']/a/@href"
        stores_urls = parser.xpath(xpath_stores_urls)
        for each_url in stores_urls:
            url = f"https://www.fitnessfirst.co.uk{each_url}"
            yield scrapy.Request(url, callback=self.parse_store)

    def parse_store(self, response):
        parser = html.fromstring(response.text)
        xpath_store = '//script[@type="application/ld+json"]/text()'
        xpath_lat_lng = "//a[contains(text(), 'See in maps')]/@href"
        stores = json.loads("".join(parser.xpath(xpath_store)))
        try:
            lat_lng = "".join(parser.xpath(xpath_lat_lng)).split('/')[-2]
            latitude = lat_lng.split(',')[0].replace('@', '')
            longitude = lat_lng.split(',')[1]
        except Exception as error:
            latitude = ""
            longitude = ""
            self.logger.warning(error)
        for store in stores:
            name = store.get('name', '')
            phone = store.get('telephone', '')
            email = store.get('email', '')
            address = store.get('address', {})
            street = address.get('streetAddress', '')
            city = address.get('addressLocality', '')
            zipcode = address.get('postalCode', '')
            country = address.get('addressCountry', '')
            store_type = store.get('@type', '')
            extras = {'Email': email, 'Store Type': store_type}
            extras = {extra: item for extra, item in extras.items() if item}
            locations = {
                'Provider': 'fitness_first',
                'DateUpdated': '',
                'StoreId': "",
                'Name': name,
                'Street': street,
                'City': city,
                'State': "",
                'ZipCode': zipcode,
                'Phone': phone,
                'OpenHours': "",
                'Latitude': latitude,
                'Longitude': longitude,
                'Url': response.url,
                'Extras': json.dumps(extras) if extras else "",
                'Status': "Open",
            }
            if country == 'GB':
                locations['Country'] = 'UK'
                locations['ProviderId'] = '55430'
                yield Storelocation(**locations)
            else:
                locations['Country'] = country
                locations['ProviderId'] = '0'
                yield Storelocation_Others(**locations)