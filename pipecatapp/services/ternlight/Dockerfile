FROM node:18-slim

WORKDIR /app

COPY package.json .
RUN npm install

COPY ternlight_server.js .

ENV PORT=8000
EXPOSE 8000

CMD ["node", "ternlight_server.js"]
