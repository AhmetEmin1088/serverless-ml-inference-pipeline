import torch
from torchvision import models
dummy_input = torch.randn(1, 3, 224, 224)
model = models.resnet18(pretrained=True).eval()
torch.onnx.export(
    model,
    dummy_input,
    "resnet18.onnx",
    input_names=["input"],
    output_names=["output"],
    opset_version=12,
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)
print("resnet18.onnx exported.")
