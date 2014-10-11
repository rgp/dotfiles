#!/usr/bin/env python
# coding=UTF-8

import math, subprocess

p = subprocess.Popen(["ioreg", "-rc", "AppleSmartBattery"], stdout=subprocess.PIPE)
output = p.communicate()[0]

o_max = [l for l in output.splitlines() if 'MaxCapacity' in l][0]
o_cur = [l for l in output.splitlines() if 'CurrentCapacity' in l][0]

b_max = float(o_max.rpartition('=')[-1].strip())
b_cur = float(o_cur.rpartition('=')[-1].strip())

charge = b_cur / b_max
charge_threshold = int(math.ceil(4 * charge))

# Output

total_slots, slots = 4, []
filled = int(math.ceil(charge_threshold * (total_slots / 10.0))) * u'▸'
empty = (total_slots - len(filled)) * u'▹'

out = (filled + empty).encode('utf-8')
import sys

# color_green = '%{[32m%}'
# color_yellow = '%{[1;33m%}'
color_green = '\e[0;32m'
color_yellow = '\e[0;33m'
# color_red = '%{[31m%}'
color_red = '\e[0;31m'
color_reset = '\e[0m'
color_out = (
    color_green if len(filled) > 3
    else color_yellow if len(filled) > 1
    else color_red
)

sys.stdout.write(out)
out = color_out + out + color_reset
# sys.stdout.write(out)
