FROM node:lts-alpine3.19

WORKDIR /app
COPY . .

RUN npm install

EXPOSE 5173

ENTRYPOINT ["npm"]
CMD ["run", "dev"]