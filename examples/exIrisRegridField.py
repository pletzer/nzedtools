#!/usr/bin/env python

"""
Example showing how to read a field using iris
"""

import sys
import argparse
import iris
import numpy
from numpy import linspace

iris.FUTURE.netcdf_promote = True

parser = argparse.ArgumentParser(description='Regrid a field')
parser.add_argument('--input', type=str, dest='filename', default='',
                    help='input file name')
parser.add_argument('--field', type=str, dest='field', default='',
                    help='field (variable) name')
parser.add_argument('--lat_target', type=str, dest='lat_target', default='linspace(-90., 90., 11)',
                    help='target latitudes')
parser.add_argument('--lon_target', type=str, dest='lon_target', default='linspace(0., 360., 21)',
                    help='target longitudes')
parser.add_argument('--mode', type=str, dest='mode', default='linear',
                    help='either "nearest", "linear" or "area"')

args = parser.parse_args()

if args.filename is '':
    print('ERROR: must provide file name (--input)')
    parser.print_help()
    sys.exit(1)

if args.field is '':
    print('ERROR: must provide field name (--field)')
    parser.print_help()
    sys.exit(2)

cubes = iris.load(args.filename)

found = False
for cube in cubes:
    if cube.var_name == args.field:
        found = True
        lats = eval(args.lat_target)
        lons = eval(args.lon_target)
        nlats = len(lats)
        nlons = len(lons)
        targetCube = iris.cube.Cube(numpy.zeros((nlats, nlons), numpy.float32))
        # add a coordinate system
        cs = iris.coord_systems.GeogCS(6371229)
        targetCube.add_dim_coord(iris.coords.DimCoord(eval(args.lat_target), 'latitude', units='degrees', coord_system=cs), 0)
        targetCube.add_dim_coord(iris.coords.DimCoord(eval(args.lon_target), 'longitude', units='degrees', coord_system=cs), 1)
        regriddedData = cube.regrid(targetCube, iris.analysis.Linear())
        print(regriddedData.data)

if not found:
    print('ERROR: could not find field {}'.format(args.field))
    sys.exit(3)

