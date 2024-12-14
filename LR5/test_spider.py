import os
if os.name == 'nt':  # Windows OS
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from quotes_project.spiders.quotes_spider import QuotesSpider  # Импорт паука

process = CrawlerProcess(get_project_settings())
process.crawl(QuotesSpider)
process.start()
