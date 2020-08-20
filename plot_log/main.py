#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-
import os
import re
from time import *
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# str = '2020-03-05 12:52:29.272 [Debug]: SnapFaceMongoDao::syncData2Java all use: 16'
# pattern = re.compile(r'^2020-03-05 12:5[0-2].+$')
# match = pattern.match(str)
#
# if match:
#     print(match.group())

def findlog_by_time_indir(log_dir, pattern, out_file_name):
    ofile = open(out_file_name, 'w')
    file_names = os.listdir(log_dir)
    for file_name in file_names:
        print(file_name)
        if not os.path.isdir(file_name):
            f = open(log_dir + "/" + file_name, "r")
            iter_f = iter(f)
            for line in iter_f:
                match = pattern.match(line)
                if match:
                    print(match.group())
                    ofile.writelines(match.group())
                    ofile.write("\n")

def statistics_count_time(input_file, pattmap, out_count):
    with open(input_file) as f:
        iter_f = iter(f)
        max_use_time = 0;
        max_use_ts = '';
        for line in iter_f:
            for key, value in pattmap.items():
                pattern = re.compile(r'' + value)
                match = pattern.match(line)
                if match:
                    cur_time = match.group(1)
                    time_str = cur_time
                    cur_time = datetime.strptime(cur_time, '%Y-%m-%d %H:%M:%S.%f')
                    use_time = match.group(2)
                    use_time = int(use_time)
                    if(use_time > max_use_time):
                        max_use_time = use_time
                        max_use_ts = time_str
                    if(out_count.has_key(key)):
                        old_count = out_count[key][-1][1]
                        out_count[key].append([cur_time, old_count + 1, use_time])
                    else:
                        out_count[key]=[[cur_time, 1, use_time]]

                    # if use_time > 500:
                    #     print match.group()
                    # break

        print 'max use time ',max_use_time, ' time ', max_use_ts

def draw_time_count(out_count):
    # plt.figure(figsize=(200,180), dpi=80)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M')) #横坐标日期显示格式
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval = 10)) #横坐标每过5分钟画一个点
    plt.xlabel('time')
    plt.ylabel('count')

    last_value_map = {}
    dtime_min = datetime.strptime('2050-03-06 12:00:00.000', '%Y-%m-%d %H:%M:%S.%f')
    for key in out_count:
        plot_np_array = np.array(out_count[key]) #转化为np用于切片
        xs = plot_np_array[:,0] #切片，':'前面没东西表示所有行，0表示取0列，取出之后组成一个新的一list
        ys = plot_np_array[:,1]
        print key + ' ' + str(len(xs))
        if (xs[0] < dtime_min):
            dtime_min = xs[0]

        last_value_map[key] = (xs[-1], ys[-1])
        plt.plot(xs, ys, label=key)

    yoffset = 0
    print '抓拍率统计:'
    for key,value in last_value_map.items():
        lv = value[1]/(value[0] - dtime_min).seconds
        print '\t' + key + ' ' + str(lv) +'张/秒 ' + str(lv * 60 * 60) + '张/小时 运行时长:' + str(value[0] - dtime_min)
        if key!='SnapScene':
            plt.scatter(value[0], value[1] - yoffset) #在坐标处画一个标注，一般是一个点
            plt.annotate(key + ' ' + str(value[1]), (value[0], value[1]), (value[0], value[1] - yoffset)) #在坐标处添加文本注释
            yoffset += 20000
        else:
            plt.scatter(value[0], value[1])
            plt.annotate(key + ' ' + str(value[1]), (value[0], value[1]))

    plt.xlim(xmin=dtime_min)#设置x轴的范围
    plt.ylim(ymin=0)#设置y轴的范围
    plt.gcf().autofmt_xdate() #自动旋转x轴日期显示
    plt.legend(loc='upper left') #添加legend
    plt.show()

def draw_time_cost(out_count):
    # plt.figure(figsize=(200,180), dpi=80)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M')) #横坐标日期显示格式
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval = 5)) #横坐标每过5分钟画一个点
    plt.xlabel('time')
    plt.ylabel('cost time')

    for key in out_count:
        plot_np_array = np.array(out_count[key]) #转化为np用于切片
        xs = plot_np_array[:,0] #切片，':'前面没东西表示所有行，0表示取0列，取出之后组成一个新的一list
        ys = plot_np_array[:,2]
        data_len = len(ys)
        print key + ' 总量:' + str(data_len) + ' 总时间: ' + str(ys.sum()) + ' 平均耗时: ' + str((ys.sum()/data_len))
        plt.plot(xs, ys, label=key)

    plt.gcf().autofmt_xdate() #自动旋转x轴日期显示
    plt.legend(loc='upper left') #添加legend
    plt.show()

