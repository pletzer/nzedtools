#!/usr/bin/env python

"""
Example showing how to read a field using iris
"""

import sys
import argparse
import iris
from mpi4py import MPI
from pnumpy import CubeDecomp

sz = MPI.COMM_WORLD.Get_size()
rk = MPI.COMM_WORLD.Get_rank()

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
        decomp = CubeDecomp(sz, cube.shape)
        slab = decomp.getSlab(rk)
        if len(slab) == 0:
            if rk == 0:
                print('ERROR: could not find a valid decomposition')
                print('consider running with a different processor count')
                print('valid processor counts are: {}'.format(decomp.getNumberOfValidProcs()))
        else:
            # now read the local data MPI rank rk
            data = cube[slab]
            print('[{0}] {4} ({5}) slab = {1} data shape {2} type {3}'.format(rk, slab, 
                   data.shape, data.dtype, cube.var_name, cube.name()))

if not found:
    print('ERROR: could not find field {}'.format(args.field))
    sys.exit(3)

