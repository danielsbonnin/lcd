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
        self.verticalspeed = 1
        self.firstline =  "                "
        self.secondline = "                "
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
        self.firstline = self.secondline
        self.secondline = line
        self.refresh()
    
    def setspeed(self, speed):
        speed = max(speed, 0.2)
        speed = min(speed, 1)
        self.scrollspeed = speed

    def linescroll(self, line, reps=200, coljump=2):
        line = " " * 16 + line + " " * 16
        self.clear()
        for i in range(reps):
            try:
                for j in range(16, len(line) + coljump, coljump):
                    self.display.write(bytearray([0xFE, 0x80]))
                    self.display.write(line[j - 16:j])
                    time.sleep(self.scrollspeed)
            except KeyboardInterrupt:
                self.clear()
                exit()
        self.clear()
    
    def verticalscroll(self, text, reps=200):
        text = text.splitlines()
        lines = []
        for i in text:
            if len(i) < 16:
                filler = " " * (16 - len(i))
                lines.append(i + filler)
            elif len(i) == 16:
                lines.append(i)
            else:
                newline = ""
                for word in i.split(" "):
                    if len(word) > 15:
                        word = word[0:15]
                    if len(newline) + len(word) > 15:
                        lines.append(newline + " ")
                        newline = word
                    else:
                        if len(newline) == 0:
                            newline = word
                        else:
                            newline += " " + word
                if len(newline) > 0:
                    lines.append(newline)
        print(lines)
        for i in range(reps):
            try: 
                for j in lines:
                    self.writeline(j)
                    time.sleep(self.verticalspeed)
                self.writeline(" " * 16)
                time.sleep(self.verticalspeed)
                self.writeline(" " * 16)
                time.sleep(self.verticalspeed)
            except KeyboardInterrupt:
                self.clear()
                exit()
        self.clear()

