FROM caseyjlaw/rtpipe-base
MAINTAINER Casey Law <caseyjlaw@gmail.com>

WORKDIR /work
EXPOSE 8888

# do this first to improve build time
COPY setup.sh /
RUN ["/bin/bash", "/setup.sh"]

COPY base.ipynb control.py entrypoint.sh rtpipe_c4xlarge.conf rtpipe_c42xlarge.conf /
RUN chmod +x /entrypoint.sh
RUN chmod +x /control.py

ENV agdir /alnotebook
ENTRYPOINT ["/entrypoint.sh"]

