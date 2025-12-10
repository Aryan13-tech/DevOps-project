FROM python:3.10-slim
RUN pip install flask
RUN printf "from flask import Flask\napp = Flask(__name__)\n@app.route('/')\ndef home(): return 'Hello from Flask Container!'\napp.run(host='0.0.0.0', port=8080)" > app.py
CMD ["sh", "-c", "python app.py"]