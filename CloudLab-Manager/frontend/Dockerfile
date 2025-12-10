FROM nginx:latest

# Remove default NGINX config
RUN rm /etc/nginx/conf.d/default.conf

# Add your custom NGINX config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy your frontend HTML file
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
