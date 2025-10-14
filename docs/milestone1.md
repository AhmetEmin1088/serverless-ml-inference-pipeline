# Milestone 1 — Progress Report  
**Project:** Serverless Machine Learning Inference Pipeline  
**Course:** ECE 6210 – Machine Intelligence (Fall 2025)  
**Team:** Machine Minds  
**Members:** [Ahmet Emin Yilmaz], [Munashe C Kabuya], [Allen Tinashe Maraire]  
**Date:** October 15, 2025  

## 1. Current Problem Formulation

Traditional machine learning deployments rely on servers that must stay online even when models are idle. This leads to high maintenance costs and inefficient resource use, especially for small teams and research projects.  
Our project proposes a **serverless machine learning inference pipeline** that uses **AWS Lambda** and **S3** to dynamically load and execute a trained model on demand.  

We are using **ResNet18**, a convolutional neural network (CNN) for image classification, exported to **ONNX** format for compatibility with cloud runtimes. The goal is to achieve cost-efficient, fully managed ML inference without maintaining servers.

## 2. Progress So Far

### Model Setup  
- Implemented and tested ResNet18 with the CIFAR-10 dataset locally using PyTorch.  
- Exported the trained model to ONNX format (`resnet18.onnx`).  
- Verified model inference locally using ONNX Runtime.

### Cloud Infrastructure  
- Created an AWS S3 bucket (`s3://machine-minds-models-2025`) and uploaded the ONNX model.  
- Configured AWS IAM roles with the **AWSLambdaBasicExecutionRole** policy.  
- Developed and deployed a Lambda function (`serverless_resnet_test`) that downloads the ONNX model from S3 to `/tmp`.  
- Increased Lambda timeout to 60s to handle large file transfers.  
- Verified successful model download:  

  ```json
  {
    "statusCode": 200,
    "body": "Model downloaded successfully to /tmp/resnet18.onnx"
  }
