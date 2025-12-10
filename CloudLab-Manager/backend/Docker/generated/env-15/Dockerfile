FROM ubuntu:latest
CMD ["sh", "-c", "apt update -y && apt install -y busybox && echo \"Hello message from Ubuntu successfully.\" > index.html && busybox httpd -f -p 8080 -h /"]