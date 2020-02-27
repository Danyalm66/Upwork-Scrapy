# -*- coding: utf-8 -*-
import scrapy


class BrandSpider(scrapy.Spider):
    name = 'brand'
    
    start_urls = ['http://www.elementvape.com/brands/']

    def parse(self, response):
        all_prd=response.xpath('//*[@class="brand-title"]/a/@href').extract()
        for a in all_prd:
            yield scrapy.Request(a, callback=self.all_products)


    def all_products(self,response):
        all_products=response.xpath('//a[starts-with(span,"All")]/@href').extract_first()
        
        if all_products:
            yield scrapy.Request(all_products, callback=self.products)
        else:
            yield scrapy.Request(response.url, self.products)

    def products(self,response):
        prod_urls=response.xpath('//*[@class="product-name"]/a/@href').extract()
        for p in prod_urls:
            yield scrapy.Request(p, callback=self.product_page)

    def product_page(self,response):
        dic={}
        title=response.xpath('//*[@class="productdetail-name"]/text()').extract_first()
        prod_url=response.url
        price=response.xpath('//*[@class="special-price"]/span/text()').extract_first().strip()
        availability=response.xpath('//*[@class="availability"]/p/strong/text()').extract_first()
        dic['Title']=title
        dic['Price']=price
        dic['Availability']=availability
        dic['Product Url']=prod_url
        yield dic
