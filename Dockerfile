FROM rclone/rclone:latest
WORKDIR /
ADD https://github.com/itsToggle/plex_debrid/archive/refs/heads/main.zip /
ADD . / ./
ADD https://raw.githubusercontent.com/debridmediamanager/zurg-testing/main/config.yml /zurg/
ENV \
  XDG_CONFIG_HOME=/config \
  TERM=xterm

RUN \
  apk add --update --no-cache gcompat libstdc++ libxml2-utils curl tzdata nano ca-certificates wget fuse3 python3 build-base py3-pip python3-dev linux-headers && \
  ln -sf python3 /usr/bin/python && \
  unzip main.zip && \
  rm main.zip && \
  mv plex_debrid-main/ plex_debrid && \
  python3 -m venv /venv && \
  source /venv/bin/activate && \
  pip3 install --upgrade pip && \
  pip3 install -r /plex_debrid/requirements.txt && \
  pip3 install -r /requirements.txt

HEALTHCHECK --interval=60s --timeout=10s \
  CMD ["/bin/sh", "-c", "source /venv/bin/activate && python /healthcheck.py"]
ENTRYPOINT ["/bin/sh", "-c", "source /venv/bin/activate && python /main.py"]