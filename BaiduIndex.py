# -*- coding:utf-8 -*-

from selenium import webdriver
from PIL import Image, ImageOps
from selenium.webdriver.common.action_chains import ActionChains
from Setting import *
import pandas as pd
import time
import pytesseract
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')


class BDIndexProcessor:
    def __init__(self):
        self.__browser = None
        self.__df = None
        self.__list_date = []
        self.__list_index = []
        self.__NoBaiduIndex = []
        self.__used = []
        pass

    def open_browser(self):
        url = "http://index.baidu.com/"
        self.__browser = webdriver.Chrome()
        self.__browser.get(url)
        # 点击网页的登录按钮
        pass

    def close_browser(self):
        self.__browser.close()
        pass

    def log_in(self, account, pass_word):
        self.__browser.find_element_by_xpath("//ul[@class='usernav']/li[4]").click()
        time.sleep(3)
        try:
            self.__browser.find_element_by_id("TANGRAM_11__password").send_keys(pass_word)
            self.__browser.find_element_by_id("TANGRAM_11__userName").send_keys(account)
            self.__browser.find_element_by_id("TANGRAM_11__submit").click()
        except Exception as e:
            print(e)
            self.__browser.find_element_by_id("TANGRAM_12__password").send_keys(pass_word)
            self.__browser.find_element_by_id("TANGRAM_12__userName").send_keys(account)
            self.__browser.find_element_by_id("TANGRAM_12__submit").click()
        time.sleep(2)
        pass

    def open_index_page(self, key_word, begin, end):
        # self.__browser.maximize_window()
        self.__browser.find_element_by_id("schword").clear()
        self.__browser.find_element_by_id("schword").send_keys(key_word)
        try:
            self.__browser.find_element_by_id("searchWords").click()
        except Exception as e:
            print(e)
            self.__browser.find_element_by_id("schsubmit").click()
        # 点击网页上的开始日期
        time.sleep(4)
        fyear, fmonth = self.get_time(begin)
        lyear, lmonth = self.get_time(end)
        try:
            self.__browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
            self.__browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
            self.__browser.find_element_by_xpath(
                "//span[@class='selectA yearA slided']//div//a[@href='#" + str(fyear) + "']").click()
            self.__browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
            self.__browser.find_element_by_xpath(
                "//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(fmonth) + "']").click()
            # 选择网页上的截止日期
            self.__browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
            self.__browser.find_element_by_xpath(
                "//span[@class='selectA yearA slided']//div//a[@href='#" + str(lyear) + "']").click()
            self.__browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
            self.__browser.find_element_by_xpath(
                "//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(lmonth) + "']").click()
            self.__browser.find_element_by_xpath("//input[@value='确定']").click()
            time.sleep(3)
        except Exception as e:
            print(e)
        pass

    @staticmethod
    def get_former_time(str_time):
        str_time = str(str_time).replace('-', '')
        year = str_time[0:4]
        month = str_time[4:6]
        return year, month
        pass

    @staticmethod
    def get_later_time(str_time):
        str_time = str(str_time).replace('-', '')
        year = int(str_time[0:4])
        month = int(str_time[4:6])
        if month == 12:
            month = 1
            year += 1
        if month < 10:
            month = '0' + str(month)
        return str(year), str(month)
        pass

    @staticmethod
    def get_time(str_time):
        str_time = str(str_time).replace('-', '')
        year = int(str_time[0:4])
        month = int(str_time[4:6])
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        if month < 10:
            month = '0' + str(month)
        return str(year), str(month)
        pass

    @staticmethod
    def __init_table(threshold=140):  # 二值化函数
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return table

    def image_to_string(self, filename):
        image = Image.open(filename)
        imgry = image.convert('L')
        binary = imgry.point(self.__init_table(), '1')
        im1 = binary.convert('L')
        im2 = ImageOps.invert(im1)
        im3 = im2.convert('1')
        im4 = im3.convert('L')
        (x, y) = im4.size
        x_s = x * 2
        y_s = y * 2
        out = im4.resize((x_s, y_s), Image.ANTIALIAS)
        return pytesseract.image_to_string(out)
        pass

    @staticmethod
    def time_rangle(locations):
        return (int(locations['x']),
                int(locations['y'] - 175),
                int(locations['x'] + 220 - 146),
                int(locations['y'] - 117 - 29))
        pass

    def get_index_rangle(self, locations, lens):
        return (int(locations['x'] + 29 + lens),
                int(locations['y'] - 117 - 29),
                int(locations['x'] + 220),
                int(locations['y'] - 117))
        pass

    @staticmethod
    def get_one_month_days(year, month):
        leap_year = {'01': 31, '02': 29, '03': 31, '04': 30, '05': 31, '06': 30,
                     '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}
        nonleap_year = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30,
                        '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}
        year = int(year)
        if year % 4 == 0:
            return leap_year[month]
        else:
            return nonleap_year[month]


    '''
    @staticmethod
    def get_days(begin, end):
        leap_year = {'01': 31, '02': 29, '03': 31, '04': 30, '05': 31, '06': 30,
                     '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}
        nonleap_year = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30,
                        '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}
        begin = str(begin).replace('-', '')
        fyear = int(begin[0:4])
        fmonth = begin[4:6]
        end = str(end).replace('-', '')
        lyear = int(end[0:4])
        lmonth = end[4:6]
        if fyear % 4 == 0:
            fmonth = leap_year[fmonth]
        else:
            fmonth = nonleap_year[fmonth]
        if lyear % 4 == 0:
            lmonth = leap_year[lmonth]
        else:
            lmonth = nonleap_year[lmonth]
        return fmonth + lmonth
        pass
        '''

    def exist_viewbox(self):
        try:
            self.__browser.find_element_by_xpath('//div[@id="viewbox"]')
            return True
        except Exception as e:
            print(e)
            return False

    def __move_mouse(self, x_offset, y_offset):
        ActionChains(self.__browser).move_by_offset(x_offset, y_offset).perform()
        while not self.exist_viewbox():
            print('NO ViewBox!')
            ActionChains(self.__browser).move_by_offset(0, 0).perform()
        imgelement = self.__browser.find_element_by_xpath('//div[@id="viewbox"]')
        return imgelement.location

    def get_baidu_index(self, key_word, begin, end):
        self.__browser.maximize_window()
        # time.sleep(2)
        # days = self.get_days(begin=begin, end=end)
        year, month = self.get_time(end)
        days = self.get_one_month_days(year=year,month=month)
        print(days)
        try:
            xoyelement = self.__browser.find_elements_by_css_selector("#trend rect")[2]
            ActionChains(self.__browser).move_to_element_with_offset(xoyelement, 1, 0).perform()
            while not self.exist_viewbox():
                ActionChains(self.__browser).move_by_offset(1, 0).perform()
            last_location = {'y': 0, 'x': 0}
            i = 0
            while i < days:
                locations = self.__browser.find_element_by_xpath('//div[@id="viewbox"]').location
                time_start = time.time()
                while last_location == locations:
                    time_end = time.time()
                    temp = time_end - time_start
                    if temp >= 10:
                        break
                    x_offset = random.randint(1, 4)
                    ActionChains(self.__browser).move_by_offset(x_offset, 0).perform()
                    locations = self.__browser.find_element_by_xpath('//div[@id="viewbox"]').location
                time.sleep(1)
                print('Picture' + str(i))
                lens = self.get_len(key_word=key_word)
                path = "./Screen1/" + str(i)
                self.__browser.save_screenshot(path + ".png")
                img = Image.open(path + ".png")
                jpg = img.crop(self.time_rangle(locations))
                jpg.save(path + '_time.jpg')
                index_rangle = self.get_index_rangle(locations, lens)
                jpg = img.crop(index_rangle)
                jpg.save(path + '_index.jpg')
                text_time = self.image_to_string(path + '_time.jpg')
                text_index = self.image_to_string(path + '_index.jpg')
                text_index = str(text_index).replace(', ', '').replace('. ', '').replace(',', '').replace('.', '')
                print('Time and Index:', text_time, text_index)
                self.__list_date.append(text_time)
                self.__list_index.append(text_index)
                i += 1
                last_location = locations
            self.__df = pd.DataFrame({'Date': self.__list_date, 'Index': self.__list_index}, columns=['Date', 'Index'])
            self.__df.to_excel('./Data1/' + key_word + '.xlsx')
            self.__list_date = []
            self.__list_index = []
        except Exception as e:
            print(e)
            self.__NoBaiduIndex.append(key_word)

    pass

    def get_item(self):
        locations = {'y': 553.0, 'x': 177.0}
        img = Image.open("./screen/" + str(2) + ".png")
        jpg = img.crop(self.time_rangle(locations))
        jpg.save('./screen/' + str(2) + '_time.jpg')
        index_rangle = self.get_index_rangle(locations, 0)
        jpg = img.crop(index_rangle)
        jpg.show()
        jpg.save('./screen/' + str(2) + '_index.jpg')
        text_time = self.image_to_string('./screen/' + str(2) + '_time.jpg')
        text_index = self.image_to_string('./screen/' + str(2) + '_index.jpg')
        print('Time and Index:', text_time, text_index)
        self.__list_date.append(text_time)
        self.__list_index.append(text_index)

    pass

    def get_len(self, key_word):
        list_uchar = list(key_word)
        lens = 0
        for uchar in list_uchar:
            uchar = uchar.decode('string_escape')
            if uchar in [':']:
                lens += 7
            elif uchar.isdigit():
                lens += 7
            elif uchar.isalpha():
                lens += 7
            else:
                lens += 12.5
        if lens >= 100:
            lens = 100
        return lens

    def run(self):
        # variable
        account = "ChaofanArduino"
        pass_word = "ccf6549683"
        self.open_browser()
        self.log_in(account=account, pass_word=pass_word)
        self.open_index_page(key_word=u'战狼2', begin='2017-06-27', end='2017-07-27')
        self.get_baidu_index(key_word=u'战狼2', begin='2017-06-27', end='2017-07-27')
        try:
            df = pd.read_excel('./BaiduIndex.xlsx')
            for i in range(29, 41):
                # self.open_browser()
                # self.log_in(account=account, pass_word=pass_word)
                key_word = df.ix[i][0]
                begin = df.ix[i][1]
                end = df.ix[i][2]
                self.__used.append(key_word)
                self.open_index_page(key_word=key_word, begin=begin, end=end)
                self.get_baidu_index(key_word=key_word, begin=begin, end=end)
            self.close_browser()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    a = BDIndexProcessor()
    a.run()
    pass
