#! /usr/bin/env python2

import sys
import os
import time
import Queue

cpuinfo = {}
dickinfo = {}
netinfo = {}
diskinfo = {}
               
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
          temp_list[0] = ["CPU", "cpu:%user", "cpu:%nice", "cpu:%system", "cpu:%iowait", "cpu:%idle"]
          # handle value
          for i in range(1, 2):
               temp_list[i].remove(temp_list[i][5])
          return temp_list
     
class MemInfoParser(InfoParser):
     def parse(self, val_list):
          temp_list = val_list
          # handle title
          temp_list[0] = ["MEM", "mem:total", "mem:free", "mem:used", "mem:free+cache+buffer", "mem:used-cache-buffer"]
          # handle value
          for i in range(1, 2):
               free = float(val_list[i][0]) / 1000
               used = float(val_list[i][1]) / 1000
               cache = float(val_list[i][4]) / 1000
               buffer = float(val_list[i][3]) / 1000
               temp_list[i] = ["all", str(free+used), str(free), str(used), str(free + cache + buffer), str(used - cache - buffer)]
          return temp_list

class DiskInfoParser(InfoParser):
     def parse(self, val_list):
          temp_list = []
          # handle title
          temp_list.append(["DEV", "disk:tps", "disk:read(MB/s)", "disk:write(MB/s)", "disk:avgrq-sz", "disk:await", "disk:svctm", "disk:%util"])
          # handle value
          for i in range(1, len(val_list)):
               temp_list.insert(i, [])
               temp_list[i].append(val_list[i][0])
               temp_list[i].append(str(float(val_list[i][1])))
               temp_list[i].append(str(float(val_list[i][2])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][3])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][4])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][6])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][7])*512/1024/1024))
               temp_list[i].append(str(float(val_list[i][8])*512/1024/1024))
          return temp_list
          
class NetInfoParser(InfoParser):
     def parse(self, val_list):
          temp_list = []
          temp_list.append(["IFACE", "in(MB/s)", "out(MB/s)"])
          for i in range (1, len(val_list)):
                  temp_list.insert(i, [])
                  temp_list[i].append(val_list[i][0])
                  temp_list[i].append(str(float(val_list[i][3])/1000))
                  temp_list[i].append(str(float(val_list[i][4])/1000))
	  return temp_list

class NetErrInfoParser(InfoParser):
     def parse(self, val_list):
          temp_list = []
          temp_list.append(["IFACE_ERR", "indrop(packet/s)", "outdrop(packet/s)"])
          for i in range (1, len(val_list)):
                  temp_list.insert(i, [])
                  temp_list[i].append(val_list[i][0])
                  temp_list[i].append(str(float(val_list[i][4])/1000))
                  temp_list[i].append(str(float(val_list[i][5])/1000))
          return temp_list
          
class RawParser:
     def __init__(self):
          self.cpuinfo = CpuInfoParser()
          self.meminfo = MemInfoParser()
          self.diskinfo = DiskInfoParser()
          self.netinfo = NetInfoParser()
          self.neterrinfo = NetErrInfoParser()

     def part_section(self, raw):
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
                    temp = x.split()
                    if temp[1] == "AM" or temp[1] == "PM": # 24hour or 12hour
                         vals = temp[2:]
                    else: vals = temp[1:]
                    if start_new_section == True:
                         key = vals[0]
                         print("find key: %s (%s)" % (key, repr(vals)))
                         # if key.find("mem") != -1:
                         #      key = "MEM"
                         if key in sect_dict:
                              key = key + "_" + vals[1]
                         sect_dict[key] = []
                         sect_dict[key].append(vals)
                         start_new_section = False
                    else:
                         sect_dict[key].append(vals)
                         # print("key %s append %s" % (key, repr(vals)))
          return sect_dict
     
     def parse_raw(self, raw):
          part_dict = self.part_section(raw)
          print("split: %s" % repr(part_dict))
          for (k,v) in part_dict.items():
               print("key: %s" % k)
               print("value: %s\n" % repr(v))
               if k.find("CPU") != -1:
                    self.cpuinfo.read_list(v)
               elif k.find("mem") != -1:
                    self.meminfo.read_list(v)
               elif k.find("DEV") != -1:
                    self.diskinfo.read_list(v)
               elif k.find("IFACE") != -1:
                    if v[0][1].find("err") != -1:
        		self.neterrinfo.read_list(v)
                    else:
                        self.netinfo.read_list(v)


if __name__ == "__main__":

     rpsr = RawParser()
     
     f=os.popen("sar -n DEV -n EDEV -u -d -r -p 1 1 | sed -e '/^Average:/d'")
     raw = f.readlines()[1:]
     print("line: %s" % raw)
     rpsr.parse_raw(raw)

     print("cpu title: %s\ncpu value: %s\n" % (rpsr.cpuinfo.get_title(), rpsr.cpuinfo.get_values()))
     print("mem title: %s\nmem value: %s\n" % (rpsr.meminfo.get_title(), rpsr.meminfo.get_values()))
     print("disk title: %s\ndisk value: %s\n" % (rpsr.diskinfo.get_title(), rpsr.diskinfo.get_values()))
     print("net title: %s\nnet value: %s\n" % (rpsr.netinfo.get_title(), rpsr.netinfo.get_values()))
     print("neterr title: %s\nneterr value: %s\n" % (rpsr.neterrinfo.get_title(), rpsr.neterrinfo.get_values()))
          
     # f=os.popen("sar -n DEV -n EDEV -u -d -r -p 10 1 | sed -e '/^Average:/d'")
     # raw = f.readlines()[1:]
     # print("raw: %s" % raw)

     # que = Queue.Queue()
     # for i in range(len(raw)):
     #      que.put(raw[i])

     # while not que.empty():
     #      line = que.get()
     #      if line == "\n":
               
