FROM nginx:1.13.12-alpine
COPY dev/dev.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]