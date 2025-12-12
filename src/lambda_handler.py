import os
import json
import base64
import time
import numpy as np
from io import BytesIO
from PIL import Image
import onnxruntime as rt

# MODEL IS HERE — INSIDE IMAGE
MODEL_PATH = "/var/task/resnet18.onnx"


def preprocess_image_bytes(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))

    arr = np.array(img).astype("float32") / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    arr = (arr - mean) / std
    arr = np.transpose(arr, (2, 0, 1))
    arr = np.expand_dims(arr, axis=0)
    return arr


def predict(session, x):
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: x})
    pred = int(np.argmax(outputs[0], axis=1)[0])
    return pred


def lambda_handler(event, context):
    t0 = time.time()

    # Load model
    try:
        sess = rt.InferenceSession(MODEL_PATH)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "model load failed", "detail": str(e)})
        }

    t_load = time.time()

    # Parse event
    try:
        body = event.get("body")
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

        img_b64 = data.get("image_b64")
        if not img_b64:
            return {"statusCode": 400, "body": json.dumps({"error": "no image provided"})}

        image_bytes = base64.b64decode(img_b64)
        x = preprocess_image_bytes(image_bytes)

        pred = predict(sess, x)

        return {
            "statusCode": 200,
            "body": json.dumps({"pred_index": pred})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "inference failed", "detail": str(e)})
        }
