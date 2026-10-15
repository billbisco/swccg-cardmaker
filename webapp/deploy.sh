#!/bin/bash
# Deploy the card maker on the swccg.com VPS (run as root from the unpacked bundle directory).
#   static UI  -> /var/www/swccg.com/cardmaker/
#   remaster art -> /opt/swccg-cardmaker-src/src (the OVS transcriptions' slips/scans, not in git: copyright + size)
#   service    -> docker container swccg_cardmaker on 127.0.0.1:17010, nginx proxies /cardmaker/api/
set -euo pipefail
cd "$(dirname "$0")"
B=$(pwd)
docker build -q -f webapp/Dockerfile -t swccg-cardmaker:latest . >/dev/null
docker rm -f swccg_cardmaker >/dev/null 2>&1 || true
mkdir -p /opt/swccg-cardmaker-data && chown 10010:10010 /opt/swccg-cardmaker-data
docker run -d --name swccg_cardmaker --restart unless-stopped --memory 1500m --cpus 2 --shm-size 256m \
  -p 127.0.0.1:17010:8790 -v /opt/swccg-cardmaker-data:/data -v /opt/swccg-holotable:/holotable:ro -v /opt/swccg-cardmaker-src/src:/app/src:ro swccg-cardmaker:latest >/dev/null
mkdir -p /var/www/swccg.com/cardmaker && cp -r webapp/static/. /var/www/swccg.com/cardmaker/
echo "deployed $(date -u +%FT%TZ)"
