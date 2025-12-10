# 🚀 CloudLab Manager – Environment Commands Example

This file contains ready-to-use commands for each supported Docker image.  
Copy them into the **Initial Commands** input box when creating an environment.

---
# 1).

### select Docker image :- ubantu:latest

### Port number :- 2020

copy and pest this command in to initial commands.
```sh
 apt update -y && apt install -y busybox && echo "Hello from Ubuntu Web Server!" > index.html && busybox httpd -f -p 2020
```

---
# 2).

### select Docker image :-node:18-alpine 

### Port number :- 1010

copy and pest this command in to initial commands.
```sh
apk add --no-cache nodejs npm && printf "const http=require('http');http.createServer((req,res)=>{res.end('Hello from Node.js Web Server!');}).listen(1010,'0.0.0.0');" > server.js && node server.js
```

---
# 3).

### select Docker image :- python:3.10-slim

### Port number :- 3030

copy and pest this command in to initial commands.
```sh
pip install flask && printf "from flask import Flask\napp=Flask(__name__)\n@app.route('/')\ndef home(): return 'Hello from Flask Container!'\napp.run(host='0.0.0.0', port=3030)" > app.py && python3 app.py

```



























  











