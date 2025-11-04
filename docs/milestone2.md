# Milestone 2 — Progress Report

**Project:** Serverless Machine Learning Inference Pipeline  
**Course:** ECE 6210 – Machine Intelligence (Fall 2025)  
**Team:** Machine Minds  
**Members:** [Ahmet Emin Yilmaz], [Munashe C Kabuya], [Allen Tinashe Maraire]  
**Date:** November 5, 2025

## 1. Objective Recap

The **Serverless Machine Learning Inference Pipeline** project aims to deploy and serve deep learning models without maintaining dedicated servers. Using **AWS Lambda** and **Amazon S3**, the system enables scalable, on-demand inference through a fully serverless architecture.

While **Milestone 1** focused on establishing base infrastructure and verifying the model download from S3,
**Milestone 2** extends the project by implementing:

- Full inference execution using ONNX Runtime
- Local testing through Docker-based Lambda emulation
- Containerization and deployment via AWS Elastic Container Registry (ECR)

## 2. Progress Since Milestone 1

### Model Runtime Integration

- Integrated **ONNX Runtime** into the AWS Lambda handler for efficient inference execution.
- The `lambda_handler.py` function now:

  - Downloads the `resnet18.onnx` model from S3 if not already in `/tmp/`.
  - Loads it using **ONNX Runtime**.
  - Accepts a base64-encoded image as input, preprocesses it using `torchvision.transforms`, and returns the top predicted class index.

This ensures that the model can be dynamically loaded and executed within the Lambda environment without requiring a persistent server.

### Local Testing via Docker Lambda Runtime

To validate the function before cloud deployment, the Lambda container was tested locally using the AWS Lambda base image for Python 3.9:

```bash
docker run -p 9000:8080 serverless-resnet-infer-fixed
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @data/test_event.json
```

The output confirmed successful inference:

```json
{
  "statusCode": 200,
  "body": {
    "pred_index": 841,
    "timings": {
      "model_load_s": 1.312,
      "preprocess_s": 1.004,
      "inference_s": 0.137
    }
  }
}
```

This demonstrated that:

- The model loads correctly inside the Lambda container.
- Inference works seamlessly with real image data.
- Cold and warm run timings can be observed and measured locally.

### Containerization and AWS Deployment Readiness

A custom **Dockerfile** was created to package the Lambda runtime and dependencies:

```dockerfile
FROM public.ecr.aws/lambda/python:3.9
RUN pip install --no-cache-dir numpy==1.26.4 onnxruntime==1.16.3 pillow torch torchvision
COPY src/ ${LAMBDA_TASK_ROOT}/
CMD ["lambda_handler.lambda_handler"]
```

The container was built and tested locally:

```bash
docker build -t serverless-resnet-infer-fixed -f docker/Dockerfile .
```

Then pushed to **AWS Elastic Container Registry (ECR)** for deployment:

```bash
aws ecr create-repository --repository-name serverless-resnet-infer-fixed
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
docker tag serverless-resnet-infer-fixed:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/serverless-resnet-infer-fixed:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/serverless-resnet-infer-fixed:latest
```

The image was successfully deployed to **AWS Lambda** by selecting _“Container Image”_ and providing the ECR image URI.

## 3. Evaluation and Results

| Metric                    | Description                 | Observed Value                 |
| ------------------------- | --------------------------- | ------------------------------ |
| **Cold start latency**    | Model load + initialization | ~1.3s                          |
| **Warm start latency**    | Repeated inference          | ~0.3s                          |
| **Inference cost**        | Pay-per-request             | No idle cost                   |
| **Scalability**           | Automatic                   | Scales with request volume     |
| **Environment footprint** | Lightweight                 | No EC2 or orchestration needed |

These metrics show that Lambda provides a low-latency, cost-efficient inference setup suitable for real-world ML workloads.
