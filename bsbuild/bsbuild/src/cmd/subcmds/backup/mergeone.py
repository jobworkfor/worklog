#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io

file_list = os.listdir('')
filtered_list = []
for item in file_list:
    if item.startswith("logcat"):
        filtered_list.append(item)
        filtered_list.sort()
        filtered_list.reverse()

all_in_one_file = open('all_in_one.txt', 'w')

for item in filtered_list:
    print("mergin file ", item)
    file_info = "[" + item + "] "
    for txt in io.open(item, mode="r", encoding="utf-8"):
        all_in_one_file.write(file_info + txt)

all_in_one_file.close()
