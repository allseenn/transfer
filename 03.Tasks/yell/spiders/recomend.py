import scrapy
from scrapy.http import HtmlResponse
from yell.items import YellItem
from scrapy.loader import ItemLoader


class RecomendSpider(scrapy.Spider):
    name = "recomend"
    allowed_domains = ["irecommend.ru"]
    protocol = "https://"
    folder = "/content/"
    pages = 0
    url = ""
    ## file = "sait-geekbrains"
    #start_urls = ["https://irecommend.ru"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = f"{self.protocol}{self.allowed_domains[0]}{self.folder}{kwargs.get('query')}"
        #start = scrapy.FormRequest(url)
        #pages = int(self.parse_amount_of_pages(start))
        #self.start_url = [f"{self.protocol}{self.allowed_domains[0]}{self.folder}{kwargs.get('query')}"]
        self.start_urls = [self.url]

    def parse(self, response):
        try:
            self.pages = int(response.xpath('//li[@class="pager-last last"]/a/text()').get())
        except:
            self.pages = 1
        for i in range(self.pages):
            yield response.follow(f"{self.url}?page={i}", callback=self.parse_page)

    def parse_page(self, response):
        yells =  response.xpath('//a[@class="reviewTextSnippet"]/@href').getall()
        for yell in yells:
            yield response.follow(self.protocol+self.allowed_domains[0]+yell, callback=self.parse_yell)

    # def parse_yell(self, response):
    #     yell_text = response.xpath('//div[@itemprop="reviewBody"]//p/text()').getall()
    #     yell_verdict = response.xpath('//span[@class="verdict"]/text()').get()
    #     # print(yell_text)
    #     yield YellItem(text=yell_text, verdict=yell_verdict)
            
    def parse_yell(self, response: HtmlResponse):
        loader = ItemLoader(item=YellItem(), response=response)
        loader.add_xpath('header', '//h2[@class="reviewTitle"]//text()')
        loader.add_xpath('text', '//div[@itemprop="reviewBody"]//p/text()')
        loader.add_xpath('verdict', '//span[@class="verdict"]/text()')
        loader.add_value('link', response.url)
        yield loader.load_item()
        
