#!/usr/bin/env python

import argparse, os, boto3

parser = argparse.ArgumentParser()
parser.add_argument('mode', help='Function to run')
parser.add_argument('--sdmfile', help='Name of SDM data file', default=None)
parser.add_argument('--scan', type=int, help='Scan number to search', default=0)
args = parser.parse_args()
mode = args.mode
sdmfile = args.sdmfile
scan = args.scan

s3 = boto3.resource('s3')


def listsdms(bucketname='ska-vla-frb-pds', sort=True):
    """ lists all sdms in the s3 bucket in MJD (time) order """

    bucket = s3.Bucket(bucketname)
    sdmlist = set([obj.key.split('/')[0] for obj in bucket.objects.all()])
    if sort: sdmlist = sorted(sdmlist, key=lambda x: '.'.join(x.split('.')[-2:]))

    return sdmlist


def copyskeleton(sdmfile, bucketname='ska-vla-frb-pds'):
    """ Copies directory structure and metadata for sdm from s3 (no bdfs) """

    assert sdmfile

    bucket = s3.Bucket(bucketname)
    sdm_objects = [obj for obj in bucket.objects.all() if sdmfile in obj.key]
    metadata_objects = [obj for obj in sdm_objects if obj.key.split('.')[-1] in ['xml', 'bin']]

    if metadata_objects:
        # make space for data locally
        os.mkdir(sdmfile)
        os.mkdir(sdmfile + '/ASDMBinary')

        for obj in metadata_objects:
            print('Copying {}'.format(obj.key))
            bucket.download_file(obj.key, obj.key)
    else:
        print('no metadata objects found for {}.'.format(sdmfile))


def listscans(sdmfile, bucketname='ska-vla-frb-pds'):
    """ Get dict of (scan, bdfnum) from Main.xml. Creates skeleton sdm file locally, if not available. """

    import sdmpy

    assert sdmfile
    if not os.path.exists(sdmfile): copyskeleton(sdmfile, bucketname=bucketname)

    sdm = sdmpy.SDM(sdmfile)
    scans = dict((int(sdm['Main'][row].scanNumber), sdm['Main'][row].dataUID.split('/')[-1])
             for row in range(len(sdm['Main'])))

    return scans


def copyscan(sdmfile, scan, bucketname='ska-vla-frb-pds'):
    """ Copies sdm plus bdf for single scan. """

    assert sdmfile
    assert scan
    if not os.path.exists(sdmfile): copyskeleton(sdmfile, bucketname=bucketname)

    scans = listscans(sdmfile, bucketname=bucketname)

    bucket = s3.Bucket(bucketname)
    sdm_object = [obj for obj in bucket.objects.all()
                  if sdmfile in obj.key and scans[scan] in obj.key]
    assert len(sdm_object) == 1
    sdmpath = sdm_object[0].key

    bucket.download_file(sdmpath, sdmpath)


def search(sdmfile, scan):
    """ Search scan of sdmfile for transients. Uses rtpipe_cbe.conf file in repo. """

    import rtpipe.RT as rt

    d = rt.set_pipeline(sdmfile, scan, paramfile='rtpipe_cbe.conf',
                        fileroot=sdmfile, nologfile=True)
    rt.pipeline(d, range(d['nsegments']))


def cleanup():
    """ Merge cands and noise files """

    pass


if __name__ == '__main__':

    if mode == 'listsdms':
        print(listsdms())
    elif mode == 'copyskeleton':
        copyskeleton(sdmfile)
    elif mode == 'listscans':
        print(listscans(sdmfile))
    elif mode == 'copyscan':
        copyscan(sdmfile, scan)
    elif mode == 'search':
        search(sdmfile, scan)
    else:
        print('\"{}\" is not a recognized mode. Try \"listsdms\", \"copyskeleton\", \"listscans\", \"copyscan\", or \"search\".'.format(mode))
