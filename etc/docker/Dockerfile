FROM python:3.9-slim AS build

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libopencv-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/
COPY etc/config/config.json /app/config/config.json


FROM python:3.9-slim

COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /app /app

WORKDIR /app

CMD ["python", "pubImage.py"]
