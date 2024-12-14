import scrapy
from scrapy_splash import SplashRequest
import pymongo

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js/"]

    # Подключение к MongoDB
    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient("mongodb://localhost:27017/PSU")
        self.db = self.client["JuralDetails"]  # Имя базы данных
        self.collection = self.db["quotes_result"]  # Имя коллекции

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
                args={'wait': 1},  # Задержка для загрузки JS
            )

    def parse(self, response):
        quotes = response.css("div.quote")
        for quote in quotes:
            item = {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("span small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }
            # Сохраняем данные в MongoDB
            if item['text']:
                self.collection.insert_one(item)
            else:
                self.logger.warning('Skipping item due to missing text: %s', item)



        # Переход на следующую страницу, если она существует
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield SplashRequest(
                response.urljoin(next_page),
                self.parse,
                args={'wait': 1},
            )
