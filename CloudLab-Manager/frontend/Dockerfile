FROM nginx:latest

# remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# copy your custom nginx reverse proxy config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy ALL your frontend files (html + css + images)
COPY . /usr/share/nginx/html/

EXPOSE 80
