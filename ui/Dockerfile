FROM node:16 as builder
WORKDIR /ui
COPY package*.json ./
RUN npm clean-install
COPY . .
ENV NODE_ENV=production
RUN npm run build
CMD ["npm", "run", "serve"]

FROM caddy:2-alpine
COPY --from=builder /ui/dist /usr/share/caddy
EXPOSE 80