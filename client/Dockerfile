FROM node:latest

COPY . /src
WORKDIR /src

RUN npm install --loglevel warn

EXPOSE 8080

CMD ["npm", "run", "prod"]
