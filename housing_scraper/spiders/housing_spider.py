import scrapy
import re
import csv

min_price = 600
max_price = 900
min_bed = 2
ne_lat = 40.254775
ne_long = -111.661492
sw_lat = 40.240411
sw_long = -111.686466

class HousingSpider(scrapy.Spider):
    name = "housing_spider"
    start_urls = [
        'https://www.rentler.com/places-for-rent/?minprice={}&maxprice={}&minbedrooms={}&ne.lat={}&ne.lon={}&sw.lat={}&sw.lon={}'
            .format(min_price, max_price, min_bed, ne_lat, ne_long, sw_lat, sw_long)]

    def parse(self, res):

        if 'rentler' in res.url:
            
            selector = '#listings .listing'
            for listing in res.css(selector):
                listing_url = listing.css('a ::attr(href)').extract_first()
                yield scrapy.Request(
                    res.urljoin(listing_url[:-2]),
                    callback=self.parse_rentler_listing
                )

    def parse_rentler_listing(self, res):
        address_selector = "span[itemprop='streetAddress'] ::text"
        price_selector = "span[itemprop='price'] ::text"
        available_selector = ".available h3 ::text"
        phone_selector = ".card .table tr:first-of-type td:first-of-type a ::text"
        desc_selector = "#description + p ::text"

        address = res.css(address_selector).re(r'[\w ]+')
        price = res.css(price_selector).re(r'[0-9.]+')
        availability = res.css(available_selector).re(r'([0-9/]+|Available now)')
        phone = res.css(phone_selector).re(r'[0-9 ()\-]+')

        address = address[0] if len(address) > 0 else "No address"
        price = price[0] if len(price) > 0 else "No price"
        availability = availability[0] if len(availability) > 0 else "No availability"
        phone = phone[0] if len(phone) > 0 else "No phone"

        yield {
            'address': address,
            'price': price,
            'availability': availability,
            'phone': phone
        }

        with open('results/rentler.csv', mode='a') as file:
            writer = csv.writer(file, delimiter=',')

            writer.writerow([address, price, availability, phone])
