FROM python:3.13.9-slim-bookworm

ENV PYTHONWRITEBUTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["./entrypoint.sh"]
