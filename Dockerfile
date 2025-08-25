FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080

# Run with gunicorn in containers (prod-friendly)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app", "--timeout", "90"]
