#!/usr/bin/env python

"""
Example showing how to read a field using iris
"""

import sys
import argparse
import iris

iris.FUTURE.netcdf_promote = True

parser = argparse.ArgumentParser(description='Read a field from a file')
parser.add_argument('--input', type=str, dest='filename', default='',
                    help='input file name')
parser.add_argument('--field', type=str, dest='field', default='',
                    help='field (variable) name')
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
        print ('{0}: ({1}) shape {2} type {3}'.format(cube.var_name, cube.name(), cube.shape, cube.dtype))

if not found:
    print('ERROR: could not find field {}'.format(args.field))
    sys.exit(3)

