#!/usr/bin/env python2

import CairoPlot
import cairo
import math
import sys
import os
import string
from optparse import OptionParser

def main():
     size_limit = 1500 * 600;
     x_size = 1500
     y_size = 500
     
     parser = OptionParser()
     parser.add_option("-f", "--file", dest="filename",
                       help="input data file")
     parser.add_option("-o", "--output", dest="chartname",
                       help="output chart file")
     parser.add_option("-s", "--size", dest="size",
                       help="'xsize,ysize' length of the chart x*y<=%d" % size_limit)
     parser.add_option("-y", "--y-max", dest="y_max",
                       help="y max limit")
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
     if (x_size * y_size > size_limit):
          print("ERROR: x*y > %s" % size_limit)
          sys.exit(1)

     # init y range
     if (options.y_max):
          y_max = string.atoi(options.y_max)
               
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
          
     while True:
          l = ifile.readline()
          if len(l) == 0:
               break
          line_datas = l.split()

          if (len(line_datas) != len(items) + 2):
               continue
          # for (num, key) in enumerate(items):
          #      data_map[key].append(float(line_datas[num+2]) * 100)
          #      print("%s" % line_datas[num])
          # print("get line: %s" % l[:-1])
          data_map["cpu:%user"].append(float(line_datas[2]) * 100)
          data_map["net:eth0:out(MB/s)"].append((float(line_datas[24])/1.25))
          data_map["net:eth0:in(MB/s)"].append((float(line_datas[23])/1.25))
          
     # data = { "cpu":[32, 34, 34, 32, 34, 34, 32, 32, 32, 34, 34, 32, 29, 29, 34, 34, 34, 37,
     #                 37, 39, 42, 47, 50, 54, 57, 60, 60, 60, 60, 60, 60, 60, 62, 62, 60, 55,
     #                 55, 52, 47, 44, 44, 40, 40, 37, 34, 34, 32, 32, 32, 31, 32],
     #          "mem": [55, 52, 47, 44, 44, 40, 40, 37, 34, 34, 32, 32, 32, 31, 32, 62, 60, 55,
     #                  32, 34, 34, 32, 34, 34, 32, 32, 32, 34, 34, 32, 29, 29, 34, 34, 34, 37,
     #                  37, 39, 42, 47, 50, 54, 57, 60, 60, 60, 60, 60, 60, 60, 62]}
     use_data = {}
     use_data["cpu:%user"] = data_map["cpu:%user"]
     # use_data["net:eth0:out(MB/s)"] = data_map["net:eth0:out(MB/s)"]
     # use_data["net:eth0:in(MB/s)"] = data_map["net:eth0:in(MB/s)"]
     # ==========output file section==========
     h_labs = ["0:00", "3:00", "6:00", "9:00", "12:00", "15:00", "18:00", "21:00", "24:00"]
     v_labs = ["","25%","50%","75%","100%"]
     CairoPlot.dot_line_plot(options.chartname, use_data, x_size, y_size, background = (204,204,204), border = 5,
                             axis = True, grid = True, dots = True, h_labels = h_labs, v_labels = v_labs)

if __name__ == "__main__":
     main()
     
