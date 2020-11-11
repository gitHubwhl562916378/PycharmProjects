import torch
import torchvision

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.resnet = torchvision.models.resnet18()

    def forward(self, x):
        x = self.resnet(x)
        return x
