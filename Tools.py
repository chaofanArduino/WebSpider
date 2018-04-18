# -*- coding:utf-8 -*-

from Setting import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class TimeTools:
    def __init__(self):
        pass

    def __str__(self):
        return 'TimeTools'

    @staticmethod
    def series_format_date(series_time, separator=''):
        series_temp = pd.Series(series_time)
        series_temp = series_temp.fillna('10001010')
        for i in range(0, len(series_temp)):
            series_temp[i] = str(series_temp[i])
            series_temp[i] = TimeTools.str_format_date(date=series_temp[i], separator=separator)
        return series_temp

    @staticmethod
    def str_format_date(date, separator=''):
        for temp in DATE_REPLACE.keys():
            date = date.replace(temp, DATE_REPLACE[temp])
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        return year + separator + month + separator + day

    @staticmethod
    def __get_days_of_month(year, month):
        """

        :param year: year such as 2017
        :param month: month such as 07 or 7
        :return: days of the month in the year
        """
        try:
            year = int(year)
            month = str(month)
        except Exception as e:
            print(e)
        if year % 4 == 0:
            return LEAP_YEAR[month]
        else:
            return NONLEAP_YEAR[month]

    @staticmethod
    def __get_days_of_year(year):
        """

        :param year: year such as 2017
        :return: days of the year
        """
        try:
            year = int(year)
        except Exception as e:
            print(e)
        if year % 4 == 0:
            return 366
        else:
            return 365

    @staticmethod
    def get_days(begin, end):
        """

        :param begin: date such as 2017-08-09
        :param end: date such as 2017-08-10
        :return: the days between the two dates
        """
        begin = TimeTools.str_format_date(date=begin)
        end = TimeTools.str_format_date(date=end)
        try:
            fyear = int(begin[0:4])
            fmonth = int(begin[4:6])
            fday = int(begin[6:8])
            lyear = int(end[0:4])
            lmonth = int(end[4:6])
            lday = int(end[6:8])
        except Exception as e:
            print(e)

        if lyear == fyear:
            if lmonth == fmonth:
                return lday - fday + 1
            else:
                days = TimeTools.__get_days_of_month(fyear, fmonth) - fday + 1
                for month in range(fmonth + 1, lmonth):
                    days += TimeTools.__get_days_of_month(fyear, month)
                days += lday
                return days
        else:
            days = TimeTools.__get_days_of_month(fyear, fmonth) - fday + 1
            for month in range(fmonth + 1, 13):
                days += TimeTools.__get_days_of_month(fyear, month)
            for year in range(fyear+1,lyear):
                days += TimeTools.__get_days_of_year(year)
            for month in range(1, lmonth):
                days += TimeTools.__get_days_of_month(lyear, month)
            days += lday
            return days


class IndexTools:
    def __init__(self):
        pass

    def __str__(self):
        return 'IndexTools'

    @staticmethod
    def series_format_index(series_index):
        series_temp = pd.Series(series_index)
        series_temp = series_temp.fillna('0')
        for i in range(0, len(series_temp)):
            series_temp[i] = IndexTools.str_format_index(index=series_temp[i])
        return series_temp

    pass

    @staticmethod
    def str_format_index(index):
        index = str(index)
        for temp in INDEX_REPLACE.keys():
            index = index.replace(temp, INDEX_REPLACE[temp])
        return index
        pass


if __name__ == '__main__':
    pass
