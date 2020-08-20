# -*- coding: UTF-8 -*-

import re
import os

def find_log(file_name, patten_str):
    with open(file_name) as f:
        iter_f = iter(f)
        for line in iter_f:
            patten = re.compile(r'' + patten_str)
            res = patten.match(line)
            if(res):
                print(res.group())

# 2020-04-17 04:11:52.030 [Information]: KLVideoDevice::~KLVideoDevice delete mEventHandler use 0
find_log('/home/whl/seye-logs/KLMediaServer.log', '.*HandAlgorithmTask::~HandAlgorithmTask cameraId.*')