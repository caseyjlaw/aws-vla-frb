FROM caseyjlaw/rtpipe-base
MAINTAINER Casey Law <caseyjlaw@gmail.com>

WORKDIR /work
COPY base.ipynb setup.sh control.py entrypoint.sh rtpipe_cbe.conf /
EXPOSE 8888

RUN ["/bin/bash", "/setup.sh"]
ENTRYPOINT ["/entrypoint.sh"]
CMD ["help"]

