FROM node:8.12-alpine

RUN apk add --update --no-cache build-base nginx git

RUN mkdir /app && mkdir /app/data

WORKDIR /app

COPY . .

RUN npm install
ENV NODE_ENV production
RUN npm run build:dll
RUN npm run build
