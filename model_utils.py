import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
from tqdm import tqdm
import pickle
import mysql.connector
from fine_tune import fine_tune_model_with_new_data

# ----- Cấu hình -----
IMAGE_DATA = './static'
MODEL_PATH = './best_model_updated.pt'
FEATURES_CACHE = './features.pkl'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql',
    'database': 'taphoa_hango'
}

# ----- Tiền xử lý ảnh -----
TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# ----- Load mô hình -----
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 11)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.to(DEVICE)
model.eval()

# ----- Load class names từ bảng categories -----
def load_class_names():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT label FROM categories ORDER BY id")
    class_names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return class_names

class_names = load_class_names()

# ----- Hàm trích xuất vector đặc trưng và dự đoán nhãn -----
def extract_features(image_path):
    image = Image.open(image_path).convert("RGB")
    image = TRANSFORM(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        feature_extractor = nn.Sequential(*list(model.children())[:-1])
        features = feature_extractor(image).flatten()
        output = model(image)
        pred_class = torch.argmax(output, dim=1).item()
    return features.cpu().numpy(), pred_class

# ----- Load hoặc tạo đặc trưng từ CSDL -----
def load_or_generate_features():
    if os.path.exists(FEATURES_CACHE):
        try:
            with open(FEATURES_CACHE, 'rb') as f:
                data = pickle.load(f)
                if not isinstance(data, dict) or 'sources' not in data:
                    print("⚠️ File cache không chứa 'sources', đang xóa và tạo lại...")
                    os.remove(FEATURES_CACHE)
                else:
                    print("✅ Đang nạp đặc trưng từ file cache...")
                    return data
        except Exception as e:
            print(f"⚠️ Lỗi khi đọc file cache: {e}, đang xóa và tạo lại...")
            os.remove(FEATURES_CACHE)

    print("📦 Trích xuất đặc trưng từ CSDL...")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    query_products = """
        SELECT p.image_path, p.product_id, c.label
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.image_path IS NOT NULL AND p.image_path != ''
    """
    cursor.execute(query_products)
    products_rows = cursor.fetchall()

    query_images = """
        SELECT pi.image_path, pi.product_id, c.label
        FROM product_images pi
        JOIN products p ON pi.product_id = p.product_id
        JOIN categories c ON p.category_id = c.id
    """
    cursor.execute(query_images)
    images_rows = cursor.fetchall()

    conn.close()

    features_list = []
    paths_list = []
    labels_list = []
    sources_list = []

    for row in tqdm(products_rows, desc="Đang xử lý hình ảnh từ products", unit=" ảnh"):
        print(row['label'])
        img_path = os.path.join(IMAGE_DATA, row['label'], row['image_path'])
        if not os.path.exists(img_path):
            print(f"⚠️ Không tìm thấy file: {img_path}")
            continue
        try:
            feat, _ = extract_features(img_path)
            features_list.append(feat)
            paths_list.append(row['image_path'])
            labels_list.append(row['label'])
            sources_list.append('products')
        except Exception as e:
            print(f"Lỗi với {img_path}: {e}")

    for row in tqdm(images_rows, desc="Đang xử lý hình ảnh từ product_images", unit=" ảnh"):
        print(row['label'])
        img_path = os.path.join(IMAGE_DATA, row['label'], row['image_path'])
        if not os.path.exists(img_path):
            print(f"⚠️ Không tìm thấy file: {img_path}")
            continue
        try:
            feat, _ = extract_features(img_path)
            features_list.append(feat)
            paths_list.append(row['image_path'])
            labels_list.append(row['label'])
            sources_list.append('product_images')
        except Exception as e:
            print(f"Lỗi với {img_path}: {e}")

    cache_data = {
        'features': np.array(features_list),
        'paths': paths_list,
        'labels': labels_list,
        'sources': sources_list
    }
    with open(FEATURES_CACHE, 'wb') as f:
        pickle.dump(cache_data, f)
    print("💾 Đã lưu đặc trưng vào file.")
    return cache_data

import os

