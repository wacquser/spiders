# -*- coding = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in = scrapy.Field()
# http = scrapy.Field()

import scrapy

class EmploymentItem(scrapy.Item):

    # positionId = scrapy.Field()
    positionName = scrapy.Field()
    createTime = scrapy.Field()
    companyName = scrapy.Field()
    companyShortName = scrapy.Field()
    city = scrapy.Field()
    category = scrapy.Field()
    mainCategory = scrapy.Field()
    workYear = scrapy.Field()
    bonus = scrapy.Field()
    salary = scrapy.Field()
    education = scrapy.Field()
    workKind = scrapy.Field()
    financeStage = scrapy.Field()
    industryField = scrapy.Field()
    companySize = scrapy.Field()
    companyLabelList = scrapy.Field()
    pvScore = scrapy.Field()
    job_desc = scrapy.Field()
    company_website = scrapy.Field()
    page_url = scrapy.Field()
