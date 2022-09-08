FROM node:16

WORKDIR /ui
RUN rm -rf node_modules
RUN rm -f package-lock.json
COPY package*.json ./
RUN npm cache clean --force
RUN npm install 
RUN npm install -g @vue/cli-service
RUN npm install -g @vue/cli

COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]