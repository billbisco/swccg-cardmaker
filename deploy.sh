#!/bin/bash
# Deploy the card maker on the swccg.com VPS (run as root from the unpacked bundle directory).
#   static UI  -> /var/www/swccg.com/cardmaker/
#   remaster art -> /opt/swccg-cardmaker-src/src (the OVS transcriptions' slips/scans, not in git: copyright + size)
#   service    -> docker container swccg_cardmaker on 127.0.0.1:17010, nginx proxies /cardmaker/api/
set -euo pipefail
cd "$(dirname "$0")"
B=$(pwd)
# files copied with scp keep mode 600 and the container user (10010) cannot read them (rev 53 outage)
chmod -R a+rX assets webapp cards *.py 2>/dev/null || true
docker build -q -f webapp/Dockerfile -t swccg-cardmaker:latest . >/dev/null
docker rm -f swccg_cardmaker >/dev/null 2>&1 || true
mkdir -p /opt/swccg-cardmaker-data && chown 10010:10010 /opt/swccg-cardmaker-data
docker run -d --name swccg_cardmaker --restart unless-stopped --memory 1500m --cpus 2 --shm-size 256m \
  -p 127.0.0.1:17010:8790 -v /opt/swccg-cardmaker-data:/data -v /opt/swccg-holotable:/holotable:ro -v /opt/swccg-cardmaker-src/src:/app/src:ro swccg-cardmaker:latest >/dev/null
mkdir -p /var/www/swccg.com/cardmaker && cp -r webapp/static/. /var/www/swccg.com/cardmaker/
# drop the previous builds of this image (each deploy leaves a 4 GB dangling image; base layers are shared)
for i in $(docker images -f dangling=true -q); do
  [ "$(docker image inspect "$i" --format '{{json .Config.Cmd}}')" = '["python3","webapp/server.py","--port","8790"]' ] && docker rmi -f "$i" >/dev/null || true
done
echo "deployed $(date -u +%FT%TZ)"
