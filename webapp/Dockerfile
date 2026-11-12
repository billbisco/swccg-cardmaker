# SWCCG Card Maker render service. Build from the swccg-cardmaker checkout root:
#   docker build -f webapp/Dockerfile -t swccg-cardmaker .
FROM mcr.microsoft.com/playwright/python:v1.56.0-noble
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends fonts-dejavu-core && rm -rf /var/lib/apt/lists/*   # ▲▼ glyphs as the remasters were set
RUN pip install --no-cache-dir pillow==12.3.0 numpy==2.5.3 playwright==1.56.0
COPY render.py build_vs.py early_slip.py lang_ja.py ./
COPY assets ./assets
# rev 77: Japanese printings (lang_ja.py) set in Noto Sans JP (SIL OFL), registered with fontconfig so Chromium finds it by name
RUN mkdir -p /usr/local/share/fonts/noto-jp && cp /app/assets/fonts/NotoSansJP/*.ttf /usr/local/share/fonts/noto-jp/ && fc-cache -f >/dev/null
COPY gempdata/Light.json gempdata/Dark.json gempdata/sets.json gempdata/corrections.json gempdata/fill.json gempdata/LightLegacy.json gempdata/DarkLegacy.json gempdata/card_labels.json gempdata/ReflectionsGold.json gempdata/legacy_art.json gempdata/legacy_versions.json gempdata/legacy_typeset.json ./gempdata/
COPY cards ./cards
COPY webapp ./webapp
RUN mkdir -p /app/out /data && useradd -m -u 10010 cm && chown -R cm /app/out /data
USER cm
ENV CARDMAKER_DATA=/data HOLOTABLE=/holotable/Images-HT/starwars
EXPOSE 8790
CMD ["python3", "webapp/server.py", "--port", "8790"]
