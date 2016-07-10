#! /bin/bash
#
# This is the "entrypoint" script for the rtpipe aws project
# It assumes docker run will mount empty disk to /work

set -e

command="$1"
shift 

mv /rtpipe*conf /work  # move stuff into newly mounted disk
exec /control.py "$command" "$@"



