# import os
# import json
# from scrapy.crawler import CrawlerProcess
# from scrapy.spiders import Spider

import os
from multiprocessing import Process
import json
import scrapy
import re
import requests
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


class CryptoNewsSpider(scrapy.spiders.Spider):
    name = 'cryptonews_spider'

    def start_requests(self):
        urls = ['https://www.okx.com/support/hc/en-us/sections/360000030652-Latest-Announcements']#, 'https://www.binance.com/ru/support/announcement/?c=48', 'https://cryptonews.net/news/top/', 'https://cryptodaily.co.uk/tag/defi', 'https://cryptodaily.co.uk/tag/altcoins']
        
        headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
        headers_okx = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        
        for url in urls:
            if 'www.okx.com' in url:
                yield scrapy.Request(url=url, callback=self.parse, headers=headers_okx)
            else:
                yield scrapy.Request(url=url, callback=self.parse, headers=headers)


    def parse(self, response):
        if response.url == 'https://news.bitcoin.com':
            list_of_news = response.xpath('//div[@class="story--medium__info"]/a/@href').getall()

            for news in list_of_news:
                yield {'link': news}  

        elif response.url == 'https://cryptonews.net/news/top/':
            list_of_news = response.xpath('//div[@class="row news-item start-xs"]/@data-link').getall()

            for news in list_of_news:
                yield {'link': news} 

        elif 'https://cryptodaily.co.uk' in response.url:
            list_of_news = response.xpath('//a[@class="post-item"]/@href').getall()

            for news in list_of_news:
                yield {'link': news} 

        elif 'www.binance.com' in response.url:
            jsonnews = response.xpath('//script[@id="__APP_DATA"]/text()').get()
            list_of_news = json.loads(jsonnews)['pageData']['redux']['ssrStore']['latestArticles']['announcement']

            for news in list_of_news:
                yield {'link': f'https://www.binance.com/ru/support/announcement/{news["code"]}'} 

        elif 'www.okx.com' in response.url:
            list_of_news = response.xpath('//a[@data-monitor="article"]/@href').getall()

            for news in list_of_news:
                yield {'link': f'https://www.okx.com{news}'} 


def cryptonews_spider_getter():
    os.remove('/home/ubuntu/Cryptonews_bot/newssaved_new.txt')

    process = CrawlerProcess(settings={
        'FEEDS': {
            "cryptonews.json": {"format": "json"},
        },
    })

    with open('/home/ubuntu/Cryptonews_bot/newssaved_general.txt', 'r') as r:
        newssaved = r.readlines()
        newssaved_list = list(map(lambda x: x.strip('\n'), newssaved))


    process.crawl(CryptoNewsSpider)
    process.start()

    lst = []

    with open('/home/ubuntu/Cryptonews_bot/cryptonews.json') as f:
        file = json.load(f)
        for i in file:
            lst.append(i['link'])

    os.remove('/home/ubuntu/Cryptonews_bot/cryptonews.json')

    a = set(lst).difference(set(newssaved_list))
    a = list(a)

    if a != []:
        with open('/home/ubuntu/Cryptonews_bot/newssaved_general.txt', 'a') as f:
            for link in a:
                f.write(f'{link}\n')

        with open('/home/ubuntu/Cryptonews_bot/newssaved_new.txt', 'w') as f:
            for link in a:
                f.write(f'{link}\n')

