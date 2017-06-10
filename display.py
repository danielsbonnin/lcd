#!/usr/bin/env python          

import time
import serial      

class Display:
    def __init__(self):
        self.display = serial.Serial(          
            port='/dev/ttyAMA0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.scrollspeed = 0.5
        self.firstline =  "     Daniel     "
        self.secondline = "     Bonnin     "
        time.sleep(1)
    def clear(self):
        self.display.write(bytearray([0xFE, 0x80]))
        self.display.write("                ")
        self.display.write("                ")
    
    def refresh(self):
        self.display.write(bytearray([0xFE, 0x80]))
        self.display.write(self.firstline)
        self.display.write(self.secondline)

    def writeline(self, line):
        if len(line) > 16:
            line = line[0:16]
        elif len(line) < 16:
            line += " " * (16 - len(line))
        self.secondline = self.firstline
        self.firstline = line
        self.refresh()
    
    def setspeed(self, speed):
        speed = max(speed, 0.1)
        speed = min(speed, 1)
        self.scrollspeed = speed

    def linescroll(self, line):
        if len(line) > 32:
            line = line + " "
        else:
            line += " " * (32 - len(line))
        self.clear()
        for i in range(200):
            for j in range(0, (-1 * len(line)), -1):
                self.display.write(bytearray([0xFE, 0x80]))
                self.display.write(line[j:])
                time.sleep(self.scrollspeed)
            for j in range(len(line)):
                self.display.write(bytearray([0xFE, 0x80]))
                self.display.write(line[:j])
                time.sleep(self.scrollspeed)
                
if __name__ == "__main__":
    d = Display()
    d.linescroll("Daniel Bonnin is trying to make this work")
