#!/usr/bin/env python

import argparse
import numpy as np
from PIL import Image
from pathlib import PurePath

import py360convert

# Parsing command line arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description='Convertion between cubemap and equirectangular or equirectangular to perspective.')
parser.add_argument('--convert', choices=['c2e', 'e2c', 'e2p'], required=True,
                    help='What convertion to apply.')
parser.add_argument('--i', required=True,
                    help='Path to input image.')
parser.add_argument('--o', required=True,
                    help='Path to output image.')
parser.add_argument('--w', required=True, type=int,
                    help='Output width for c2e or e2p. Output cube faces width for e2c.')
parser.add_argument('--h', type=int,
                    help='Output height for c2e or e2p.')
parser.add_argument('--mode', default='bilinear', choices=['bilinear', 'nearest'],
                    help='Resampling method.')
parser.add_argument('--h_fov', type=float, default=60,
                    help='Horizontal field of view for e2p.')
parser.add_argument('--v_fov', type=float, default=60,
                    help='Vertical field of view for e2p.')
parser.add_argument('--u_deg', type=float, default=0,
                    help='Horizontal viewing angle for e2p.')
parser.add_argument('--v_deg', type=float, default=0,
                    help='Vertical viewing angle for e2p.')
parser.add_argument('--in_rot_deg', type=float, default=0,
                    help='Inplane rotation for e2p.')
parser.add_argument('--f', default='dice', choices=['dice', 'list', 'dict'],
                    help='Output format for e2c.')
args = parser.parse_args()


# Read image
img = np.array(Image.open(args.i))
if len(img.shape) == 2:
    img = img[..., None]

# Convert
if args.convert == 'c2e':
    out = py360convert.c2e(img, h=args.h, w=args.w, mode=args.mode)
elif args.convert == 'e2c':
    out = py360convert.e2c(img, face_w=args.w, mode=args.mode, cube_format=args.f)
elif args.convert == 'e2p':
    out = py360convert.e2p(img, fov_deg=(args.h_fov, args.v_fov), u_deg=args.u_deg, v_deg=args.v_deg,
                           out_hw=(args.h, args.w), in_rot_deg=args.in_rot_deg, mode=args.mode)
else:
    raise NotImplementedError('Unknown conversion')

# Output image
if (args.convert == 'e2c') and (args.f == 'list'):
    fparts = PurePath(args.o)

    pathout = str(fparts.parent) + '\\' + str(fparts.stem) + '1' + str(fparts.suffix)
    img1 = Image.fromarray(out[0].astype(np.uint8))
    img1.save(pathout)

    pathout = str(fparts.parent) + '\\' + str(fparts.stem) + '2' + str(fparts.suffix)
    img2 = Image.fromarray(out[1].astype(np.uint8))
    img2 = img2.transpose(method=Image.FLIP_LEFT_RIGHT)
    img2.save(pathout)

    pathout = str(fparts.parent) + '\\' + str(fparts.stem) + '3' + str(fparts.suffix)
    img3 = Image.fromarray(out[2].astype(np.uint8))
    img3 = img3.transpose(method=Image.FLIP_LEFT_RIGHT)
    img3.save(pathout)

    pathout = str(fparts.parent) + '\\' + str(fparts.stem) + '4' + str(fparts.suffix)
    img4 = Image.fromarray(out[3].astype(np.uint8))
    img4.save(pathout)

    pathout = str(fparts.parent) + '\\' + str(fparts.stem) + '5' + str(fparts.suffix)
    img5 = Image.fromarray(out[4].astype(np.uint8))
    img5 = img5.transpose(method=Image.FLIP_TOP_BOTTOM)
    img5.save(pathout)

    pathout = str(fparts.parent) + '\\' + str(fparts.stem) + '6' + str(fparts.suffix)
    img6 = Image.fromarray(out[5].astype(np.uint8))
    img6.save(pathout)
else:
    Image.fromarray(out.astype(np.uint8)).save(args.o)
