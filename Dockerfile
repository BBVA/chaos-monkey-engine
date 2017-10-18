FROM python:3.6
MAINTAINER BBVALabs

RUN mkdir -p /opt/chaosmonkey
RUN python3 -m  venv /opt/chaosmonkey/venv

ENV REFRESHED_AT 2016-02-15T11:00
COPY . /opt/chaosmonkey/src
RUN /opt/chaosmonkey/venv/bin/pip install /opt/chaosmonkey/src

ENTRYPOINT ["/opt/chaosmonkey/venv/bin/chaos-monkey-engine"]
CMD ["-d", "/opt/chaosmonkey/src/storage/cme.sqlite", "-a", "/opt/chaosmonkey/src/attacks", "-p", "/opt/chaosmonkey/src/planners"]

