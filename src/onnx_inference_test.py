import onnxruntime as rt
import numpy as np
from PIL import Image
import torchvision.transforms as transforms

sess = rt.InferenceSession("resnet18.onnx")
input_name = sess.get_inputs()[0].name

# örnek image (notebook'tan bir görüntü kaydedin ya da data içinden)
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

# load any image: ./data/some_image.png (örnek olarak CIFAR image'ı kullanabilirsiniz)
img = Image.open("./data/sample.png").convert("RGB")
x = transform(img).unsqueeze(0).numpy().astype(np.float32)

out = sess.run(None, {input_name: x})
pred = np.argmax(out[0], axis=1)
print("Pred index:", int(pred[0]))
