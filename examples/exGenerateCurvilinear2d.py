#!/usr/bin/env python

"""
Example showing how to generate curvilinear data in 2d
"""

import sys
import argparse
import iris
import numpy
from numpy import linspace
from math import sin, cos, tan, atan2, exp, log, log10, pi, e, acos, asin, atan

iris.FUTURE.netcdf_promote = True
iris.FUTURE.netcdf_no_unlimited = True

parser = argparse.ArgumentParser(description='Generate curvilinear data in 2d')
parser.add_argument('--nj', type=int, dest='nj', default=11, 
                    help='dimension in the slow varying axis')
parser.add_argument('--ni', type=int, dest='ni', default=21, 
                    help='dimension in the fast varying axis')
parser.add_argument('--lat', type=str, dest='lat', default='-90. + 180.*y', 
                    help='latitude expression of x and y, 0 <= x, y <= 1')
parser.add_argument('--lon', type=str, dest='lon', default='0. + 360.*x', 
                    help='longitude expression of x and y, 0 <= x, y <= 1')
parser.add_argument('--expr', type=str, dest='expr', default='x**2*y', 
                    help='data expression of x and y, 0 <= x, y <= 1')
parser.add_argument('--output', type=str, dest='filename', default='',
                    help='output file name')

args = parser.parse_args()

if args.filename is '':
    print('ERROR: must provide file name (--output)')
    parser.print_help()
    sys.exit(1)

# generate the 2d lat-lon grids

nj = args.nj
ni = args.ni

# latitudes and longitudes on the curvilinear grid
lats = numpy.zeros((nj, ni), numpy.float64)
lons = numpy.zeros((nj, ni), numpy.float64)
# data container
data = numpy.zeros((nj, ni), numpy.float32)

dy = 1.0/float(nj - 1)
dx = 1.0/float(ni - 1)
for j in range(nj):
    y = 0. + dy*j
    for i in range(ni):
        x = 0. + dx*i
        lats[j, i] = eval(args.lat)
        lons[j, i] = eval(args.lon)
        data[j, i] = eval(args.expr)

# create a cube
cube = iris.cube.Cube(data, 'air_temperature')
cube.add_aux_coord(iris.coords.AuxCoord(lats, "latitude"), (0, 1))
cube.add_aux_coord(iris.coords.AuxCoord(lons, "longitude"), (0, 1))

iris.save(cube, args.filename)
