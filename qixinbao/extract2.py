#-*- coding: UTF-8 -*-
from lxml import etree


file = open('source_new1.html', 'r')
content = file.read()
page = etree.HTML(content)

def extract_basic(page):
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
        # values = [label[i] for i in range(0, len(tds)) for label in tds  if i // 2 != 0]

        result = {}
        for m, n in zip(labels, values):
            result[m] = n
            print m  + n + '\n'
        # print result
    # for each in tables:
    #     print each
    # print tables
    # print len(tables)


# extract_basic(page)
# test = page.xpath('//div[@class="row"]/div[contains(@class, "col")]')
def extract_card(page):
    company_name = page.xpath('//div[@class="company-card"]//h2/text()')
    company_card = page.xpath('//div[@class="company-card"]//div[@class="company-info-item clearfix"]')

    print company_name[0]
    print company_card
    result = {}
    for card in company_card:
        label = card.xpath('./div[@class="company-info-item-label"]/text()')
        # if label:
        #     label = label[0]
        # value = card.xpath('./div[@class="company-info-item-text"]/*/text()')
        value = card.xpath('./div[@class="company-info-item-text"]//text()')
        href = card.xpath('./div[@class="company-info-item-text"]//a/@href')
        if href:
            value = href[0]
        else:
            if value:
                if value[0] == ' ':
                    value = value[1]
                else:
                    value = value[0]
        print label[0],value

extract_card(page)

