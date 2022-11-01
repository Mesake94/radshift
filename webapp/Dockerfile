FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y
RUN apt-get upgrade -y
# RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install libpangocairo-1.0-0 -y
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /app
COPY . /app
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh


ENTRYPOINT ["sh","entrypoint.sh"]