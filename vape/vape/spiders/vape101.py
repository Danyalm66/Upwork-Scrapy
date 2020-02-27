# -*- coding: utf-8 -*-
import scrapy


class Vape101Spider(scrapy.Spider):
    name = 'vape101'

    start_urls = ['http://101vape.com/brands.html/']

    def parse(self, response):
        brand_title=response.xpath('//*[@class="brand-image"]/a/@href').extract()
        for a in brand_title:
            yield scrapy.Request(a+'?product_list_limit=all', callback=self.products)
        for b in brand_title:
            yield scrapy.Request(b+'?product_list_limit=15', callback=self.products)
        for c in brand_title:
            yield scrapy.Request(c+'?product_list_limit=30', callback=self.products)
        for d in brand_title:
            yield scrapy.Request(b+'?product_list_limit=9', callback=self.products)
            
        nextpage=response.xpath('//li[@class="item pages-item-next"]/a/@href').extract()
        if len(nextpage)>0:
        
            yield scrapy.Request(nextpage[0])
        

    def products(self,response):
        pro_url=response.xpath('//h3[@class="product-name"]/a/@href').extract()
        for i in pro_url:
            yield scrapy.Request(i, callback=self.product_page)
    
    def product_page(self,response):
        dic={}
        title=response.xpath('//h1[@class="page-title"]/span/text()').extract_first()
        url=response.url
        sku=response.xpath('//div[@class="product attribute sku"]/div/text()').extract_first().strip()
        price=response.xpath('//span[@class="price"]/text()').extract_first()
        dic['Title']=title
        dic['Price']=price
        dic['SKU']=sku
        dic['Product Url']=url
        yield dic
            
