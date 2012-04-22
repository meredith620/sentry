#!/usr/bin/env python2

import os
import sys
import math
import string
from optparse import OptionParser
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import XYLineChart
from pygooglechart import Axis

def main():
     size_limit = 3000 * 100;
     x_size = 3000
     y_size = 100
     y_max = 100
     
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
               
     # input file section
     ifile = open(options.filename)
     while True:
          l = ifile.readline()
          if len(l) == 0:
               break
          print("get line: %s" % l[:-1])
     data = [
          32, 34, 34, 32, 34, 34, 32, 32, 32, 34, 34, 32, 29, 29, 34, 34, 34, 37,
          37, 39, 42, 47, 50, 54, 57, 60, 60, 60, 60, 60, 60, 60, 62, 62, 60, 55,
          55, 52, 47, 44, 44, 40, 40, 37, 34, 34, 32, 32, 32, 31, 32
          ]
     data2 = [
          55, 52, 47, 44, 44, 40, 40, 37, 34, 34, 32, 32, 32, 31, 32, 62, 60, 55,
          32, 34, 34, 32, 34, 34, 32, 32, 32, 34, 34, 32, 29, 29, 34, 34, 34, 37,        
          37, 39, 42, 47, 50, 54, 57, 60, 60, 60, 60, 60, 60, 60, 62
          ]
     data_list = [data, data2]
     # output file section
     chart = SimpleLineChart(x_size, y_size, y_range=[0, y_max])
	# init color
     RR=16; GG=16; BB=160
     color_list = []
     for x in range(len(data_list)):
          RR+=15;GG+=15;BB+=15
          color_list.append("%s%s%s" %
                            (str(hex(RR%255))[2:],
                             str(hex(GG%255))[2:],
                             str(hex(BB%255))[2:]) )
     #print(color_list)
     
                            

if __name__ == "__main__":
     main()
     
