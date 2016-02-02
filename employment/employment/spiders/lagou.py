import scrapy
import json

from employment.items import EmploymentItem

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    start_urls = ['http://www.lagou.com/']

    def parse(self, response):
        lables = response.xpath('//div[@class="menu_box"]//dd/a/text()').extract()
        pre_url = 'http://www.lagou.com/jobs/positionAjax.json'

        # for each in lables[:1]:
        for each in lables:
            for index in range(1,31):
                if index == 1:
                    filldata={'first':'True','pn':'1','kd':'%s' % (each)}
                else:
                    filldata={'first':'False','pn':'%d' %(index) ,'kd':'%s' % (each)}
                yield scrapy.FormRequest(pre_url, formdata=filldata, callback=self.extract)

    def extract(self, response):

        jsonresponse = json.loads(response.body)

        for each in jsonresponse["content"]["result"]:
            item = EmploymentItem()
            page_url = 'http://www.lagou.com/jobs/' + str(each["positionId"]) + '.html'

            item['positionName'] =  each["positionName"]
            item['createTime'] =  each["formatCreateTime"]
            item['companyName'] =  each["companyShortName"]
            item['companyShortName'] =  each["companyName"]
            item['city'] =  each["city"]
            item['category'] =  each["positionType"]
            item['mainCategory'] =  each["positionFirstType"]
            item['workYear'] =  each["workYear"]
            item['bonus'] =  each["positionAdvantage"]
            item['salary'] =  each["salary"]
            item['education'] =  each["education"]
            item['workKind'] =  each["jobNature"]
            item['financeStage'] =  each["financeStage"]
            item['industryField'] =  each["industryField"]
            item['companySize'] =  each["companySize"]
            item['companyLabelList'] =  each["companyLabelList"]
            item['pvScore'] =  each["pvScore"],
            item['page_url'] = page_url

            yield scrapy.Request(page_url,self.parse_page, meta={'item':item})

    def parse_page(self, response):
        item = response.meta['item']
        job_desc_selector = response.xpath('//dd[@class="job_bt"]//text()')
        company_website_selector = response.xpath('//ul[@class="c_feature"]//a/@href')
        item['job_desc'] = job_desc_selector.extract() if job_desc_selector else None
        item['company_website'] = company_website_selector[0].extract() if company_website_selector else None
        yield item




