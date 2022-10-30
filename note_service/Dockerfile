FROM python:3.10-slim

WORKDIR /app

RUN apt-get update --allow-unauthenticated -yqq && \
	  apt-get upgrade --allow-unauthenticated -yqq && \
    apt-get install --allow-unauthenticated -yqq --no-install-recommends \
	  curl \
    librdkafka-dev \
    gcc \
    libc-dev

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8001

CMD ["uvicorn", "note:app", "--host", "0.0.0.0", "--port", "8001"]