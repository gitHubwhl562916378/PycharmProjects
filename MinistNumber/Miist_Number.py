#!/usr/bin/python
# -*- coding: UTF-8 -*-

import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.autograd import Variable
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

class Batch_Net(torch.nn.Module):
    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
        super(Batch_Net, self).__init__()
        self.layer1 = torch.nn.Sequential(
            torch.nn.Linear(in_dim, n_hidden_1),
            torch.nn.BatchNorm1d(n_hidden_1), torch.nn.ReLU(True)
        )
        self.layer2 = torch.nn.Sequential(
            torch.nn.Linear(n_hidden_1, n_hidden_2),
            torch.nn.BatchNorm1d(n_hidden_2), torch.nn.ReLU(True)
        )
        self.layer3 = torch.nn.Sequential(torch.nn.Linear(n_hidden_2, out_dim))

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x

batch_size = 32
learning_rate = 1e-2
num_epoches = 20
data_tf = transforms.Compose( #Compose 把多个步骤合到一起
    [transforms.ToTensor(),
     transforms.Normalize([0.5], [0.5])] #将图片转化到-１~１之间
)

train_dataset = datasets.MNIST(
    root='./data', train=True, transform=data_tf, download=False
)
test_dataset = datasets.MNIST(root='./data', train=False, transform=data_tf, download=False)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)  #ｓｈｕｆｆｌｅ表示每次迭代的时候是否将数据打乱
test_loader  = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

model = Batch_Net(28 * 28, 300, 100, 10)
if(torch.cuda.is_available()):
    model = model.cuda()

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

for epoch in range(num_epoches):
    print('epoch {}'.format(epoch + 1))
    #training----------------------
    train_loss = 0.
    train_acc = 0.
    for img, label in train_loader:
        img = Variable(img)
        img = img.view(batch_size, 28 * 28)
        label = Variable(label)
        if(torch.cuda.is_available()):
            img = img.cuda()
            label = label.cuda()
        out = model(img)
        loss = criterion(out, label)
        train_loss += loss.item()
        pred = torch.max(out, 1)[1]
        train_correct = (pred.data.cpu() == label.data.cpu()).sum()
        train_acc += train_correct.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print('Train Loss: {:.6f}, Acc: {:.6f}'.format(train_loss / (len(train_loader)), train_acc / (len(train_loader))))

model.eval()
eval_loss = 0
eval_acc = 0
for data in test_loader:
    img, label = data
    img = img.view(img.size(0), -1)
    if torch.cuda.is_available():
        img = Variable(img, volatile=True).cuda()
        label = Variable(label, volatile=True).cuda()
    else:
        img = Variable(img, volatile=True)
        label = Variable(label, volatile=True)
    out = model(img)
    loss = criterion(out, label)
    eval_loss = criterion(out, label)
    eval_loss += loss.item() * label.size(0)
    pred = torch.max(out, 1)
    num_correct = (pred == label).sum()
    eval_acc += num_correct.item()
    print('Test Loss: {:.6f}, Acc:{:.6f}'.format(eval_loss / (len(test_loader)), eval_acc / (len(test_dataset))))