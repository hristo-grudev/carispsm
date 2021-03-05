import scrapy

from scrapy.loader import ItemLoader
from ..items import CarispsmItem
from itemloaders.processors import TakeFirst


class CarispsmSpider(scrapy.Spider):
	name = 'carispsm'
	start_urls = ['https://www.carisp.sm/category/news-carisp/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="read-more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="pagination"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h3[@class="heading"]/a/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="time"]/a/text()').get()

		item = ItemLoader(item=CarispsmItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
