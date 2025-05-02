from flask import Flask, request, jsonify
import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import pickle
import mysql.connector

app = Flask(__name__)

# Biến toàn cục để lưu trữ kết quả tìm kiếm tạm thời
search_results = {
    'top_indices': [],
    'similarities': [],
    'class_paths': [],
    'class_sources': [],
    'class_features': [],
    'predicted_label': None,
    'data': None
}

# ----- Kết nối CSDL -----
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

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
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 11)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.to(DEVICE)
model.eval()

# ----- Load class names từ bảng categories -----
def load_class_names():
    conn = get_db_connection()
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
    conn = get_db_connection()
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

# ----- Hàm lấy sản phẩm từ top_indices -----
def get_products_from_indices(top_indices, class_paths, class_sources, similarities, data, start_idx, num_items):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        products = []
        for idx in top_indices[start_idx:start_idx + num_items]:
            image_path = class_paths[idx]
            source = class_sources[idx]

            try:
                if source == 'products':
                    query = """
                        SELECT p.*, c.name as category_name
                        FROM products p
                        JOIN categories c ON p.category_id = c.id
                        WHERE p.image_path = %s
                    """
                    cursor.execute(query, (image_path,))
                else:  # source == 'product_images'
                    query = """
                        SELECT p.*, pi.image_path as pi_image_path, c.name as category_name
                        FROM products p
                        JOIN product_images pi ON pi.product_id = p.product_id
                        JOIN categories c ON p.category_id = c.id
                        WHERE pi.image_path = %s
                    """
                    cursor.execute(query, (image_path,))

                product = cursor.fetchone()
                if product:
                    product['similarity'] = float(similarities[idx])
                    product['image_source'] = source
                    if source == 'product_images':
                        product['image_path'] = product['pi_image_path']
                        del product['pi_image_path']
                    products.append(product)

                print(f"Product: Image Path: {image_path} (Similarity: {similarities[idx]:.4f}, Source: {source})")

            except Exception as e:
                print(f"Error querying product for image_path {image_path}: {str(e)}")
                continue

        conn.close()
        return products
    except Exception as e:
        return jsonify({'error': f'Failed to fetch products: {str(e)}'}), 500

# ----- API tìm kiếm ban đầu -----
@app.route('/api/similar-images', methods=['POST'])
def get_similar_images():
    global search_results
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        temp_path = os.path.join(IMAGE_DATA, 'temp_query.jpg')
        image_file.save(temp_path)

        if not os.path.exists(temp_path):
            return jsonify({'error': 'Failed to save temporary image file'}), 500

        try:
            query_feature, pred_class = extract_features(temp_path)
            query_feature = query_feature.reshape(1, -1)
        except Exception as e:
            os.remove(temp_path)
            return jsonify({'error': f'Failed to extract features from image: {str(e)}'}), 500

        if pred_class < 0 or pred_class >= len(class_names):
            os.remove(temp_path)
            return jsonify({'error': f'Invalid predicted class index: {pred_class}'}), 500

        predicted_label = class_names[pred_class]

        print(f"📌 Ảnh truy vấn: {temp_path}")
        print(f"📋 Dự đoán phân lớp: {predicted_label}")

        try:
            data = load_or_generate_features()
        except Exception as e:
            os.remove(temp_path)
            return jsonify({'error': f'Failed to load or generate features: {str(e)}'}), 500

        if 'labels' not in data:
            os.remove(temp_path)
            return jsonify({'error': 'Invalid cache data: missing labels'}), 500

        class_indices = [i for i, label in enumerate(data['labels']) if label == predicted_label]
        print(data['labels'])
        print(class_indices)
        if not class_indices:
            os.remove(temp_path)
            return jsonify({'error': f"No images found in category '{predicted_label}'"}), 404

        required_keys = ['features', 'paths', 'sources']
        for key in required_keys:
            if key not in data:
                os.remove(temp_path)
                return jsonify({'error': f'Invalid cache data: missing {key}'}), 500

        class_features = np.array([data['features'][i] for i in class_indices])
        class_paths = [data['paths'][i] for i in class_indices]
        class_sources = [data['sources'][i] for i in class_indices]

        similarities = cosine_similarity(query_feature, class_features)[0]
        top_indices = similarities.argsort()[::-1]

        # Lưu kết quả tìm kiếm vào biến toàn cục
        search_results = {
            'top_indices': top_indices.tolist(),  # Chuyển NumPy array thành list để tránh lỗi
            'similarities': similarities.tolist(),  # Chuyển NumPy array thành list
            'class_paths': class_paths,
            'class_sources': class_sources,
            'class_features': class_features.tolist(),  # Chuyển NumPy array thành list
            'predicted_label': predicted_label,
            'data': data
        }

        # Lấy 5 sản phẩm đầu tiên
        similar_products = get_products_from_indices(
            top_indices, class_paths, class_sources, similarities, data, start_idx=0, num_items=5
        )

        os.remove(temp_path)

        return jsonify({
            'predicted_category': predicted_label,
            'similar_products': similar_products,
            'total_results': len(top_indices)
        })

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

# ----- API load more để lấy thêm 5 sản phẩm -----
@app.route('/api/load-more-similar', methods=['POST'])
def load_more_similar():
    global search_results
    try:
        # Lấy dữ liệu từ body
        body = request.get_json()
        if not body:
            return jsonify({'error': 'Request body must be JSON'}), 400

        # Lấy offset từ body (mặc định là 5 nếu không có)
        offset = body.get('offset', 5)
        if not isinstance(offset, int) or offset < 0:
            return jsonify({'error': 'Offset must be a non-negative integer'}), 400

        num_items = 5

        # Kiểm tra xem có kết quả tìm kiếm trước đó không
        # Sử dụng len() thay vì kiểm tra trực tiếp giá trị logic của mảng
        if len(search_results['top_indices']) == 0:
            return jsonify({'error': 'No previous search results found. Please run a search first.'}), 400

        top_indices = search_results['top_indices']
        similarities = search_results['similarities']
        class_paths = search_results['class_paths']
        class_sources = search_results['class_sources']
        data = search_results['data']

        # Kiểm tra xem còn sản phẩm để load không
        if offset >= len(top_indices):
            return jsonify({'error': 'No more products to load'}), 404

        # Lấy 5 sản phẩm tiếp theo
        similar_products = get_products_from_indices(
            top_indices, class_paths, class_sources, similarities, data, start_idx=offset, num_items=num_items
        )

        return jsonify({
            'similar_products': similar_products,
            'next_offset': offset + num_items if offset + num_items < len(top_indices) else None,
            'total_results': len(top_indices)
        })

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

# ----- Thực thi -----
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)