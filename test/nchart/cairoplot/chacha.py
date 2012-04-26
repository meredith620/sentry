#!/usr/bin/env python2

import CairoPlot
import cairo
import math
import sys
import os
import string
from optparse import OptionParser

def main():
     x_size = 2880
     y_size = 700
     
     parser = OptionParser()
     parser.add_option("-f", "--file", dest="filename",
                       help="input data file")
     parser.add_option("-o", "--output", dest="chartname",
                       help="output chart file")
     parser.add_option("-s", "--size", dest="size",
                       help="'xsize,ysize' ")
     parser.add_option("-t", "--type", dest="type",
                       help="'t1,t2,t3' draw type lines")
     (options, args) = parser.parse_args(sys.argv[1:])          
     if (options.filename == None or options.chartname == None):
          parser.print_help()
          sys.exit(1)
     # init x,y size
     if (options.size):
          size = options.size
          xy_pair = size.split(",")
          if len(xy_pair) == 2:
               x_size = string.atoi(xy_pair[0])
               y_size = string.atoi(xy_pair[1])
          else :
               parser.print_help()
               sys.exit(1)
               
     if (options.type):
          val_types = options.type.split(",")
     else:val_types = ["user", "system", "iowait", "nice"] #default
                 
     # ===========input file section=============
     ifile = open(options.filename)
     l = ifile.readline()
     items = l.split()
     if (len(items) == 0):
          print("%s's first line is not title!" % options.filename)
          sys.exit(1)

     empty_data = []
     for x in xrange(1440):
          empty_data.append(0)
     data_map = {}     
     for (num,ite) in enumerate(items):
          data_map[ite] = []

     maxn = 0.0
     while True:
          l = ifile.readline()
          if len(l) == 0:
               break
          line_datas = l.split()

          if (len(line_datas) != len(items) + 1):
               continue
          for (num, key) in enumerate(items):
               for val_t in val_types:
                    if (key.find(val_t) != -1):
                         val = float(line_datas[num+1])
                         data_map[key].append(val)
                         if (val > maxn): maxn = val
     print("max: %f" % maxn)
          # data_map["cpu:%user"].append(float(line_datas[2]) * 100)
          # data_map["net:eth0:out(MB/s)"].append((float(line_datas[24])/1.25))
          # data_map["net:eth0:in(MB/s)"].append((float(line_datas[23])/1.25))
          
     data = { "cpu":[32, 34, 34, 32, 34, 34, 32, 32, 32, 34, 34, 32, 29, 29, 34, 34, 34, 37,
                     37, 39, 42, 47, 50, 54, 57, 60, 60, 60, 60, 60, 60, 60, 62, 62, 60, 55,
                     55, 52, 47, 44, 44, 40, 40, 37, 34, 34, 32, 32, 32, 200, 150],
              "mem": [55, 52, 47, 44, 44, 40, 40, 37, 34, 34, 32, 32, 32, 31, 32, 62, 60, 55,
                      32, 34, 34, 32, 34, 34, 32, 32, 32, 34, 34, 32, 29, 29, 34, 34, 34, 37,
                      37, 39, 42, 47, 50, 54, 57, 60, 60, 60, 60, 60, 60, 60, 100]}
     use_data = {}
     for k in data_map.keys():
          for val_t in val_types:
               if (k.find(val_t) != -1):
                    use_data[k] = data_map[k]
                    print("draw key: %s" % k)
     #use_data["net:eth0:out(MB/s)"] = data_map["net:eth0:out(MB/s)"]
     #use_data["net:eth0:in(MB/s)"] = data_map["net:eth0:in(MB/s)"]
     # ==========output file section==========
     h_labs = ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00" , "11:00", "12:00", "13:00", "14:00",  "15:00","16:00" ,"17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
     v_labs = ["", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%"]
     CairoPlot.dot_line_plot(options.chartname, use_data, x_size, y_size, background = (204,204,204), border = 0,
                             axis = True, grid = True, dots = False, h_labels = h_labs)#, v_labels = v_labs)

if __name__ == "__main__":
     main()
     
