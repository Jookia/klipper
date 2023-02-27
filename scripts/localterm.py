#!/usr/bin/env python3

import serial
import readline

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

with serial.Serial('/tmp/printer', 115200, timeout=0.5) as ser:
    while True:
        line = input('klipper> ')
        ser.write(line.encode('utf-8') + b'\n')
        for l in ser.readlines():
            print(l.decode('utf-8')[:-1])
