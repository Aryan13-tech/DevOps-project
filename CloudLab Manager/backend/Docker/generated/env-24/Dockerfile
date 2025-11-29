FROM ubuntu:latest
CMD ["sh", "-c", "apt update -y && apt install -y busybox && echo \"Hello from Ubuntu Web Server!\" > index.html && busybox httpd -f -p 8082"]