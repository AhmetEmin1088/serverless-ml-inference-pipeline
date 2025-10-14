# Milestone 1 — Serverless ML Inference Pipeline

## Team

- Person A: ...
- Person B: ...
- Person C: ...

## Goal

Export ResNet18 to ONNX, upload to S3, implement Lambda that downloads the model and runs (test).

## Files

- src/export_resnet_onnx.py
- src/onnx_inference_test.py
- src/lambda_infer_from_s3.py

## Steps Completed

1. Exported model to resnet18.onnx (size: XX MB). (Person A)
2. Uploaded resnet18.onnx to s3://machine-minds-models-<unik>/ (Person B)
3. Lambda function `serverless_resnet_test` created and downloads model to /tmp (Person B)
4. Local ONNX inference validated (Person A)

## Test Results

- Local inference output: <screenshot or console text>
- Lambda console invoke result: Execution succeeded (attached screenshot)
- CloudWatch logs: (link or screenshot)

## Next steps

- Integrate onnxruntime into Lambda package / layer and implement full inference.
- Add API Gateway for external access.
