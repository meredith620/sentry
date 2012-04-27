import CairoPlot
import cairo
import math
import sys
import os
import string

def main():
     data = {"john" : [50, 20, 0, 10, 30], "mary" : [0, 10, 30, 50, 100], "philip" : [20, 30, 40, 20, 10]}
     h_labels = ["jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008"]
     v_labels = ["jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008"]
     CairoPlot.dot_line_plot('dotline1', data, 250, 150, axis = True, grid = True)
     CairoPlot.dot_line_plot('dotline1_dots', data, 400, 300, h_labels = h_labels, v_labels = v_labels, axis = True, grid = True, dots = True)

     data2 = {"cpu":[32, 34, 34, 32, 34, 34, 32, 32, 32, 34, 34, 32, 29, 29, 34, 34, 34, 37,
                     37, 39, 42, 47, 50, 54, 57, 60, 60, 60, 60, 60, 60, 60, 62, 62, 60, 55,
                     55, 52, 47, 44, 44, 40, 40, 37, 34, 34, 32, 32, 32, 31, 100],
              "mem":[55, 52, 47, 44, 44, 40, 40, 37, 34, 34, 32, 32, 32, 31, 32, 62, 60, 55,
                     32, 34, 34, 32, 34, 34, 32, 32, 32, 34, 34, 32, 29, 29, 34, 34, 34, 37,
                     37, 39, 42, 47, 50, 54, 57, 60, 60, 60, 60, 60, 60, 60, 100]}
     h_labs = ["0:00", "3:00", "6:00", "9:00", "12:00", "15:00", "18:00", "21:00"]
     v_labs = ["","25%","50%","75%"]
     CairoPlot.dot_line_plot('dl1', data, 600, 500, axis = True, grid = True, dots = True)
     CairoPlot.dot_line_plot('dl1_dots',
                             data2,
                             1000,
                             500,
                             background = (204,204,204),
                             border = 0,
                             axis = True,
                             grid = True,
                             dots = True,
                             h_labels = h_labs,
                             v_labels = v_labs)

if __name__ == "__main__":
     main()
