# Small, fast, boring.
FROM nginx:alpine

# Copy our static site to the default web root.
COPY index.html /usr/share/nginx/html/index.html

# NGINX listens on 80 by default.
EXPOSE 80
