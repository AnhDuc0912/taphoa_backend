from flask import Flask, request, jsonify
import os
import mysql.connector
from model_utils import extract_features, load_or_generate_features
from fine_tune import fine_tune_model_with_new_data
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests

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
DB_CONFIG = {
    'host': 'host.docker.internal',
    'user': 'root',
    'password': 'mysql',
    'database': 'taphoa_hango'
}

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

        from model_utils import class_names
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
            'top_indices': top_indices.tolist(),
            'similarities': similarities.tolist(),
            'class_paths': class_paths,
            'class_sources': class_sources,
            'class_features': class_features.tolist(),
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
        # Lấy offset từ query parameter thay vì body
        offset = request.args.get('offset', type=int, default=0)
        if offset is None or offset < 0:
            return jsonify({'error': 'Offset must be a non-negative integer'}), 400

        num_items = 5  # Mỗi lần gọi API sẽ lấy thêm 5 sản phẩm

        if len(search_results['top_indices']) == 0:
            return jsonify({'error': 'No previous search results found. Please run a search first.'}), 400

        top_indices = search_results['top_indices']
        similarities = search_results['similarities']
        class_paths = search_results['class_paths']
        class_sources = search_results['class_sources']
        data = search_results['data']

        if offset >= len(top_indices):
            return jsonify({'error': 'No more products to load'}), 404

        # Lấy 5 sản phẩm tiếp theo
        similar_products = get_products_from_indices(
            top_indices, class_paths, class_sources, similarities, data, start_idx=offset, num_items=num_items
        )

        # Tính offset tiếp theo
        next_offset = offset + num_items if offset + num_items < len(top_indices) else None

        return jsonify({
            'similar_products': similar_products,
            'next_offset': next_offset,
            'total_results': len(top_indices)
        })

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

