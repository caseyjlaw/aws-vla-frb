## search all scans of an sdmfile

docker_rock.py search listsdms.txt

sdmfile=$(python next_to_search_sdm.py)

scan=$(python next_to_search_scan.py)

docker run --rm $config caseyjlaw/rtpipe-aws copyscan $sdmfile $scan # copy data for scan to instance

contid=`docker run -d $config caseyjlaw/rtpipe-aws search $sdmfile $scan` # search scan for transients in background

# products are backed up automatally to s3 after search completes

add_finish_to_complete.py $sdmfile $scan

************************************************************************
'''
add_finish_to_complete.py $sdmfile $scan
'''
does not work yet because python script behaves differently when pass environment varibales as arguments
