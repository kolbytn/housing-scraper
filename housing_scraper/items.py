# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

class HousingScraperItem(scrapy.Item): 
   name = scrapy.Field() 
   url = scrapy.Field() 
   desc = scrapy.Field() 
