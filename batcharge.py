#!/usr/bin/env python
# coding=UTF-8

import math, subprocess, argparse

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-c','--clean', help='No colors', required=False, const=True, nargs="?")
parser.add_argument('-t','--tmux', help='Tmux colors', required=False, const=True, nargs="?")
args = vars(parser.parse_args())

p = subprocess.Popen(["ioreg", "-rc", "AppleSmartBattery"], stdout=subprocess.PIPE)
output = p.communicate()[0]

o_max = [l for l in output.splitlines() if 'MaxCapacity' in l][0]
o_cur = [l for l in output.splitlines() if 'CurrentCapacity' in l][0]

b_max = float(o_max.rpartition('=')[-1].strip())
b_cur = float(o_cur.rpartition('=')[-1].strip())

charge = b_cur / b_max
charge_threshold = int(math.ceil(10 * charge))

# Output

total_slots, slots = 10, []
filled = int(math.ceil(charge_threshold * (total_slots / 10.0))) * u'▸'
empty = (total_slots - len(filled)) * u'▹'

out = (filled + empty).encode('utf-8')
import sys

color_green = '#[fg=green]' if args['tmux'] else '%{%F{green}%}'
color_yellow = '#[fg=yellow]' if args['tmux'] else '%{%F{yellow}%}'
color_red = '#[fg=red]' if args['tmux'] else '%{%F{red}%}'
color_reset = '#[fg=white]' if args['tmux'] else '%{%f%}'
color_out = (
    color_green if len(filled) > 8
    else color_yellow if len(filled) > 4
    else color_red
)
percent = int(charge*100)
# sys.stdout.write(color_out + str(percent) + color_reset)
if args['clean']:
  color_out = ''
out = color_out + out + color_reset
sys.stdout.write(out)
