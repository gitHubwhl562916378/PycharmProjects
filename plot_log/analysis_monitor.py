from cProfile import label
from tkinter import Y
from turtle import title
import matplotlib.pyplot as plt
import numpy as np


def load_data(input_file):
    ret = []
    f = open(input_file)
    iter_f = iter(f)
    index = 0
    for line in iter_f:
        if (index % 20) == 0:
            v = line.strip().split(',')
            v = list(map(float, v))
            ret.append(v)
        index += 1
    return ret


def draw_figure(data, titles, labels):
    for i, d in enumerate(data, start=0):
        plt.figure(i+1)
        x = d[:, 0].tolist()
        y1 = d[:, 1].tolist()
        y2 = d[:, 2].tolist()
        max_y1 = max(y1)
        max_x1 = x[y1.index(max_y1)]
        max_y2 = max(y2)
        max_x2 = x[y2.index(max_y2)]
        plt.title(titles[i])
        # plt.xlim(0, x[-1])
        plt.xticks(x)
        plt.ylim(0.0, max(max_y1, max_y2))
        plt.xlabel('time/s')
        plt.ylabel('percent/%')
        # 绘制多条线性图
        # 方法一
        # plt.plot(x, y1, label='old')
        # plt.plot(x, y2, label='new')
        # plt.legend(loc='upper left')
        # 方法二
        # plt.plot(x, y1, 'r-o', x, y2, 'g--x')  # r-o 表示红色，实线，圆点标记点值
        plt.plot(x, y1, '-', x, y2, '--')
        plt.legend(labels, loc='upper left')

        plt.scatter(x=max_x1, y=max_y1)
        plt.annotate(text='x:' + str(max_x1) + ', y:' + str(max_y1),
                     xy=(max_x1, max_y1), xytext=(max_x1, max_y1))
        plt.scatter(x=max_x2, y=max_y2)
        plt.annotate(text='x:' + str(max_x2) + ', y:' + str(max_y2),
                     xy=(max_x2, max_y2), xytext=(max_x2, max_y2))
    plt.show()


def drawOnePid(file):
    data = load_data(file)
    draw_figure([np.array(data)], ['EHR cpu/mem live'], ['cpu', 'mem'])


def draw2Pid(files):
    datas = [np.array(load_data(d)) for d in files]
    # 方法一， 单独取出转为二维数组，再拼接
    # xAsix = datas[0][:, 0]
    # y1Asix = datas[0][:, 1]
    # y2Asix = datas[1][:, 1]
    # xAsix = np.reshape(xAsix, (len(xAsix), -1))
    # y1Asix = np.reshape(y1Asix, (len(y1Asix), -1))
    # y2Asix = np.reshape(y2Asix, (len(y2Asix), -1))
    # y2Asix = np.reshape(y2Asix, (len(y2Asix), -1))
    # draw_figure(np.hstack((xAsix, y1Asix, y2Asix)))
    # 方法二，使用numpy的赋值
    data1 = datas[0].copy()
    data1[:, 2] = datas[1][:, 1]

    data2 = datas[0].copy()
    data2 = np.delete(data2, 1, 1)  # 删除第1列
    newMem = datas[1][:, 2]
    data2 = np.append(data2, np.reshape(newMem, (len(newMem), -1)), 1)
    draw_figure([data1, data2], [
                'EHR live cpu compare', 'EHR live mem compare'], ['old', 'new'])


def main():
    drawOnePid("process_monitor_ehr_befor1.csv")
    # draw2Pid(("process_monitor_ehr_befor1.csv",
    #          "process_monitor_ehr_after1.csv"))


if __name__ == '__main__':
    main()
