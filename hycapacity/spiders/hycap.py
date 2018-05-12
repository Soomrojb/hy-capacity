# -*- coding: utf-8 -*-
# @author:  Janib Soomro
# @e-mail:  soomrojb@gmail.com
# @skype:   soomrojb
# @dated:   12th May. 2018

import scrapy
from scrapy.utils.response import open_in_browser

BaseURL = "https://www.hy-capacity.com"
LoginURL = BaseURL + "/assets/scripts/ajax-login.php"
TargetURL = "https://www.hy-capacity.com/assets/scripts/ajax-login.php"
TestLink = "https://www.hy-capacity.com/?page=Search&partid="
Credentials = ["12114", "1nv0k3"]

class HycapSpider(scrapy.Spider):
    name = 'hycap'
    allowed_domains = ["www.hy-capacity.com"]

    def start_requests(self):
        Params = {
            'user' : Credentials[0],
            'pass' : Credentials[1],
            'query' : 'login',
            'remember' : 'true'
        }
        yield scrapy.FormRequest(LoginURL, formdata=Params, callback=self.parse, method="POST")

    def parse(self, response):
        yield scrapy.FormRequest(BaseURL, callback=self.afterlogin, method="GET")

    def afterlogin(self, response):
        for Loop in range(1, 75000):
            NewLink = TestLink + str(Loop)
            yield scrapy.Request(NewLink, callback=self.parsepost, method="POST", meta=response.meta)
    
    def parsepost(self, response):
        ImageObj = []
        PostTitle = response.xpath("//div[@class='results-description' and contains(@id,'description-')]/text()").extract()
        Price = response.xpath("normalize-space(//div[contains(text(),'Sugg.') and @class='results-core'])").extract()
        CrossRefNumb = response.xpath("//li[@class='details-header']/div[text()='Cross Reference Numbers']/../following-sibling::li/text()").extract()
        ProductNotesHtml = response.xpath("//li[text()='Product Notes' and @class='details-header']/..")
        Manufacturer = response.xpath("//div[@id='row-partapplications']/div[@id='apps-mfg-2']/div[1]/text()").extract()
        Category = response.xpath("//li[contains(@style,'background-color:#FF6600')]/a/text()").extract()
        ProductCode = response.xpath("//div[@class='results-itemnum']/span/text()").extract()
        CurrentImage = response.xpath("//div[contains(@id,'detailsimages-')]/div[contains(@id,'detailsimages-currentimage-')]/img/@src").extract()
        for Images in response.xpath("//div[@id='photonav']/div[@class='photothumb']"):
            ImageObj += Images.xpath("./img/@src").extract()
        yield {
            "Post URL" : response.url,
            "Post Title" : PostTitle,
            "Price" : Price,
            "Porduct Notes (Html)" : ProductNotesHtml.extract(),
            "Cross Ref. Number" : CrossRefNumb,
            "Manufacturer" : Manufacturer,
            "Category" : Category,
            "Product Code" : ProductCode,
            "Current Image" : CurrentImage,
            "Remaining Images" : ImageObj
        }