def main():
    # re_patterns = '(?P<SnapFace>(?P<SnapFaceTime>.+) \[Debug\]: SnapFaceMongoDao::syncData2Java all use: (?P<SnapFaceCost>\d+))|' \
    #               '(?P<SnapBody>(?P<SnapBodyTime>.+) \[Debug\]: SnapBodyMongoDao::syncData2Java use: (?P<SnapBodyCost>\d+))|' \
    #               '(?P<SnapScene>(?P<SnapSceneTime>.+) \[Debug\]: SnapSceneMongoDao::syncSceneDataToJava time record id:.+ use: (?P<SnapSceneCost>\d+))|' \
    #               '(?P<SnapAlarm>(?P<SnapAlarmTime>.+) \[Debug\]: SnapAlarmMongoDao::syncData2Java time statis type:\d use: (?P<SnapAlarmCost>\d+))|' \
    #               '(?P<Attribute>(?P<AttributeTime>.+) \[Debug\]: PersonAttributeMongoDao::syncData2Java time statis use: (?P<AttributeCost>\d+))'
    #
    # match_str = '2020-03-06 00:13:39.297 [Debug]: SnapFaceMongoDao::syncData2Java all use: 10\n'\
    #             '2020-03-06 00:13:29.452 [Debug]: PersonAttributeMongoDao::syncData2Java time statis use: 16\n'\
    #             '2020-03-06 00:13:39.297 [Debug]: SnapFaceMongoDao::syncData2Java all use: 10\n'\
    #             '2020-03-06 00:13:39.305 [Debug]: SnapSceneMongoDao::syncSceneDataToJava time record id:465073405efc11eaa95fac1f6b947f3a use: 36\n'\
    #             '2020-03-06 00:13:39.317 [Debug]: SnapAlarmMongoDao::syncData2Java time statis type:5 use: 16\n'\
    #             '2020-03-06 00:13:39.339 [Debug]: SnapBodyMongoDao::syncData2Java use: 11 id:4650be7c5efc11eaa8dfac1f6b947f3a\n'\
    #             '2020-03-06 00:13:29.452 [Debug]: PersonAttributeMongoDao::syncData2Java time statis use: 16'
    # [52638, 52360, 6403, 52475, 52622]
    # match_obj = re.compile(r'' + re_patterns).match(match_str)
    # if match_obj:
    #     print match_obj.group('Attribute'),match_obj.group('AttributeTime'),match_obj.group('AttributeCost')

    start_time = time()

    #findlog_by_time_indir("log", re.compile(r'2020-03-012 0[0-1]:\d\d.+$'), "log_bytime.txt")
    # labes_map = {
    #     'SnapFace': '(.+) \[Debug\]: SnapFaceMongoDao::syncData2Java all use: (\d+)$',
    #     'SnapBody': '(.+) \[Debug\]: SnapBodyMongoDao::syncData2Java use: (\d+) id:',
    #     'SnapScene': '(.+) \[Debug\]: SnapSceneMongoDao::syncSceneDataToJava time record id:.+ use: (\d+)$',
    #     'SnapAlarm': '(.+) \[Debug\]: SnapAlarmMongoDao::syncData2Java time statis type:\d use: (\d+)$',
    #     'Attribute': '(.+) \[Debug\]: PersonAttributeMongoDao::syncData2Java time statis use: (\d+)$',
    #     'RelationShip': '(.+) \[Debug\]: RelationShipMongoDao::syncData2Java end use:(\d+)$'
    # }
    camera_id = '(?:98)' #(?:\d+)/id
    labes_map = {
        'SnapFace': '(.+) \[Debug\]: SnapFaceMongoDao::syncData2Java camera_id: ' + camera_id + ' all use: (\d+)$',
        'SnapBody': '(.+) \[Debug\]: SnapBodyMongoDao::syncData2Java camera_id:' + camera_id +' use: (\d+) id:',
        'SnapScene': '(.+) \[Debug\]: SnapSceneMongoDao::syncSceneDataToJava time camera_id: ' + camera_id + ' record id:(?:.+)  use: (\d+)$',
        'SnapAlarm': '(.+) \[Debug\]: SnapAlarmMongoDao::syncData2Java time statis camera_id: ' + camera_id + ' type:(?:\d+) use: (\d+)$',
        'Attribute': '(.+) \[Debug\]: PersonAttributeMongoDao::syncData2Java time statis camera_id: ' + camera_id + ', use: (\d+)$',
        'RelationShip': '(.+) \[Debug\]: RelationShipMongoDao::syncData2Java camera_id:' + camera_id + ' end use:(\d+) '
    }

    out_count = {}
    print  'statistics start'
    statistics_count_time('/home/whl/seye-logs/KLMediaServer.log', labes_map, out_count)
    print 'statistics cost ', time() - start_time

    # print 'draw_time_count start'
    # draw_time_count(out_count)

    print 'draw_time_cost start'
    draw_time_cost(out_count)

if __name__ == '__main__':
    main()