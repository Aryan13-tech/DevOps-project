# Use Python
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose your backend port
EXPOSE 8000

# Start backend
CMD ["python", "app.py"]
