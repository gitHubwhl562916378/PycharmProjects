import torch
import torchvision

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.resnet = torchvision.models.resnet18()
        self.resnet.conv1 = torch.nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.resnet.fc = torch.nn.Linear(512, 10)

    def forward(self, x):
        x = self.resnet(x)
        return x
