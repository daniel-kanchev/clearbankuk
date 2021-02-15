import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from clearbankuk.items import Article


class ClearSpider(scrapy.Spider):
    name = 'clear'
    allowed_domains = ['clear.bank']
    start_urls = ['https://www.clear.bank/newsroom/']

    def parse(self, response):
        links = response.xpath('//article//a[@class="hehaa0-2 eNdNf"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h3/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//time/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="sc-10k4rcu-1 MmchF"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
