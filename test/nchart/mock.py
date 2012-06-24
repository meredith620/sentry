#! /usr/bin/env python2

import sys
import os
import time
import Queue

cpuinfo = {}
dickinfo = {}
netinfo = {}
               

def part_section(raw):
     """split raw list to sections
     {CPU:[title, value_line1, value_line2], mem:[title, value_line1, value_line2]...}
     """
     sect_dict = {}
     start_new_section = True
     for x in raw:
          # print("get line: %s" % x)
          if x == "\n":
               start_new_section = True
          else:
               vals = x.split()[2:]
               
               if start_new_section == True:
                    key = vals[0]
                    # print("find key: %s (%s)" % (key, repr(vals)))
                    if key.find("mem") != -1:
                         key = "MEM"
                    if key in sect_dict:
                         key = key + "_" + vals[1]                         
                    sect_dict[key] = []
                    sect_dict[key].append(vals)
                    start_new_section = False
               else:
                    sect_dict[key].append(vals)   
                    # print("key %s append %s" % (key, repr(vals)))                    
     return sect_dict

class InfoParser:
     """
     input lines, first line is the title, following lines are values
     e.g.
     'cpu:%user' 'cpu:%nice' 'cpu:%system' 'cpu:%iowait' 'cpu:%idle'
     val val val...
     """
     def __init__(self):
          pass
          
     def read_list(self, val_list):
          self.info_list = self.parse(val_list)
          
     def parse(self, val_list):
          return val_list

     def get_title(self):
          return self.info_list[0]
     def get_values(self):
          return self.info_list[1:]

class CpuInfoParser(InfoParser):
     """
     [title, all]
     """
     def parse(self, val_list):
          temp_list = val_list
          # handle title
          for i in range(1, len(temp_list[0])):
               temp_list[0][i] = "cpu" + temp_list[0][i]
          # handle value
          for i in range(1, 2):
               temp_list[i].remove(temp_list[i][5])
          return temp_list
     
class MemInfoParser(InfoParser):
     def parse(self, val_list):
          temp_list = val_list
          # handle title
          temp_list[0] = ["mem:total", "mem:free", "mem:used", "mem:free+cache+buffer", "mem:used-cache-buffer"]
          # handle value
          for i in range(1, 2):
               free = float(val_list[i][0]) / 1000
               used = float(val_list[i][1]) / 1000
               cache = float(val_list[i][4]) / 1000
               buffer = float(val_list[i][3]) / 1000
               temp_list[i] = [str(free+used), str(free), str(used), str(free + cache + buffer), str(used - cache - buffer)]
          return temp_list

class DiskInfoParser(InfoParser):
     def parse(self, val_list):
          temp_list = []
          # handle title
          temp_list.append(["disk:tps", "disk:read(MB/s)", "disk:write(MB/s)", "disk:avgrq-sz", "disk:await", "disk:svctm", "disk:%util"])
          # handle value
          for i in range(1, len(val_list)):
               temp_list.insert(i, [])
               temp_list[i].append(str(float(val_list[i][1])))
               temp_list[i].append(str(float(val_list[i][2])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][3])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][4])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][6])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][7])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][8])*512/1024/1024))
          return temp_list
     
if __name__ == "__main__":
     cpuinfo = CpuInfoParser()
     meminfo = MemInfoParser()
     diskinfo = DiskInfoParser()
     
     f=os.popen("sar -n DEV -n EDEV -u -d -r -p 1 1 | sed -e '/^Average:/d'")
     raw = f.readlines()[1:]
     # print("line: %s" % raw)
     part_dict = part_section(raw)
     print("split: %s" % repr(part_dict))     
     for (k,v) in part_dict.items():
          print("key: %s" % k)
          print("value: %s\n" % repr(v))
          if k.find("CPU") != -1:
               cpuinfo.read_list(v)
          elif k.find("MEM") != -1:
               meminfo.read_list(v)
          elif k.find("DEV") != -1:
               diskinfo.read_list(v)

     print("cpu title: %s\ncpu value: %s\n" % (cpuinfo.get_title(), cpuinfo.get_values()))
     print("mem title: %s\nmem value: %s\n" % (meminfo.get_title(), meminfo.get_values()))
     print("disk title: %s\ndisk value: %s\n" % (diskinfo.get_title(), diskinfo.get_values()))
          
     # f=os.popen("sar -n DEV -n EDEV -u -d -r -p 10 1 | sed -e '/^Average:/d'")
     # raw = f.readlines()[1:]
     # print("raw: %s" % raw)

     # que = Queue.Queue()
     # for i in range(len(raw)):
     #      que.put(raw[i])

     # while not que.empty():
     #      line = que.get()
     #      if line == "\n":
               
