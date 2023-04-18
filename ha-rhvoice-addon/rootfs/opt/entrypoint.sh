#!/usr/bin/with-contenv bashio
# shellcheck shell=bash

echo "Setting trap PID $$"
trap cleanup INT TERM

cleanup() {
  echo 'stopping...'
  APP="$(pgrep 'python' -a | grep 'app.py' | awk '{print $1}')"
  echo "$APP" | xargs kill -TERM
  wait
  echo "stop"
  exit 0
}

if [ -f /usr/local/etc/RHVoice/RHVoice.conf ] && [ ! -L /usr/local/etc/RHVoice/RHVoice.conf ]; then
  if [ ! -f /opt/cfg/RHVoice.conf ]; then
    mv /usr/local/etc/RHVoice/RHVoice.conf /opt/cfg/RHVoice.conf
  fi
  ln -fs /opt/cfg/RHVoice.conf /usr/local/etc/RHVoice/RHVoice.conf
fi

if [ -f /opt/app.py ]; then
  python3 -u /opt/app.py &
fi

wait
