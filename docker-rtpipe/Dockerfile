FROM caseyjlaw/rtpipe-base
MAINTAINER Casey Law <caseyjlaw@gmail.com>

WORKDIR /work
EXPOSE 8888

# do this first to improve build time
COPY setup.sh /
RUN ["/bin/bash", "/setup.sh"]

COPY base.ipynb control.py entrypoint.sh rtpipe_cbe.conf /
RUN chmod +x /entrypoint.sh
RUN chmod +x /control.py

ENTRYPOINT ["/entrypoint.sh"]

