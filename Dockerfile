# app/Dockerfile
FROM python:3.10-bookworm
WORKDIR /app

# Install system dependencies for chemistry rendering (RDKit/Ketcher support)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgirepository-1.0-1 \
    libfreetype6 \
    fonts-dejavu-core \
&& rm -rf /var/lib/apt/lists/*

# Copy your local directory (including /data and /models) into the container
COPY ./ ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt 

# Expose the Streamlit port
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# CRITICAL CHANGE: Update the filename from PolytoxiQ.py to PolyBiodeg.py
ENTRYPOINT ["streamlit", "run", "PolyBiodeg.py", "--server.port=8501", "--server.address=0.0.0.0"]