WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "shared/ui/st_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]