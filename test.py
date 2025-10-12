import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
import matplotlib.pyplot as plt

# 1. Transformations (resize CIFAR10 images to ResNet input size)
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# 2. Load CIFAR-10 test dataset
testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=8, shuffle=False)

# 3. Load pretrained ResNet18 model + weights
weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights)
model.eval()

# 4. Get a batch of test images
images, labels = next(iter(testloader))

# 5. Run inference
with torch.no_grad():
    outputs = model(images)
_, preds = outputs.max(1)

# 6. Class lists
cifar_classes = testset.classes
imagenet_classes = weights.meta["categories"]

# 7. Show predictions
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
for i, ax in enumerate(axes.flat):
    # Convert tensor to displayable image
    img = images[i].permute(1, 2, 0).numpy()
    img = img * [0.229, 0.224, 0.225] + [0.485, 0.456, 0.406]
    img = img.clip(0, 1)
    
    ax.imshow(img)
    ax.axis('off')
    
    pred_label = imagenet_classes[preds[i]]
    true_label = cifar_classes[labels[i]]
    ax.set_title(f"Pred: {pred_label[:15]}...\nTrue: {true_label}", fontsize=8)

plt.tight_layout()
plt.show()
