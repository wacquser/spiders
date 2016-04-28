# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import os,shutil

class NationalData():
    def __init__(self):
        fp = webdriver.FirefoxProfile()

        # fp.set_preference("browser.download.folderList", 0) # 下载到桌面
        fp.set_preference("browser.download.folderList",2)
        self.download_dir = os.getcwd()+'\data'
        fp.set_preference("browser.download.dir", self.download_dir)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream, application/vnd.ms-excel,  text/csv, application/zip")

        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.base_url = "http://data.stats.gov.cn/easyquery.htm?cn=A01"
        self.verificationErrors = []
        self.accept_next_alert = True

    def download(self, username, password, read_file, log_file):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text(u"登录").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("keyp").clear()
        driver.find_element_by_id("keyp").send_keys(password)
        driver.find_element_by_id("auto_login").click()
        driver.find_element_by_id("submitBtn").click()
        driver.find_element_by_link_text(u"月度数据").click()
        download_count = 0
        error_count = 0
        error_download = {}
        with open(log_file, 'a+',  encoding='utf-8') as logfile:
            with open(read_file, 'r', encoding='utf-8') as file:
                for row in file.readlines():
                    if row != '\n':
                        if not row.strip().endswith('.xls'): # 不是以xls结尾的那行就是父级标签，只需要点击该标签即可
                            try:
                                driver.find_element_by_id(row.strip()).click()
                            except:
                                time.sleep(2)
                                driver.find_element_by_id(row.strip()).click()
                        else:
                            try_times = 0
                            id_label, absolute_file_name = row.strip().split(' ')
                            temp_name = absolute_file_name.split('/')
                            dir_name = self.download_dir + '/' + '/'.join(temp_name[:-1]) # 构建下载文件的路径
                            if not os.path.exists(dir_name):
                                os.makedirs(dir_name)
                            while try_times != 3:
                                try:
                                    driver.find_element_by_id(id_label).click()
                                    driver.find_element_by_css_selector("a.download.mr20").click()
                                    driver.find_element_by_id("excel").click() # 不能下载csv，只能为excel
                                    driver.find_element_by_css_selector("div.doneDodnload.btn").click()
                                    time.sleep(3) # 下载文件需要一定的时间
                                    shutil.move('data/月度数据.xls', self.download_dir+'/'+absolute_file_name) # 将下载的文件移动到准确的位置上
                                    download_count += 1
                                    time.sleep(3) # 移动文件需要一定的时间
                                    break
                                except Exception as e:
                                    try_times += 1
                                    print('\nwrong downloading: {}'.format(absolute_file_name))
                                    print('exception: {}'.format(e))
                                    print('This is the {} time to try'.format(try_times))

                                    logfile.write('\nwrong downloading: {}'.format(absolute_file_name))
                                    logfile.write('exception: {}'.format(e))
                                    logfile.write('This is the {} time to try'.format(try_times))
                                    logfile.flush()

                                    if try_times == 3:
                                        error_download[id_label] = absolute_file_name
                                        error_count += 1
                                        continue
                    else:
                        continue
            print('成功下载文件数量：{}个\n'.format(download_count))
            print('下载失败文件数量：{}个\n'.format(error_count))

            logfile.write('成功下载文件数量：{}个\n'.format(download_count))
            logfile.write('下载失败文件数量：{}个\n'.format(error_count))

            if len(error_download) != 0:
                self.redownload(error_download, log_file)

    def redownload(self, dict, log_file):
        with open(log_file, 'a+',  encoding='utf-8') as logfile:
            print('正在尝试重新下载之前下载失败的文件...')
            print('出错的文件有以下这些：')

            logfile.write('正在尝试重新下载之前下载失败的文件...\n')
            logfile.write('出错的文件有以下这些：\n')

            for id_label, absolute_file_name in dict.items():
                print(id_label + ' : ' + absolute_file_name)
                logfile.write(id_label + ' : ' + absolute_file_name +'\n')

            driver = self.driver
            error_download = []
            redownload_count = 0
            redownload_error_count = 0
            for id_label, absolute_file_name in dict.items():
                try:
                    driver.find_element_by_id(id_label).click()
                    driver.find_element_by_css_selector("a.download.mr20").click()
                    driver.find_element_by_id("excel").click() # 不能下载csv，只能为excel
                    driver.find_element_by_css_selector("div.doneDodnload.btn").click()
                    time.sleep(2) # 下载文件需要一定的时间
                    shutil.move('data/月度数据.xls', self.download_dir+'/'+absolute_file_name) # 将下载的文件移动到准确的位置上
                    redownload_count += 1
                    time.sleep(2) # 移动文件需要一定的时间
                except Exception as e:
                    print('wrong downloading: {}'.format(absolute_file_name))
                    print('exception: {}'.format(e))

                    logfile.write('\nwrong downloading: {}'.format(absolute_file_name))
                    logfile.write('exception: {}'.format(e))

                    error_download.append(absolute_file_name)
                    redownload_error_count += 1
                    continue
                time.sleep(3)
            print('重新下载成功文件数量：{}'.format(redownload_count))
            logfile.write('重新下载成功文件数量：{}\n'.format(redownload_count))
            if len(error_download) != 0:
                print('重新下载仍然失败，需要手动下载如下文件：')
                logfile.write('重新下载仍然失败，需要手动下载如下文件：\n')
                for each in error_download:
                    print(each + '\n')
                    logfile.write(each + '\n')

if __name__ == "__main__":

    username = ""
    password = ""

    username = "kylinlingh@163.com"
    password = "lin0607103014"

    intermediate_file_name = 'intermediate.txt'
    log_file_name = 'log.log'

    begintime = time.ctime()
    with open(log_file_name, 'a+', encoding='utf-8') as file:
        print('开始时间：{}'.format(begintime))
        file.write('开始时间：{}'.format(begintime))

    NationalData().download(username, password, intermediate_file_name, log_file_name)
    endtime = time.ctime()

    with open(log_file_name, 'a+', encoding='utf-8') as file:
        print('结束时间：{}'.format(endtime))
        file.write('\n结束时间：{}'.format(endtime))

