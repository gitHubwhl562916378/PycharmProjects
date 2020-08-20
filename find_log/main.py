# -*- coding: UTF-8 -*-

#FightBehaviroDetectTest::OnFightBehavior camera_id %d threshold %f scene_size %d
#[2020-04-26 06:51:31.578] [multi_sink] [debug] [FightBehaviorDetect]: FightBehaviorDetect Process threshold 0.52 setting {} index {}
import re
import os

def find_log_in_file(file_name, patten_str):
    with open(file_name) as f:
        iter_f = iter(f)
        for line in iter_f:
            patten = re.compile(r'' + patten_str)
            result = patten.match(line)
            if result:
                print(result.group())
                print(result.group(1), result.group(3), result.group(5))

if __name__ == '__main__':
    find_log_in_file('/home/whl/Documents/git/AiFrameWork/workspace/logs/logs/sdk.log', '.+\[FightBehaviorDetect\]: FightBehaviorDetect Process threshold (\d+(\.\d+)?) setting (\d+(\.\d+)?) index (-?\d)$')