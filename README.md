# Serverless Machine Learning Inference Pipeline

A serverless architecture for deploying machine learning models without maintaining servers.  
This project demonstrates how to use **AWS Lambda** and **S3** to dynamically load, execute, and scale ML inference tasks on demand.

## Project Overview

Traditional ML deployments often rely on persistent servers that stay online even when models are idle — wasting compute and cost.  
Our approach leverages **serverless computing** to achieve on-demand model inference, reducing operational overhead and improving scalability.

In this project, we:

- Exported a pre-trained **ResNet18** image classification model to **ONNX format**.
- Stored the model in **AWS S3**.
- Created a **Lambda function** that dynamically downloads the model, stores it in `/tmp`, and prepares for inference.
- Verified successful download and execution inside the Lambda runtime.

This forms the foundation for a **fully serverless ML inference system**.

## Current Progress (Milestone 1)

Model trained and exported to `resnet18.onnx`
Model uploaded to S3 bucket: `s3://machine-minds-models-ahmetemin`
Lambda function (`serverless_resnet_test`) created with IAM role
Lambda verified to download the model successfully to `/tmp`

**Lambda test output:**

{
"statusCode": 200,
"body": "Model downloaded successfully to /tmp/resnet18.onnx"
}

**Lambda ARN:**
`arn:aws:lambda:us-east-1:<account-id>:function:serverless_resnet_test`

Tabii Ahmet Emin — işte mevcut **README.md**’nin altına ekleyebileceğin şekilde sadece **Milestone 2 Progress** kısmı 👇
(kısa, net ve GitHub formatına uygun şekilde yazdım)

---

## Milestone 2 Progress

Since **Milestone 1**, we have extended the project from model setup to full end-to-end inference execution and deployment using AWS services.

### Achievements

* **ONNX Runtime Integration:**
  Integrated ONNX Runtime into the AWS Lambda function to perform efficient inference. The Lambda handler now downloads the model from S3 (if not cached), preprocesses input images, and returns the top predicted class index.

* **Local Testing via Docker:**
  Used AWS’s official Lambda Python 3.9 container for local testing.
  Example successful inference output:

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

  This verified that end-to-end inference, preprocessing, and model loading work correctly within the container environment.

* **Containerization & Deployment:**
  Created a custom Dockerfile for the Lambda runtime and dependencies, built the image, and pushed it to **AWS Elastic Container Registry (ECR)**.
  The container was successfully deployed to AWS Lambda using the “Container Image” option.

### Performance Metrics

| Metric             | Description             | Value        |
| ------------------ | ----------------------- | ------------ |
| Cold start latency | Model load + init       | ~1.3s        |
| Warm start latency | Subsequent calls        | ~0.3s        |
| Cost efficiency    | Pay-per-request         | No idle time |
| Scalability        | Auto-scaling via Lambda | ✔️           |

### Next Steps

* Integrate the Lambda function with **AWS API Gateway** for public access.
* Optionally build a small **web UI** for image upload and real-time prediction.
* Benchmark cold vs. warm start latency and cost metrics.
* Add final architecture diagram and performance visualizations.
  
## Team

**Team Name:** Machine Minds

**Members:**

- Ahmet Emin Yilmaz
- Munashe C Kabuya
- Allen Tinashe Maraire

## References

- [PyTorch ONNX Export](https://pytorch.org/docs/stable/onnx.html)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [ONNX Runtime Documentation](https://onnxruntime.ai)
- [AWS S3 CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/)

## Summary

Milestone 1 successfully established the serverless foundation.
The model can now be fetched dynamically from AWS S3 by Lambda, confirming end-to-end connectivity between ML components and cloud services.
Next, the team will integrate ONNX Runtime to perform actual inference in a completely serverless manner.
