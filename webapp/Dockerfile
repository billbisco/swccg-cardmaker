# SWCCG Card Maker render service. Build from the swccg-cardmaker checkout root:
#   docker build -f webapp/Dockerfile -t swccg-cardmaker .
FROM mcr.microsoft.com/playwright/python:v1.56.0-noble
WORKDIR /app
RUN pip install --no-cache-dir pillow==12.3.0 numpy==2.5.3 playwright==1.56.0
COPY render.py build_vs.py ./
COPY assets ./assets
COPY gempdata/Light.json gempdata/Dark.json gempdata/sets.json ./gempdata/
COPY webapp ./webapp
RUN mkdir -p /app/out /data && useradd -m -u 10010 cm && chown -R cm /app/out /data
USER cm
ENV CARDMAKER_DATA=/data HOLOTABLE=/holotable/Images-HT/starwars
EXPOSE 8790
CMD ["python3", "webapp/server.py", "--port", "8790"]
