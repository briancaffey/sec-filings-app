# build stage
FROM node:14 as build-stage
# ARG FULL_DOMAIN_NAME
# ENV FULL_DOMAIN_NAME=$FULL_DOMAIN_NAME
WORKDIR /app/
COPY quasar/package.json /app/
RUN npm cache verify
RUN npm rebuild node-sass
RUN npm install -g @quasar/cli
RUN npm install --progress=false
COPY quasar /app/
RUN quasar build -m pwa

# ci stage
FROM nginx:1.13.12-alpine as production
COPY nginx/prod/prod.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist/pwa /dist/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
