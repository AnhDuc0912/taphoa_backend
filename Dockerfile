# Sử dụng base image Python nhẹ và phù hợp cho PyTorch
FROM python:3.9-slim

# Tạo thư mục làm việc
WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy toàn bộ thư mục mã nguồn vào container
COPY . /app

# Copy requirements và cài thư viện Python
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mở cổng Flask
EXPOSE 5000

# Chạy Flask app
CMD ["python", "api.py"]