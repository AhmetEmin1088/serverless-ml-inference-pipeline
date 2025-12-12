import json, os, boto3, onnxruntime as rt
import numpy as np
from PIL import Image
from io import BytesIO
import torchvision.transforms as transforms

s3 = boto3.client('s3')
MODEL_LOCAL_PATH = "/tmp/resnet18.onnx"

def download_model(bucket, key):
    if not os.path.exists(MODEL_LOCAL_PATH):
        s3.download_file(bucket, key, MODEL_LOCAL_PATH)

def preprocess_image_bytes(image_bytes):
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    x = transform(img).unsqueeze(0).numpy().astype(np.float32)
    return x

def lambda_handler(event, context):
    # expect base64 image in JSON body: {"image_b64":"..."} OR S3 reference
    bucket = "machine-minds-models-2025"
    key = "resnet18.onnx"
    download_model(bucket, key)
    sess = rt.InferenceSession(MODEL_LOCAL_PATH)
    input_name = sess.get_inputs()[0].name

    # example: event["body"] contains {"image_b64": "..."}
    body = event.get("body")
    if body:
        try:
            data = json.loads(body)
        except:
            data = body
    else:
        data = event

    # Implementing simple path: if image_b64 present:
    if "image_b64" in data:
        import base64
        img_b = base64.b64decode(data["image_b64"])
        x = preprocess_image_bytes(img_b)
        out = sess.run(None, {input_name: x})
        pred = int(np.argmax(out[0], axis=1)[0])
        return {"statusCode":200, "body": json.dumps({"pred_index": pred})}
    else:
        return {"statusCode":400, "body":"No image provided"}
