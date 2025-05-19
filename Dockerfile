# Sử dụng image Python chính thức
FROM python:3.10-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy toàn bộ nội dung hiện tại vào container
COPY . /app

# Cài đặt pip packages (nếu có file requirements)
# Nếu không có, bạn có thể bỏ qua dòng này
# RUN pip install -r requirements.txt
RUN pip install flask torch joblib

# Mở cổng 5000 (thường dùng cho Flask)
EXPOSE 5000

# Lệnh chạy app
CMD ["python", "api.py"]
