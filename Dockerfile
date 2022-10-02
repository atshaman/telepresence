FROM python:3.10-slim-buster
WORKDIR /app
COPY main.py .
COPY requirenments.txt .
RUN pip install --no-cache-dir -r requirenments.txt
RUN useradd svc && chown -R svc /app
USER svc
CMD ["python", "/app/main.py"]