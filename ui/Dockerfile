FROM node:16

WORKDIR /ui

COPY package*.json ./
RUN npm install 

COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]