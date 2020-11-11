# -*- coding: UTF-8 -*-

import torch
import torchvision
from torchvision import transforms, utils
import matplotlib
import matplotlib.pyplot as plt


index_names = ['hezhongjie', 'snap', 'whl']
img_data = torchvision.datasets.ImageFolder('person',
                                            transform=transforms.Compose([
                                                transforms.RandomResizedCrop(224),
                                                transforms.RandomHorizontalFlip(),
                                                transforms.ToTensor()
                                            ]))

batch_size = 2
data_loader = torch.utils.data.DataLoader(img_data, batch_size=batch_size, shuffle=True)

def show_bacth(imgs):
    grid = utils.make_grid(imgs, nrow=1)
    plt.imshow(grid.numpy().transpose((1, 2, 0)))
    plt.title('Batch from dataLoader')
    torch.Size()

for X, Y in data_loader:
    _, figs = plt.subplots(1, batch_size, figsize=(12, 12))
    for f, img_tensor, label_tensor in zip(figs, X, Y):
        f.set_title(index_names[label_tensor.numpy()])
        f.imshow(img_tensor.numpy().transpose(1, 2, 0))
        f.axes.get_xaxis().set_visible(False)
        f.axes.get_yaxis().set_visible(False)
    plt.show()