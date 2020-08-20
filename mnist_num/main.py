# -*- coding: UTF-8 -*-

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import torchvision
from torch.autograd import Variable
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

batch_size=32
train_dataset = datasets.MNIST(root='./num',train=True,transform=transforms.ToTensor(),download=False)
test_dataset = datasets.MNIST(root='./num', train=False, transform=transforms.ToTensor(),download=False)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True)

# def show_bacth(imgs):
#     grid = torchvision.utils.make_grid(imgs, nrow=5)
#     plt.imshow(grid.numpy().transpose((1,2,0)))
#     plt.title('Batch from dataLoader')
#
# for i, (batch_x, batch_y) in enumerate(train_loader):
#     print(i, batch_x.size(), batch_y.size())
#     show_bacth(batch_x)
#     plt.axis('off')
#     plt.show()

class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = nn.Sequential(nn.Conv2d(1, 6, 3, 1, 2), nn.ReLU(),nn.MaxPool2d(2, 2))

        self.conv2 = nn.Sequential(nn.Conv2d(6, 16, 5), nn.ReLU(), nn.MaxPool2d(2, 2))

        self.fc1 = nn.Sequential(nn.Linear(16 * 5 * 5, 120), nn.BatchNorm1d(120), nn.ReLU())

        self.fc2 = nn.Sequential(nn.Linear(120, 84), nn.BatchNorm1d(84), nn.ReLU(), nn.Linear(84, 10))

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size()[0], -1)
        x = self.fc1(x)
        x = self.fc2(x)
        return x
#
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# LR = 0.001
#
# net = LeNet().to(device)
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(net.parameters(), lr=LR)
#
# epoch = 1
# for epoch in range(epoch):
#     sum_loss = 0.0
#     for i, data in enumerate(train_loader):
#         inputs, labes = data
#         inputs, labes = Variable(inputs).cuda(), Variable(labes).cuda()
#         optimizer.zero_grad()
#         outputs = net(inputs)
#         loss = criterion(outputs, labes)
#         loss.backward()
#         optimizer.step()
#
#         sum_loss += loss.item()
#         if i % 100 == 99:
#             print('[%d,%d] loss:%.03f' % (epoch + 1, i + 1, sum_loss / 100))
#             sum_loss = 0.0

net = torch.load('model.pth')
net.eval()
correct = 0
total = 0
for data_test in test_loader:
    images, labes = data_test
    images, labes = Variable(images).cuda(), Variable(labes).cuda()
    output_test = net(images)
    res, predicted = torch.max(output_test, 1) #多参数返回，第一个不接收
    total += labes.size(0)
    correct += (predicted == labes).sum()
print('correct1: ', correct)
print('Test acc: {0}'.format(correct.item() / len(test_dataset)))

torch.save(net, 'model.pth')