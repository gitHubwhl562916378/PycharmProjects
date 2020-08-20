import ctypes

so = ctypes.cdll.LoadLibrary("./add.so")
res = so.add(3,5)
print('result=' + str(res))