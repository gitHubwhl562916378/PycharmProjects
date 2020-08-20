import torch
# from MobileNetV2 import mobilenet_v2
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from PIL import Image
from torch.autograd import Variable
import numpy as np
import matplotlib.pyplot as plt

input_size = 224
# batch_size=16
# n_worker = 16
# traindir = './train'
# valdir = './value'
# train_dataset = datasets.ImageFolder(
#     traindir,
#     transforms.Compose([
#         transforms.RandomResizedCrop(input_size, scale=(0.2, 1.0)),
#         transforms.RandomHorizontalFlip(),
#         transforms.ToTensor(),
#         normalize,
#     ])
# )
#
# train_loader = DataLoader(
#     train_dataset, batch_size=batch_size, shuffle=True,
#     num_workers=n_worker, pin_memory=True
# )
#
# val_loader = DataLoader(
#     datasets.ImageFolder(valdir, transforms.Compose([
#         transforms.Resize(int(input_size/0.875)),
#         transforms.CenterCrop(input_size),
#         transforms.ToTensor(),
#         normalize,
#     ])),
#     batch_size=batch_size, shuffle=False,
#     num_workers=n_worker, pin_memory=True)

model = models.mobilenet_v2(True)
if torch.cuda.is_available():
    model = model.cuda()
model.eval()

img = Image.open('test.jpg')
transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
tensor = transform(img)
tensor = tensor.unsqueeze(0)
if torch.cuda.is_available():
    tensor = tensor.cuda()

with torch.no_grad():
    result = model(tensor)
result = result.cpu()
print(result, result.size())
print(result[0])
# The output has unnormalized scores. To get probabilities, you can run a softmax on it.
print(torch.nn.functional.softmax(result[0], dim=0))
_, preds = torch.max(result, 1)
print(preds)