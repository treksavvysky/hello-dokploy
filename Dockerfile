# Small, fast, boring.
FROM nginx:alpine

# Optional: Healthcheck so Dokploy knows it's alive.
HEALTHCHECK --interval=10s --timeout=2s --retries=3 CMD wget -qO- http://127.0.0.1 || exit 1

# Copy our static site to the default web root.
COPY index.html /usr/share/nginx/html/index.html

# NGINX listens on 80 by default.
EXPOSE 80
