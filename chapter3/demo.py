#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-11-11 下午2:54
# @Author  : YunSong
# @File    : demo.py
# @Software: PyCharm

import torch
import numpy as np
from torch import nn
import matplotlib.pyplot as plt

torch.manual_seed(2017)

# 从 data.txt 中读入点
with open('./data.txt', 'r') as f:
    data_list = [i.split('\n')[0].split(',') for i in f.readlines()]
    data = [(float(i[0]), float(i[1]), float(i[2])) for i in data_list]

# 标准化
x0_max = max([i[0] for i in data])
x1_max = max([i[1] for i in data])
data = [(i[0] / x0_max, i[1] / x1_max, i[2]) for i in data]

x0 = list(filter(lambda x: x[-1] == 0.0, data))  # 选择第一类的点
x1 = list(filter(lambda x: x[-1] == 1.0, data))  # 选择第二类的点

plot_x0 = [i[0] for i in x0]
plot_y0 = [i[1] for i in x0]
plot_x1 = [i[0] for i in x1]
plot_y1 = [i[1] for i in x1]

plt.plot(plot_x0, plot_y0, 'ro', label='x_0')
plt.plot(plot_x1, plot_y1, 'bo', label='x_1')
plt.legend(loc='best')
# plt.show()


np_data = np.array(data, dtype='float32')  # 转换成 numpy array
x_data = torch.from_numpy(np_data[:, 0:2])  # 转换成 Tensor, 大小是 [100, 2]
y_data = torch.from_numpy(np_data[:, -1]).unsqueeze(1)  # 转换成 Tensor，大小是 [100, 1]

criterion = nn.BCEWithLogitsLoss()  # 将 sigmoid 和 loss 写在一层，有更快的速度、更好的稳定性

w = nn.Parameter(torch.randn(2, 1))
b = nn.Parameter(torch.zeros(1))


def logistic_reg(x):
    return torch.mm(x, w) + b


optimizer = torch.optim.SGD([w, b], 1.)

# 进行 1000 次更新
import time

start = time.time()
for e in range(1000):
    # 前向传播
    y_pred = logistic_reg(x_data)
    loss = criterion(y_pred, y_data)
    # 反向传播
    optimizer.zero_grad()  # 使用优化器将梯度归 0
    loss.backward()
    optimizer.step()  # 使用优化器来更新参数
    # 计算正确率
    mask = y_pred.ge(0.5).float()
    acc = (mask == y_data).sum().item() / y_data.shape[0]
    if (e + 1) % 200 == 0:
        print('epoch: {}, Loss: {:.5f}, Acc: {:.5f}'.format(e + 1, loss.item(), acc))
during = time.time() - start
print()
print('During Time: {:.3f} s'.format(during))
