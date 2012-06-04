#! /usr/bin/env python2

import sys
import os
import time
import Queue

cpuinfo = {}
dickinfo = {}
netinfo = {}

class InfoParser:
     """input lines, first line is the title, following lines are values
     e.g. 'time' 'cpu:%user' 'cpu:%nice' 'cpu:%system' 'cpu:%iowait' 'cpu:%idle'
     time val val val..."""
     def __init__(self, val_list):
          """init function dict = { title: ['cpu:%user', 'cpu:%nice', 'cpu:%system', 'cpu:%iowait', 'cpu:%idle'], cpu_num: [val%user, val%nice, val%system ...]}"""
          self.info_dict = {}
          self.info_dict["title"] = val_list[0].split()[3:]

     def parse_lines(self, val_list):
          self.info_dict.clear() # clear former infos
          line_num = len(val_list)
          for i in range(1, line_num):
               self.info_dict[val_list[2]] = val_list[i][3:]

     def get_title(self):
          

# class SarParser:
#      def __init__(self, cmd):
#           pass

if __name__ == "__main__":
     f=os.popen("sar -n DEV -n EDEV -u -d -r -p 1 1 | sed -e '/^Average:/d'")
     print("line: %s" % repr(f[2:4].split('\n')))
     
     f=os.popen("sar -n DEV -n EDEV -u -d -r -p 10 1 | sed -e '/^Average:/d'")
     raw = f.readlines()[1:]
     print("raw: %s" % raw)

     # que = Queue.Queue()
     # for i in range(len(raw)):
     #      que.put(raw[i])

     # while not que.empty():
     #      line = que.get()
     #      if line == "\n":
               
