import rtpipe.RT as rt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('sdmfile', help='Name of SDM data file')
parser.add_argument('scan', type=int, help='Scan number to search')
args = parser.parse_args()

d = rt.set_pipeline(args.sdmfile, args.scan, paramfile='rtpipe_cbe.conf', fileroot=args.sdmfile, nologfile=True)
rt.pipeline(d, range(d['nsegments']))
