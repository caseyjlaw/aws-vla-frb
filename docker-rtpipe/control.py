#!/usr/bin/env python

import click, os, boto3

s3 = boto3.resource('s3')
bucketname = 'ska-vla-frb-pds'


@click.group('control')
def cli():
    pass


@cli.command()
@click.option('--bucketname', default=bucketname)
@click.option('--sort', default=True)
def listsdms(bucketname, sort):
    """ lists all sdms in the s3 bucket in MJD (time) order """

    bucket = s3.Bucket(bucketname)
    sdmlist = set([obj.key.split('/')[0] for obj in bucket.objects.all()])
    if sort: sdmlist = sorted(sdmlist, key=lambda x: '.'.join(x.split('.')[-2:]))
    print(sdmlist)


@cli.command()
@click.argument('sdmfile')
@click.option('--bucketname', default=bucketname)
def listscans(sdmfile, bucketname):
    """ Get dict of (scan, bdfnum) from Main.xml. Creates skeleton sdm file locally, if not available. """

    import sdmpy

    assert sdmfile
    if not os.path.exists(sdmfile): copyskeleton(sdmfile, bucketname=bucketname)

    sdm = sdmpy.SDM(sdmfile)
    print('List of scans:')
    for row in range(len(sdm['Main'])):
        scanIntent = sdm['Scan'][row].scanIntent
        if 'TARGET' in scanIntent:
            intent = 'TARGET'
        elif 'CALIBRATE' in scanIntent:
            intent = 'CALIBRATE'
        else:
            intent = 'Other'
        print('Scan {}:{}, {}, {} GB'.format(sdm['Main'][row].scanNumber, sdm['Scan'][row].sourceName, intent, int(sdm['Main'][row].dataSize)/1024**3))


@cli.command()
@click.argument('sdmfile')
@click.argument('scan', type=int)
@click.option('--bucketname', default=bucketname)
def copyscan(sdmfile, scan, bucketname):
    """ Copies sdm plus bdf for single scan. """

    assert sdmfile
    assert scan
    if not os.path.exists(sdmfile): copyskeleton(sdmfile, bucketname=bucketname)

    scans = getscans(sdmfile, bucketname=bucketname)

    bucket = s3.Bucket(bucketname)
    sdm_object = [obj for obj in bucket.objects.all()
                  if sdmfile in obj.key and scans[scan] in obj.key]
    assert len(sdm_object) == 1
    sdmpath = sdm_object[0].key

    print('Copying {}'.format(sdmpath))
    bucket.download_file(sdmpath, sdmpath)


@cli.command('search')
@click.argument('sdmfile')
@click.argument('scan', type=int)
def search(sdmfile, scan):
    """ Search scan of sdmfile for transients. Uses rtpipe_cbe.conf file in repo. """

    import rtpipe.RT as rt
    import rtpipe.parsecands as pc

    d = rt.set_pipeline(sdmfile, scan, paramfile='rtpipe_cbe.conf',
                        fileroot=sdmfile, nologfile=True)
    rt.pipeline(d, range(d['nsegments']))
    pc.merge_segments(sdmfile, scan)


@cli.command('cleanup')
def cleanup():
    """ Merge cands and noise files """

    pass


def getscans(sdmfile, bucketname):
    import sdmpy

    if not os.path.exists(sdmfile): copyskeleton(sdmfile, bucketname=bucketname)

    sdm = sdmpy.SDM(sdmfile)
    scans = dict((int(sdm['Main'][row].scanNumber), sdm['Main'][row].dataUID.split('/')[-1])
             for row in range(len(sdm['Main'])))

    return scans


def copyskeleton(sdmfile, bucketname=bucketname):
    """ Copies directory structure and metadata for sdm from s3 (no bdfs) """

    assert sdmfile

    bucket = s3.Bucket(bucketname)
    sdm_objects = [obj for obj in bucket.objects.all()
                   if sdmfile in obj.key]
    metadata_objects = [obj for obj in sdm_objects
                        if obj.key.split('.')[-1] in ['xml', 'bin']]

    if metadata_objects:
        # make space for data locally
        os.mkdir(sdmfile)
        os.mkdir(sdmfile + '/ASDMBinary')

        for obj in metadata_objects:
            print('Copying {}'.format(obj.key))
            bucket.download_file(obj.key, obj.key)
    else:
        print('no metadata objects found for {}.'.format(sdmfile))


if __name__ == '__main__':
    cli()
