FROM amazon/aws-lambda-python:3.9

WORKDIR /var/task

# Install Python deps
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy your handler code
COPY src/lambda_handler.py ${LAMBDA_TASK_ROOT}/lambda_handler.py

# Copy model
COPY src/resnet18.onnx ${LAMBDA_TASK_ROOT}/resnet18.onnx

# COPY src/test_local_infer.py ${LAMBDA_TASK_ROOT}/test_local_infer.py

CMD ["lambda_handler.lambda_handler"]
