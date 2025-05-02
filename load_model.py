import os
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Định nghĩa mô hình và feature extractor
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 11)
model.load_state_dict(torch.load('./best_model.pt', map_location=torch.device('cpu')))
model.eval()

feature_extractor = nn.Sequential(*list(model.children())[:-1])

# Chuyển đổi hình ảnh
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Dictionary nhãn
labels = {
    'banh_keo': 0, 'bia': 1, 'ca_phe': 2, 'dau_an': 3, 'gia_vi': 4, 'mi_goi': 5,
    'nuoc_mam': 6, 'nuoc_ngot': 7, 'nuoc_rua_chen': 8, 'nuoc_tuong': 9, 'sua': 10
}

def predict(image: Image.Image) -> str:
    """Dự đoán nhãn của hình ảnh."""
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(image)
        _, predicted_class = torch.max(output, 1)
        predicted_label = list(labels.keys())[predicted_class.item()]
    return predicted_label

def extract_features(image: Image.Image, model=feature_extractor) -> np.ndarray:
    """Trích xuất đặc trưng từ hình ảnh."""
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        features = model(image)
        features = features.squeeze().numpy()
    return features

def find_similar_images(image: Image.Image, dataset_dir: str, predicted_label: str, top_k: int = 5) -> list[dict]:
    """Tìm kiếm top k hình ảnh tương tự trong thư mục của lớp dự đoán."""
    input_features = extract_features(image)
    class_dir = os.path.join(dataset_dir, predicted_label)
    if not os.path.exists(class_dir):
        raise ValueError(f"Không tìm thấy thư mục cho lớp {predicted_label}")

    similar_images = []
    for img_name in os.listdir(class_dir):
        img_path = os.path.join(class_dir, img_name)
        try:
            img = Image.open(img_path)
            features = extract_features(img)
            similarity = cosine_similarity([input_features], [features])[0][0]
            similar_images.append({"path": img_path, "similarity": float(similarity)})
        except Exception as e:
            print(f"Lỗi khi xử lý {img_path}: {e}")

    similar_images = sorted(similar_images, key=lambda x: x["similarity"], reverse=True)
    return similar_images[:top_k]