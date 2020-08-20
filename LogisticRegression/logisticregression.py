#!/usr/bin/python
# -*- coding: UTF-8 -*-

import torch
from torch.autograd import Variable
import matplotlib.pyplot as plt
import numpy as np
import operator

with open('data.txt', 'r') as f:
    data_list = f.readlines()
    data_list = [i.split('\n')[0] for i in data_list]
    data_list = [i.split(',') for i in data_list]
    data = [(float(i[0]), float(i[1]), float(i[2])) for i in data_list]

x0 = list(filter(lambda x: x[-1] == 0.0, data))
x1 = list(filter(lambda x: x[-1] == 1.0, data))
plot_x0_0 = [i[0] for i in x0]
plot_x0_1 = [i[1] for i in x0]
plot_x1_0 = [i[0] for i in x1]
plot_x1_1 = [i[1] for i in x1]

plt.plot(plot_x0_0, plot_x0_1, 'ro', label='x_0')
plt.plot(plot_x1_0, plot_x1_1, 'bo', label='x_1')
plt.legend(loc='best')

x_data = torch.cat([torch.tensor([(a[0], a[1]) for a in data])], 0)
print(x_data)
y_data = torch.FloatTensor([a[2] for a in data]).unsqueeze(1)
print(y_data)
class LogisticRegression(torch.nn.Module):
    def __init__(self):
        super(LogisticRegression,self).__init__()
        self.lr = torch.nn.Linear(2, 1)
        self.sm = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.lr(x)
        x = self.sm(x)
        return x

logistic_model = LogisticRegression()
if torch.cuda.is_available():
    logistic_model.cuda()

criterion = torch.nn.BCELoss()
optimizer = torch.optim.SGD(logistic_model.parameters(), lr=1e-3, momentum=0.9)

for epoch in range(50000):
    if torch.cuda.is_available():
        x_data = Variable(x_data).cuda()
        y_data = Variable(y_data).cuda()
    else:
        x_data = Variable(x_data)
        y_data = Variable(y_data)

    out = logistic_model(x_data)
    loss = criterion(out, y_data)
    print_loss = loss.item()
    mask = out.ge(0.5).float()
    correct = (mask == y_data).sum()
    acc = correct.item() / x_data.size(0)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 100 == 0:
        print('*' * 10)
        print('epoch {}'.format(epoch +1))
        print('loss is {:.4f}'.format(print_loss))
        print('acc is {:.4f}'.format(acc))

w0, w1 = logistic_model.lr.weight[0]
print(w0, w1)
w0 = w0.item()
w1 = w1.item()
print(logistic_model.lr.bias.data[0])
b = logistic_model.lr.bias.item()
plot_x = np.arange(30, 100, 0.1)
plot_y = (-w0 * plot_x - b) / w1
plt.plot(plot_x, plot_y)
plt.show()
