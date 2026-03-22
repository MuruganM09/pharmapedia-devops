FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirement.txt .

RUN pip install --no-cache-dir torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]