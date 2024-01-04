ARG BUILD_FROM
FROM $BUILD_FROM
LABEL org.opencontainers.image.source=https://github.com/definitio/ha-rhvoice-addon

ARG BUILD_ARCH
ARG RUNTIME_PACKAGES="lame python3 locales opus-tools flac python3-setuptools"
ARG BUILD_PACKAGES="git python3-pip python3-wheel wget ca-certificates"

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update -y \
  && apt-get -y install --no-install-recommends $RUNTIME_PACKAGES \
  && apt-mark manual $(apt-mark showauto) \
  && apt-get -y install --no-install-recommends $BUILD_PACKAGES \
  && cd /usr/share/locale/ && ls | grep -v 'ru\|en\|locale.alias' | xargs rm -rf \
  && locale-gen ru_RU.UTF-8 \
  && pip3 install -r /tmp/requirements.txt \
  && wget -q https://raw.githubusercontent.com/Aculeasis/ff/main/rhv_bin.py -O rhv_bin.py \
  && pip3 install $(python3 rhv_bin.py 0 0 data) \
  && pip3 install $(python3 rhv_bin.py linux $BUILD_ARCH) \
  && git clone https://github.com/vantu5z/RHVoice-dictionary.git /opt/RHVoice-dictionary \
  && mkdir -p /usr/local/etc/RHVoice/ \
  && cp -R /opt/RHVoice-dictionary/dicts /usr/local/etc/RHVoice/dicts \
  && cp -R /opt/RHVoice-dictionary/tools/preprocessing /opt/rhvoice_tools \
  && cd /opt && mkdir /opt/cfg \
  && apt-get remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) \
  && apt-get autoremove -y \
  && apt-get -y install --no-install-recommends $RUNTIME_PACKAGES \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp /usr/share/doc/* /usr/share/info/* \
    /usr/lib/python*/test /root/.cache/* /opt/RHVoice-dictionary

ENV LC_ALL ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8

COPY rootfs /

ENTRYPOINT ["/bin/bash", "/opt/entrypoint.sh"]