# ----- API thêm sản phẩm mới -----
@app.route('/api/add-product', methods=['POST'])
def add_product():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Missing image file'}), 400

        image_file = request.files['image']
        if not image_file or image_file.filename == '':
            return jsonify({'error': 'No image file provided'}), 400

        # Lấy dữ liệu từ form
        category_id = request.form.get('category_id')
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        unit = request.form.get('unit')

        # Kiểm tra dữ liệu bắt buộc
        if not all([category_id, product_name, price, unit]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Gọi hàm upload_image để lưu ảnh
        label = 'uncategorized'  # default value nếu không có category_id

        if category_id:
            from model_utils import class_names
            label = class_names[int(category_id) - 1]

        image_path = f"{image_file.filename}_{int(torch.randint(0, 1000, (1,)).item())}.jpg"
        save_path = upload_image(label, image_file, image_path)  # Sử dụng hàm upload_image

        # Lưu vào CSDL
        conn = get_db_connection()
        cursor = conn.cursor()

        product_query = """
            INSERT INTO products (product_name, category_id, price, unit, image_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(product_query, (
            product_name,
            category_id,
            price,
            unit,
            image_path
        ))
        product_id = cursor.lastrowid

        conn.commit()
        conn.close()

        update_features_and_finetune(save_path, label, image_path, int(category_id))

        return jsonify({
            'message': 'Product added successfully',
            'product_id': product_id,
            'category_id': category_id,
            'image_path': label + "/" + image_path
        })

    except Exception as e:
        return jsonify({'error': f'Failed to add product: {str(e)}'}), 500

# API sửa sản phẩm
@app.route('/api/update-product', methods=['POST'])
def update_product():
    try:
        # Lấy product_id
        product_id = request.form.get('product_id', type=int)
        if not product_id:
            return jsonify({'error': 'Missing product_id'}), 400

        # Chỉ cho phép cập nhật các trường sau
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        unit = request.form.get('unit')

        # Kiểm tra có ít nhất một trường cần cập nhật
        if not any([product_name, price, unit]):
            return jsonify({'error': 'No valid fields to update (product_name, price, unit only)'}), 400

        # Kết nối DB
        conn = get_db_connection()
        cursor = conn.cursor()

        # Tạo truy vấn cập nhật động
        update_fields = []
        values = []

        if product_name:
            update_fields.append("product_name = %s")
            values.append(product_name)
        if price:
            update_fields.append("price = %s")
            values.append(price)
        if unit:
            update_fields.append("unit = %s")
            values.append(unit)

        values.append(product_id)

        update_query = f"""
            UPDATE products
            SET {', '.join(update_fields)}
            WHERE id = %s
        """

        cursor.execute(update_query, values)
        conn.commit()
        conn.close()

        return jsonify({'message': 'Product updated successfully'})

    except Exception as e:
        return jsonify({'error': f'Failed to update product: {str(e)}'}), 500

# API xóa sản phẩm
@app.route('/api/delete-product', methods=['POST'])
def delete_product():
    try:
        product_id = request.form.get('product_id', type=int)
        if not product_id:
            return jsonify({'error': 'Missing product_id'}), 400

        # Kết nối DB
        conn = get_db_connection()
        cursor = conn.cursor()

        # Kiểm tra sản phẩm tồn tại
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Xóa sản phẩm
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Product deleted successfully'})

    except Exception as e:
        return jsonify({'error': f'Failed to delete product: {str(e)}'}), 500

# Upload ảnh
@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Missing image file'}), 400

        image_file = request.files['image']
        category_id = request.form.get('category_id', default=None, type=int)

        if not image_file or image_file.filename == '':
            return jsonify({'error': 'No image file provided'}), 400

        # Xác định nhãn nếu có
        label = 'uncategorized'
        if category_id is not None:
            from model_utils import class_names
            label = class_names[category_id]

        image_path = f"{image_file.filename}_{int(torch.randint(0, 1000, (1,)).item())}.jpg"
        save_path = os.path.join(IMAGE_DATA, label, image_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        image_file.save(save_path)

        return jsonify({
            'message': 'Image uploaded successfully',
            'image_path': image_path,
            'category_label': label
        })

    except Exception as e:
        return jsonify({'error': f'Failed to upload image: {str(e)}'}), 500

def upload_image(label, image_file, image_path):
    try:
        # Xác định đường dẫn lưu ảnh
        save_dir = os.path.join(IMAGE_DATA, label)
        os.makedirs(save_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

        # Đường dẫn tệp lưu ảnh
        save_path = os.path.join(save_dir, image_path)
        
        # Lưu ảnh vào hệ thống
        image_file.save(save_path)

        return save_path  # Trả về đường dẫn đã lưu ảnh

    except Exception as e:
        return jsonify({'error': f'Failed to upload image: {str(e)}'}), 500

# ----- Hàm cập nhật đặc trưng và fine-tune mô hình sau khi thêm sản phẩm -----
def update_features_and_finetune(image_path, label, image_path_in_db, category_id):
    from model_utils import FEATURES_CACHE
    import pickle

    new_feature, _ = extract_features(image_path)
    data = load_or_generate_features()

    data['features'] = np.vstack([data['features'], new_feature])
    data['paths'].append(image_path_in_db)
    data['labels'].append(label)
    data['sources'].append('products')

    with open(FEATURES_CACHE, 'wb') as f:
        pickle.dump(data, f)
    print("💾 Đã cập nhật đặc trưng vào file cache.")

    fine_tune_model_with_new_data([image_path], [category_id])

# get products
@app.route('/api/get-products', methods=['GET'])
def get_products():
    try:
        # Lấy offset từ query parameter, mặc định là 0
        offset = int(request.args.get('offset', 0))
        limit = 5  # Số lượng sản phẩm mỗi lần load

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT *, c.name as category_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            ORDER BY product_id DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, offset))
        products = cursor.fetchall()

        conn.close()

        return jsonify({'products': products})

    except Exception as e:
        return jsonify({'error': f'Failed to retrieve products: {str(e)}'}), 500
    
# API lấy danh sách danh mục
@app.route('/api/get-categories', methods=['GET'])
def get_category():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT *
            FROM categories
        """
        cursor.execute(query)
        categories = cursor.fetchall()

        conn.close()

        return jsonify({'categories': categories})

    except Exception as e:
        return jsonify({'error': f'Failed to retrieve products: {str(e)}'}), 500 
# ----- Thực thi -----
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)