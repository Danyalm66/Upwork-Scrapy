# -*- coding: utf-8 -*-
import scrapy
from time import sleep
from selenium import webdriver


class BreazSpider(scrapy.Spider):
    name = 'breaz'
    
    start_urls = ['http://breazy.com/collections/juices/']
    #Enter the chrome driver's path 
    driver = webdriver.Chrome("path goes here")
    driver2 = webdriver.Chrome("path goes here")
    dont_filter=True

    count=1
    driver.get('https://breazy.com/collections/juices')
    driver2.get('https://breazy.com/collections/juices')
    
    def parse(self, response):
        print 'Sleeping for 3 second..'
        sleep(3)
        #Getting all the urls from the shown page
        product_urls=self.driver.find_elements_by_xpath('//*[@id="hits"]/a')
        for i in product_urls:
            dic={}            
            
            pr_url=i.get_attribute('href')

            #Opening a new product's page to scrape price and size
            self.driver2.get(pr_url)    
            sleep(2)
            #Skip not required products
            skip=self.driver2.find_elements_by_xpath('//*[@id="buying-options-container"]/div[2]/div[2]/div[1]/span')
            if len(skip)>0:       
                continue
            #Getting prices
            price=''
            pricesearch=self.driver2.find_elements_by_xpath('//*[@class="price-value product-page-price-value"]')
            if len(pricesearch)>0:
                price=pricesearch[0].text
            else:
                price=self.driver2.find_element_by_xpath('//*[@class="price-val product-page-price-value"]').text
            #Getting Size    
            sizeurl=self.driver2.find_elements_by_xpath('//*[@id="add-product-form"]/div[2]/div[1]/div[2]/div')
            size=''
            if len(sizeurl)>0:
                size=sizeurl[0].text
            #Getting Title
            title=i.find_element_by_xpath('./div/div[@class="action-product-name truncate"]').text
                
            dic['Title']=title
            dic['Price']=price
            dic['Size']=size
            dic['Product Url']=pr_url
            #Yielding data to the required output file 
            yield dic
        yield scrapy.Request(self.driver.current_url, callback=self.nextpage)
        
            
        
    #converst selenium object into product urls
    def geturls(self, arg):
        
        allurls=[]
        for i in arg:
            allurls.append(i.get_attribute('href'))
        return allurls

    #paginating over each page
    def nextpage(self,response):
        
      if self.count<50:
            try:
                self.driver.find_element_by_xpath('//span[@class="next"]/a').click()
                print 'Sleeping for 5 seconds...'
                sleep(5)
            except:
                #To bypass email pop up
                find=self.driver.find_elements_by_xpath('//*[@id="privy-inner-container"]/div[1]/div/div/div[3]/div[3]/button')
                if len(find)>0:
                    find[0].click()
                    print 'Sleeping for 5 seconds...'
                    sleep(5)
                self.driver.find_element_by_xpath('//span[@class="next"]/a').click()
                print 'Sleeping for 1 seconds...'
                sleep(1)
            
            self.count+=1
            yield scrapy.Request(self.driver.current_url, callback=self.parse)
            

            
