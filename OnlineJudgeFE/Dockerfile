FROM node:8.12-alpine

RUN apk add --update --no-cache build-base git

RUN mkdir /app && mkdir /app/data

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

RUN npm run build:dll
RUN npm run build
