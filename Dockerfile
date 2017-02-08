FROM python:3.5
RUN mkdir -p /opt/chaosmonkey
RUN pyvenv /opt/chaosmonkey/venv
ENV REFRESHED_AT 2016-02-08T13:00
COPY requirements.txt /opt/chaosmonkey/
RUN /opt/chaosmonkey/venv/bin/pip install -r /opt/chaosmonkey/requirements.txt
COPY . /opt/chaosmonkey/src
RUN /opt/chaosmonkey/venv/bin/pip install /opt/chaosmonkey/src

ENTRYPOINT ["/opt/chaosmonkey/venv/bin/cm"]
CMD ["-d", "/opt/chaosmonkey/src/storage/cme.sqlite", "-a", "/opt/chaosmonkey/src/attacks", "-p", "/opt/chaosmonkey/src/planners"]

