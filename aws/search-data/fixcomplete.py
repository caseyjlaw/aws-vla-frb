import boto3, csv

s3 = boto3.resource('s3')
candsbucket = 'ska-vla-frb-cands'

def productlist(bucketname=candsbucket):
    """ Get all cands/noise products as (sdmfile, scan) lists """

    bucket = s3.Bucket(bucketname)
    sdmlist = list(set([obj.key.split('/')[0] for obj in bucket.objects.all()]))

    products = []
    for sdm in sdmlist:
        # get all products for this sdm
        prods = [obj.key for obj in bucket.objects.all() if sdm in obj.key]

        # filter to list of cands and noise products
        candscans = [int(pr.rstrip('.pkl')[pr.find('_sc') + 3:]) for pr in prods if (('cands' in pr) and ('pkl' in pr))]
        noisescans = [int(pr.rstrip('.pkl')[pr.find('_sc') + 3:]) for pr in prods if (('noise' in pr) and ('pkl' in pr))]

        # for each scan in both lists, add to products list
        for scan in list(set(candscans + noisescans)):
            if (scan in candscans) and (scan in noisescans):
                products.append( (sdm, scan) )

    return products


def write(products, filename="complete.csv"):
    """ Write products (sdmfile, scan) to output csv file """

    with open(filename, "w") as completeFile:
        completeWriter = csv.writer(completeFile, lineterminator = "\n")
        for sdmfile, scan in products:
            completeWriter.writerow([sdmfile] + [scan])

products = productlist()
write(products)
