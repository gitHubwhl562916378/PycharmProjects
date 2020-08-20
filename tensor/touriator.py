#!/usr/bin/python
# -*- coding: UTF-8 -*-

import torch
from torch.autograd import Variable
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

a = torch.Tensor([[2, 3], [4, 9], [7, 9]])
print('a is {}'.format(a))
print('a size is {}'.format(a.size())) #a.size() =3, 2

b = torch.LongTensor([[2, 3], [4, 8], [7, 9]])
print('b is {}'.format(b))

c = torch.zeros(3, 2)
print('zero tensor: {}'.format(c))

d = torch.randn((3, 2))
print('normal randon is : {}'.format(d))

a[2, 0] = 6
print('changed a is: {}'.format(a))

numpy_b = b.numpy()
print('conver to numpy is \n{}'.format(numpy_b))

e = np.array([[3, 2], [5, 8], [8, 10]])
print('e is {}'.format(e))
torch_e = torch.from_numpy(e)
print('from numpy to torch.Tensor is {}'.format(torch_e))
f_torch_e = torch_e.float()
print('change data type to float  tensor: {}'.format(f_torch_e))

if  torch.cuda.is_available():
    a_cuda = a.cuda()
    print(a_cuda)