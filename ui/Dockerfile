FROM node:16 as builder
RUN npm install -g serve
WORKDIR /ui
COPY package*.json ./
RUN npm clean-install
COPY . .
ENV NODE_ENV=production
RUN npm run build
EXPOSE 8080
CMD [ "serve", "-s", "dist", "-l", "8080" ]