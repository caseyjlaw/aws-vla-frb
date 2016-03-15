#!/usr/bin/env python

import click, os, glob, boto3, gzip

s3 = boto3.resource('s3')
databucket = 'ska-vla-frb-pds'
candsbucket = 'ska-vla-frb-cands'


@click.group('control')
def cli():
    pass


@cli.command()
@click.option('--bucketname', default=databucket)
@click.option('--sort', default=True)
def listsdms(bucketname, sort):
    """ lists all sdms in the s3 bucket in MJD (time) order """

    bucket = s3.Bucket(bucketname)
    sdmlist = set([obj.key.split('/')[0] for obj in bucket.objects.all()])
    if sort: sdmlist = sorted(sdmlist, key=lambda x: '.'.join(x.split('.')[-2:]))
    print(sdmlist)


@cli.command()
@click.argument('sdmfile')
@click.option('--bucketname', default=databucket)
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
@click.option('--bucketname', default=databucket)
def copyscan(sdmfile, scan, bucketname):
    """ Copies sdm plus bdf for single scan. """

    assert sdmfile
    assert scan
    if not os.path.exists(sdmfile): copyskeleton(sdmfile, bucketname=bucketname)
    if not os.path.exists(sdmfile + '.GN'): copygain(sdmfile, bucketname=bucketname)

    scans = getscans(sdmfile, bucketname=bucketname)

    bucket = s3.Bucket(bucketname)
    sdm_object = [obj for obj in bucket.objects.all()
                  if sdmfile in obj.key and scans[scan] in obj.key]
    assert len(sdm_object) == 1
    sdmpath = sdm_object[0].key

    print('Copying {}'.format(sdmpath))
    bucket.download_file(sdmpath, sdmpath)

    # check if data is zipped (done for NERSC data)
    if '.gz' in sdmpath:
        print('Unzipping {}'.format(sdmpath))
        with gzip.open(sdmpath, 'rb') as zf:
            data = zf.read()

        with gzip.open(sdmpath[:-3], 'wb') as zf:
            zf.write(data)


@cli.command()
@click.argument('sdmfile')
@click.argument('scan', type=int)
def search(sdmfile, scan, **kwargs):
    """ Search scan of sdmfile for transients. Uses rtpipe_cbe.conf file in repo. 

    kwargs is passed directly to rt.set_pipeline to customize search.
    """

    import rtpipe.RT as rt
    import rtpipe.parsecands as pc

    if not os.path.exists(sdmfile + '.GN'): copygain(sdmfile, bucketname=databucket)

    d = rt.set_pipeline(sdmfile, scan, paramfile='rtpipe_cbe.conf',
                        fileroot=sdmfile, nologfile=True, **kwargs)
    rt.pipeline(d, range(d['nsegments']))
    pc.merge_segments(sdmfile, scan)

    backupproducts(sdmfile, scan, bucketname=candsbucket)


@cli.command()
@click.argument('sdmfile')
@click.option('--bucketname', default=candsbucket)
def mergecands(sdmfile, bucketname):
    """ Merge cands and noise files for given sdmfile """

    import rtpipe.parsecands as pc

    copyproducts(sdmfile, bucketname=bucketname)
    pc.merge_cands(glob.glob('cands_{}*pkl'.format(sdmfile)), sdmfile)
    pc.merge_noises(glob.glob('noise_{}*pkl'.format(sdmfile)), sdmfile)


@cli.command()
@click.argument('sdmfile')
def jupyter(sdmfile):
    """ Merge candidates and run jupyter notebook server to visualize. """

    import subprocess, shutil
    shutil.move('/base.ipynb', os.path.join('/work', '{}.ipynb'.format(sdmfile)))

    subprocess.call(['jupyter', 'notebook', '--notebook-dir=/work', '--no-browser', '--ip=0.0.0.0'])


@cli.command()
@click.argument('sdmfile')
@click.option('--bucketname', default=candsbucket)
def savenotebook(sdmfile, bucketname):
    """ Merge candidates and run jupyter notebook server to visualize. """

    bucket = s3.Bucket(bucketname)
    notebook = os.path.abspath('{}.ipynb'.format(sdmfile))
    print('Copying {}'.format(notebook))
    bucket.upload_file(notebook, os.path.join(sdmfile, os.path.basename(notebook)))


def copyproducts(sdmfile, bucketname=candsbucket):
    """ Copy all products for given sdmfile into instance for analysis. """

    bucket = s3.Bucket(bucketname)
    products = [obj for obj in bucket.objects.all()
                if sdmfile in obj.key]

    for product in products:
        print('Copying {}'.format(product))
        bucket.download_file(product, os.path.basename(product))


def backupproducts(sdmfile, scan, bucketname=candsbucket):
    """ Sync search products to s3 bucket for backup

    sdmfile is original data name, which is used as directory to store products in s3.
    productlist is list of files to back up (full path).
    """

    bucket = s3.Bucket(bucketname)
    products = [os.path.abspath(prod) for prod in glob.glob('cands_{}_sc{}*'.format(sdmfile, scan)) + glob.glob('noise_{}_sc*'.format(sdmfile, scan))]
    
    for product in products:
        print('Copying {}'.format(product))
        bucket.upload_file(product, os.path.join(sdmfile, os.path.basename(product)))


def getscans(sdmfile, bucketname):
    import sdmpy

    if not os.path.exists(sdmfile): copyskeleton(sdmfile, bucketname=bucketname)

    sdm = sdmpy.SDM(sdmfile)
    scans = dict((int(sdm['Main'][row].scanNumber), sdm['Main'][row].dataUID.split('/')[-1])
             for row in range(len(sdm['Main'])))

    return scans


def copyskeleton(sdmfile, bucketname=databucket):
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


def copygain(sdmfile, bucketname=databucket):
    """ Finds gainfile in s3 for given sdmfile """

    assert sdmfile

    bucket = s3.Bucket(bucketname)
    gain_object = [obj for obj in bucket.objects.all()
                  if sdmfile in obj.key and 'gains' in obj.key]
    assert len(gain_object) == 1
    gainpath = gain_object[0].key

    print('Copying {}'.format(gainpath))
    bucket.download_file(gainpath, os.path.basename(gainpath))


if __name__ == '__main__':
    cli()
