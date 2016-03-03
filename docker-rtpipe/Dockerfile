FROM caseyjlaw/rtpipe-base
MAINTAINER Casey Law <caseyjlaw@gmail.com>

WORKDIR /work
COPY setup.sh control.py entrypoint.sh /
COPY rtpipe_cbe.conf /work/
EXPOSE 8888

RUN ["/bin/bash", "/setup.sh"]
ENTRYPOINT ["/entrypoint.sh"]
CMD ["help"]

