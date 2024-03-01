

from scrapy import Spider
from scrapy.selector import Selector
from stack.items import StackItem


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "https://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    def parse(self, response):
            questions = Selector(response).xpath('//div[@class="s-post-summary--content"]/h3')

            for question in questions:
                item = StackItem()
                item['title'] = question.xpath('a[@class="s-link"]/text()').extract()[0]
                item['url'] = question.xpath('a[@class="s-link"]/@href').extract()[0]
                yield item
            

'''

We are iterating through the `questions` and assigning the `title` and `url` values from the scraped data. Be sure to test out the XPath selectors in the JavaScript Console within Chrome Developer Tools - e.g., `$x('//div[@class="summary"]/h3/a[@class="question-hyperlink"]/text()')` and `$x('//div[@class="summary"]/h3/a[@class="question-hyperlink"]/@href')`.

$ scrapy crawl stack



'''
