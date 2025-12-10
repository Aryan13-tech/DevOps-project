FROM nginx:latest

# Remove default NGINX config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom reverse proxy config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy ONLY index.html, not everything
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
