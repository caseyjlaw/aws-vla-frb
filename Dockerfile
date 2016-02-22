FROM caseyjlaw/rtpipe-base
MAINTAINER Casey Law <caseyjlaw@gmail.com>

WORKDIR /work
COPY setup.sh entrypoint.sh /
COPY search.py rtpipe_cbe.conf /work/
#COPY cleanup.py /
EXPOSE 8888

RUN ["/bin/bash", "/setup.sh"]
ENTRYPOINT ["/entrypoint.sh"]
CMD ["help"]
