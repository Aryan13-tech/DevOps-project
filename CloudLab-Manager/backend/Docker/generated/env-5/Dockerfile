FROM python:3.10-slim
CMD RUN pip install flask
RUN printf "from flask import Flask\napp = Flask(__name__)\n@app.route('/')\ndef home(): return 'Hello from Python Container!'\napp.run(host='0.0.0.0', port=8080)" > app.py
CMD ["python3", "app.py"]