#! /bin/bash
# Copyright 2015-2016 Peter Williams <peter@newton.cx>
# Licensed under the MIT License.
#
# This is the "entrypoint" script for the rtpipe aws project
# if using "docker run <imagename> search sdmname",
# we are invoked with $1=process
# and $2=sdmname.

set -e

if [ -z "$1" -o "$1" = help ] ; then
    echo "You must supply a subcommand. Subcommands are:
bash        -- Run a bash shell
cleanup <sdmname> -- run cleanup process and start jupyter session for visualization
"
    exit 1
fi

command="$1"
shift 

mv /rtpipe_cbe.conf /work

if [ "$command" = bash ] ; then
    exec bash "$@"
else
    cd /work
    if [ "$command" = cleanup ] ; then
	exec jupyter notebook --notebook-dir=/work --no-browser --ip=0.0.0.0
    else
	exec /control.py "$command" "$@"
    fi
fi


