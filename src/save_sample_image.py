import torchvision
import torchvision.transforms as transforms
from PIL import Image
import os

# CIFAR-10 dataset (test set)
transform = transforms.Compose([transforms.ToTensor()])
testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)

img, label = testset[0]
os.makedirs("data", exist_ok=True)
Image.fromarray((img.permute(1, 2, 0).numpy() * 255).astype("uint8")).save("./data/sample.png")

print("Saved one CIFAR-10 image to ./data/sample.png (label:", label, ")")
