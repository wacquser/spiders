# -*- coding: utf-8 -*-
import scrapy
import urlparse
import time
from selenium import webdriver
from scrapy.http import Request
from qixinbao_crawler.items import QixinbaoCrawlerItem
from lxml import etree
import urllib2

import requests

class BasicSpider(scrapy.Spider):
    name = "qixinbao"
    # allowed_domains = ["web"]
    start_urls = (
        "http://www.qixin.com/login",
    )

    def get_cookies(self):
        driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.get( "http://www.qixin.com/login")
        driver.find_element_by_name("account").clear()
        driver.find_element_by_name("account").send_keys("15602235484")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("15602235484")
        time.sleep(5)
        driver.find_element_by_id("btnLogin").click()
        cookies = driver.get_cookies()
        return cookies, driver

    def get_last_url(self, driver, compay_url):
        base_url = "http://www.qixin.com/"
        para = "search?key=%s" %compay_url
        para += '&type=enterprise&method=all'
        driver.get(base_url + para)

        new_driver = driver.find_element_by_xpath('//*[@id="container-onlineSearch"]//div[@class="search-ent-left-content"]/a')
        new_url = new_driver.get_attribute('href')
        return new_url

    def parse(self, response):
        cookies, driver = self.get_cookies()
        list_of_company = self.get_company('qixinbao_crawler/company.txt')
        for company in list_of_company:
            encode_company = urllib2.quote(company)
            url = self.get_last_url(driver, encode_company)
            yield Request(url=url,
                           cookies=cookies,
                           meta={'cookies':cookies},
                           callback=self.extract_basic)

    def get_company(self, file):
        with open(file, 'r') as f:
            list_of_company = []
            for each in f.readlines():
                list_of_company.append(each.strip())
        return list_of_company

    def extract_basic(self, response):
        item = QixinbaoCrawlerItem()
        page = etree.HTML(response.body)

        company_name = page.xpath('//div[@class="company-card"]//h2/text()')
        item['gongsiming'] = company_name[0]
        result = {}
        tables = page.xpath('//table[@class="table table-bordered"]//tr')
        for tr in tables:
            tds_text = tr.xpath('.//td//text()')
            labels = []
            values = []
            tds = [each for each in tds_text if each != ' ']
            for i in range(0, len(tds)):
                if i % 2 == 0:
                    labels.append(tds[i])
                else:
                    values.append(tds[i])
            for m, n in zip(labels, values):
                result[m] = n
                # print m  + n + '\n'

        item['xinyongdaima'] = result[u'统一社会信用代码：']
        item['jigoudaima'] = result[u'组织机构代码：']
        item['zhucehao'] = result[u'注册号：']
        item['jingyingzhuangtai'] = result[u'经营状态：']
        item['gongsileixing'] = result[u'公司类型：']
        item['chengliriqi'] = result[u'成立日期：']
        item['faren'] = result[u'法定代表人：']
        item['yingyeqixian'] = result[u'营业期限：']
        item['zhuceziben'] = result[u'注册资本：']
        item['fazhaoriqi'] = result[u'发照日期：']
        item['dengjijiguan'] = result[u'登记机关：']
        item['qiyedizhi'] = result[u'企业地址：']
        item['jingyingfanwei'] = result[u'经营范围：']
        # item['ziranrengudong'] = result[u'自然人股东']

        yield item


    def write2file(self, response):
        print 'write2file'
        print response.url
        with open('source_new1.html', 'w') as file:
            file.write(response.body)


