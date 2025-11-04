import os
import json
import base64
import time
import numpy as np
from io import BytesIO
from PIL import Image
import onnxruntime as rt
import torchvision.transforms as transforms

LOCAL_TEST = os.environ.get("LOCAL_TEST", "True") == "True"
S3_BUCKET = os.environ.get("MODEL_BUCKET", "machine-minds-models-2025")
S3_KEY = os.environ.get("MODEL_KEY", "resnet18.onnx")

# Toggle for local testing vs AWS Lambda
LOCAL_TEST = True

# Model paths and S3 info
if LOCAL_TEST:
    MODEL_PATH = "./resnet18.onnx"  # local model path
else:
    MODEL_PATH = "/tmp/resnet18.onnx"

S3_BUCKET = "machine-minds-models-2025"
S3_KEY = "resnet18.onnx"


def download_model_to_tmp(s3_client):
    """Download the model from S3 to /tmp only if not in local mode."""
    if LOCAL_TEST:
        print("[INFO] LOCAL_TEST enabled → skipping S3 download.")
        return
    if not os.path.exists(MODEL_PATH):
        print(f"[INFO] Downloading model from s3://{S3_BUCKET}/{S3_KEY} ...")
        s3_client.download_file(S3_BUCKET, S3_KEY, MODEL_PATH)
        print("[INFO] Model downloaded to /tmp successfully.")


def preprocess_image_bytes(image_bytes):
    """Convert raw image bytes into normalized tensor input."""
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    x = transform(img).unsqueeze(0).numpy().astype(np.float32)
    return x


def predict(session, x):
    """Run inference using ONNX Runtime and return class index."""
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: x})
    pred = int(np.argmax(outputs[0], axis=1)[0])
    return pred


def lambda_handler(event, context):
    """Main Lambda handler (works locally and in AWS Lambda)."""
    import boto3
    s3 = boto3.client('s3')

    t0 = time.time()
    try:
        download_model_to_tmp(s3)
        sess = rt.InferenceSession(MODEL_PATH)
    except Exception as e:
        return {"statusCode": 500,
                "body": json.dumps({"error": "model load failed", "detail": str(e)})}

    t_load = time.time()

    # Parse incoming event
    try:
        body = event.get("body")
        if isinstance(body, str):
            data = json.loads(body)
        elif body:
            data = body
        else:
            data = event
        img_b64 = data.get("image_b64")
        if not img_b64:
            return {"statusCode": 400,
                    "body": json.dumps({"error": "no image provided"})}

        image_bytes = base64.b64decode(img_b64)
        x = preprocess_image_bytes(image_bytes)
        t_pre = time.time()

        pred = predict(sess, x)
        t_pred = time.time()

        print(f"[TIMING] Load: {t_load - t0:.2f}s | Preproc: {t_pre - t_load:.2f}s | Infer: {t_pred - t_pre:.2f}s")
        return {"statusCode": 200,
                "body": json.dumps({
                    "pred_index": pred,
                    "timings": {
                        "model_load_s": round(t_load - t0, 3),
                        "preprocess_s": round(t_pre - t_load, 3),
                        "inference_s": round(t_pred - t_pre, 3)
                    }
                })}
    except Exception as e:
        return {"statusCode": 500,
                "body": json.dumps({"error": "inference failed", "detail": str(e)})}
