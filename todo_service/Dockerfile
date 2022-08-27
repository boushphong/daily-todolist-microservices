FROM python:3.10-slim

WORKDIR /app

RUN apt-get update -yqq && \
	apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
	curl

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000

CMD ["uvicorn", "todo:app", "--host", "0.0.0.0", "--port", "8000"]