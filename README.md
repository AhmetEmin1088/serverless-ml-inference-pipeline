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

## Next Steps (Milestone 2 Plan)

- Integrate `onnxruntime` inside Lambda via a Layer or container image
- Implement inference logic (accept base64 image input → return predicted class)
- Connect Lambda with AWS API Gateway to expose an HTTP endpoint
- Test inference latency and cost efficiency
- (Optional) Add a simple web frontend or CLI for testing

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
