# -*- coding: utf-8 -*-
import scrapy


class CompaniesSpider(scrapy.Spider):
    name = 'companies'
    start_urls = ['http://www.lctconnect.com/limousine-companies/city-serviced-01:countries_united_states//']

    def parse(self, response):
        products=response.xpath('//a[@class="link-large"]/@href').extract()
        for product in products:
            yield scrapy.Request(product, callback=self.page)

        url=response.xpath('//*[@class="navigator rs"]/a/@href').extract_first()
        if url:
            yield scrapy.Request(url)

    def page(self,response):
        dic={}
        headers=response.xpath('//div[@class="name"]')
        count=1
        emails=response.xpath('//*[@class="static"]/@href').extract()
        for e in emails:
                cfemail= e.split("#").pop()
                encoded_bytes = bytearray.fromhex(cfemail)
                email=str(bytearray(byte ^ encoded_bytes[0] for byte in encoded_bytes[1:]))
                dic['Email #'+str(count)]=email
                count=count+1
        for i in headers:
            header = i.xpath('./@title').extract_first()
            data= i.xpath('./following-sibling::div/text()').extract_first()
            links=['Company Website']
            if header in links:
                data= i.xpath('./following-sibling::div/a/text()').extract_first()
            try:
                dic[header.strip()]=data.strip()
            except AttributeError:
                continue
        yield dic

    
