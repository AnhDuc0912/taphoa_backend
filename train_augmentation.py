import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms
from torchvision.datasets import ImageFolder
from sklearn.model_selection import train_test_split
from PIL import Image
import numpy as np

# Thiết lập thiết bị (CPU/GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Định nghĩa các biến số
DATASET_DIR = './static'
MODEL_PATH = './best_model.pt'
NEW_MODEL_PATH = './best_model_updated.pt'
NUM_CLASSES = 11
BATCH_SIZE = 32
NUM_EPOCHS = 10
LEARNING_RATE = 0.001

# Dictionary nhãn
labels = {
    'banh_keo': 0, 'bia': 1, 'ca_phe': 2, 'dau_an': 3, 'gia_vi': 4, 'mi_goi': 5,
    'nuoc_mam': 6, 'nuoc_ngot': 7, 'nuoc_rua_chen': 8, 'nuoc_tuong': 9, 'sua': 10
}

# Tăng cường dữ liệu cho tập huấn luyện
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),  # Cắt ngẫu nhiên và thay đổi kích thước
    transforms.RandomHorizontalFlip(),  # Lật ngang ngẫu nhiên
    transforms.RandomRotation(30),      # Xoay ngẫu nhiên ±30 độ
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),  # Thay đổi độ sáng, tương phản, bão hòa
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Biến đổi cho tập kiểm tra (không tăng cường)
test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Tải dữ liệu từ thư mục
def load_dataset(dataset_dir):
    dataset = ImageFolder(root=dataset_dir, transform=None)  # Tạm thời không áp dụng transform
    return dataset

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
def split_dataset(dataset, test_size=0.2):
    train_idx, test_idx = train_test_split(
        list(range(len(dataset))), test_size=test_size, stratify=dataset.targets, random_state=42
    )
    
    # Dataset tùy chỉnh để áp dụng transform khác nhau
    class CustomDataset(Dataset):
        def __init__(self, dataset, indices, transform=None):
            self.dataset = dataset
            self.indices = indices
            self.transform = transform
        
        def __len__(self):
            return len(self.indices)
        
        def __getitem__(self, idx):
            img, label = self.dataset[self.indices[idx]]
            if self.transform:
                img = self.transform(img)
            return img, label
    
    train_dataset = CustomDataset(dataset, train_idx, transform=train_transform)
    test_dataset = CustomDataset(dataset, test_idx, transform=test_transform)
    
    return train_dataset, test_dataset

# Khởi tạo mô hình
def initialize_model(num_classes, model_path):
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    return model

# Huấn luyện mô hình
def train_model(model, train_loader, test_loader, num_epochs, learning_rate):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    best_acc = 0.0
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        train_acc = 100 * correct / total
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}, Train Acc: {train_acc:.2f}%')
        
        # Đánh giá trên tập kiểm tra
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        test_acc = 100 * correct / total
        print(f'Test Acc: {test_acc:.2f}%')
        
        # Lưu mô hình nếu đạt độ chính xác tốt nhất
        if test_acc > best_acc:
            best_acc = test_acc
            torch.save(model.state_dict(), NEW_MODEL_PATH)
            print(f'Mô hình đã được lưu tại: {NEW_MODEL_PATH}')

# Hàm chính để chạy huấn luyện
def main():
    # Tải dữ liệu
    dataset = load_dataset(DATASET_DIR)
    train_dataset, test_dataset = split_dataset(dataset)
    
    # Tạo DataLoader
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # Khởi tạo mô hình
    model = initialize_model(NUM_CLASSES, MODEL_PATH)
    
    # Huấn luyện mô hình
    train_model(model, train_loader, test_loader, NUM_EPOCHS, LEARNING_RATE)

if __name__ == "__main__":
    main()