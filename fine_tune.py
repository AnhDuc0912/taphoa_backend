import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import os

# ----- Cấu hình -----
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MODEL_PATH = './best_model_updated.pt'
TRANSFORM = transforms.Compose([
    transforms.RandomResizedCrop(224, scale=(0.8, 1.2), ratio=(0.9, 1.1)),  # Cắt và zoom
    transforms.RandomHorizontalFlip(p=0.5),  # Lật ngang
    transforms.RandomRotation(degrees=15),   # Xoay nhẹ
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.05),  # Biến đổi màu
    transforms.RandomGrayscale(p=0.1),        # Đôi khi chuyển sang grayscale
    transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 2.0)),  # Làm mờ nhẹ
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ----- Tải mô hình -----
def load_model():
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 11)  # Số lớp mặc định, có thể điều chỉnh
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    return model

# ----- Dataset tùy chỉnh cho dữ liệu mới -----
class CustomDataset(Dataset):
    def __init__(self, image_paths, labels, transform):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, self.labels[idx]

# ----- Hàm fine-tune mô hình với dữ liệu mới -----
def fine_tune_model_with_new_data(new_image_paths, new_labels):
    global model
    model = load_model()
    model.train()

    # Tạo dataset và dataloader
    dataset = CustomDataset(new_image_paths, new_labels, TRANSFORM)
    loader = DataLoader(dataset, batch_size=1, shuffle=True)

    # Thiết lập optimizer và loss
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-4)

    # Fine-tune với 5 epoch
    for epoch in range(5):
        running_loss = 0.0
        for images, labels in loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch {epoch+1}/5, Loss: {running_loss/len(loader):.4f}")

    # Lưu mô hình đã fine-tuned
    model.eval()
    torch.save(model.state_dict(), MODEL_PATH)
    print("💾 Mô hình đã được fine-tuned và lưu lại.")

    return model