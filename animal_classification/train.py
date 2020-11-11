import sys
import torch
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
from torch.autograd import Variable
from models import *

train_sets = torchvision.datasets.FashionMNIST('data', train=True, download=True, transform=transforms.ToTensor())
transforms.ConvertImageDtype
batch_size = 32
train_loader = DataLoader(train_sets, batch_size=batch_size, shuffle=True, num_workers=2)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
net = Net().to(device)
print(net)

loss = torch.nn.CrossEntropyLoss()
optimzer = torch.optim.SGD(net.parameters(), lr=0.001)

epoch = 100

for ep in range(epoch):
    sum_loss = 0.0
    for batch_index, data in enumerate(train_loader):
        inputs, labels = data
        if torch.cuda.is_available():
            inputs, labels = Variable(inputs).cuda(), Variable(labels).cuda()
        optimzer.zero_grad()
        outputs = net(inputs)
        err = loss(outputs, labels)
        err.backward()
        optimzer.step()

        sum_loss += err.item()
        if batch_index % 100 == 99:
            print('epoch {} batch {} loss acc {}'.format(ep + 1, batch_index + 1, sum_loss/100))
            sum_loss = 0.0

net.eval()