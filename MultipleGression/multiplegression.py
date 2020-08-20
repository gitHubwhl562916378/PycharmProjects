#!/usr/bin/python
# -*- coding: UTF-8 -*-

import torch
from torch.autograd import Variable
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

def make_features(x):
    x = x.unsqueeze(1)
    return torch.cat([x ** i for i in range(1, 4)], 1)

W_target = torch.FloatTensor([0.5, 3, 2.4]).unsqueeze(1)
b_target = torch.FloatTensor([0.9])

def f(x):
    return x.mm(W_target) + b_target[0]

def get_batch(random):
    x = make_features(random)
    y = f(x)
    if torch.cuda.is_available():
        return Variable(x).cuda(), Variable(y).cuda()
    else:
        return Variable(x), Variable(y)

class poly_model(torch.nn.Module):
    def __init__(self):
        super(poly_model, self).__init__()
        self.poly = torch.nn.Linear(3, 1)

    def forward(self, x):
        out = self.poly(x)
        return out

if torch.cuda.is_available():
    model = poly_model().cuda()
else:
    model = poly_model()

criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

epoch = 0
while True:
    random = torch.randn(32)
    batch_x, batch_y = get_batch(random)
    output = model(batch_x)
    loss = criterion(output, batch_y)
    print_loss = loss.item()
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    epoch += 1
    print(print_loss)
    if print_loss < 1e-3:
        break

model.eval()
for name, parameters in model.named_parameters():
    print('name: {}, param: {}'.format(name, parameters))

random = torch.randn(32)
batch_x, batch_y = get_batch(random)
predict = model(batch_x)
predict = predict.data.cpu()
predict = predict.numpy().flatten()
random = random.numpy()
batch_y = batch_y.data.cpu()
plt.title('MultipleGression')
plt.plot(random, batch_y.numpy(), 'ro', label='real curve')
data_dict = {}
for i in random:
    data_dict[i] = predict[np.argwhere(random == i).squeeze()]
data_dict = sorted(data_dict.items(), key=lambda x: x[0])
print(data_dict)
predict = []
random = []
for item in data_dict:
    random.append(item[0])
    predict.append(item[1])
plt.plot(random, predict, 'b-', label='fitting curve')
plt.legend(loc='best')
plt.show()