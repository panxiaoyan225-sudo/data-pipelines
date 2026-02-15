FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# This runs your ranking script
CMD ["python", "ranking_script.py"]