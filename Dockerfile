# FROM python:3.10-slim-bullseye

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     cmake \
#     libopenblas-dev \
#     liblapack-dev \
#     libx11-dev \
#     libgtk-3-dev \
#     libboost-python-dev \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache-dir dlib==19.24.1 face-recognition fastapi uvicorn python-multipart

# WORKDIR /app
# COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]


FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir dlib==19.24.1

RUN pip install --no-cache-dir face-recognition fastapi uvicorn python-multipart numpy<2.0.0

COPY . .

EXPOSE 10000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]