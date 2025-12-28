FROM python:3.13.9-slim-bookworm

ENV PYTHONWRITEBUTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    nodejs \
    npm

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 8000

CMD ["./entrypoint.sh"]
