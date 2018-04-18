# -*- coding:utf-8 -*-

from Tools import *
import os


class Main:
    def __init__(self):
        pass

    def get_files(self, filename):
        dict_files = {}
        list_file = os.listdir(filename)
        for file in list_file:
            file = file.decode('gbk')
            dict_files[file] = pd.read_excel(filename + file)
        return dict_files

    def get_df(self,df, begin, end):
        begin = int(TimeTools.str_format_date(begin))
        end = int(TimeTools.str_format_date(end))
        df = df[df.Date >= begin+1]
        df = df[df.Date <= end]
        return df
        pass

    def get_filename(self, file):
        return file[0:len(file)-5]
        pass

    def run(self):
        path_f = FILE_PATH + 'movies/'
        path_l = FILE_PATH + 'data/'
        file_g = FILE_PATH + 'goal.xlsx'
        dict_f = self.get_files(filename=path_f)
        dict_l = self.get_files(filename=path_l)
        df_g = pd.read_excel(file_g)
        df_g.index = df_g.Movies
        list_movie_name = []
        list_time1 = []
        list_time2 = []
        list_time3 = []
        list_month_mean = []
        list_week_mean = []
        list_month_max = []
        list_week_max = []
        for file_f in dict_f.keys():
            for file_l in dict_l.keys():
                if file_f == file_l:
                    df = pd.concat([dict_f[file_f], dict_l[file_l]], ignore_index=True)
                    df['Date'] = TimeTools.series_format_date(df['Date'])
                    df['Index'] = IndexTools.series_format_index(df['Index'])
                    temp = file_l[0:len(file_l)-5]
                    list_movie_name.append(temp)
                    print(temp)
                    df.to_csv('./BI/' + temp + '_whole.csv',index=False)
                    time1 = df_g.ix[temp][1]
                    time2 = df_g.ix[temp][2]
                    time3 = df_g.ix[temp][3]
                    list_time1.append(time1)
                    list_time2.append(time2)
                    list_time3.append(time3)
                    df_temp = self.get_df(df, time1, time2)
                    list_month_mean.append(df_temp.Index.mean())
                    list_month_max.append(df_temp.Index.max())
                    df_temp.to_csv('./BI/' + temp + '_month.csv',index=False)
                    df_temp = self.get_df(df, time2, time3)
                    list_week_mean.append(df_temp.Index.mean())
                    list_week_max.append(df_temp.Index.max())
                    df_temp.to_csv('./BI/' + temp + '_week.csv',index=False)
        dict_temp = {
            u'电影名称':list_movie_name,
            u'上映前一个月':list_time1,
            u'上映日期':list_time2,
            u'上映后一周':list_time3,
            u'上映前一个月到上映日期平均数':list_month_mean,
            u'上映前一个月到上映日期最大值':list_month_max,
            u'上映日期到上映后一周平均数':list_week_mean,
            u'上映日期到上映后一周平最大值':list_week_max
        }
        columns = [  u'电影名称',
            u'上映前一个月',
            u'上映日期',
            u'上映后一周',
            u'上映前一个月到上映日期平均数',
            u'上映前一个月到上映日期最大值',
            u'上映日期到上映后一周平均数',
            u'上映日期到上映后一周平最大值']
        df_temp = pd.DataFrame(dict_temp,columns=columns)
        df_temp.to_excel('./BI/result.xlsx',index=False)

if __name__ == '__main__':
    m = Main()
    m.run()
    file_g = FILE_PATH + 'goal.xlsx'
    df_g = pd.read_excel(file_g)
    print(df_g)
    df_g.index = df_g.Movies
    print(df_g.ix[u'战狼2'][1])
    pass
