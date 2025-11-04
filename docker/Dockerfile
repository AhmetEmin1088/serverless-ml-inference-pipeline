# Base image: AWS Lambda Python 3.9 runtime
FROM public.ecr.aws/lambda/python:3.9

# Upgrade pip safely
RUN python3.9 -m pip install --upgrade pip

# Copy and install dependencies
COPY src/requirements.txt /tmp/requirements.txt

# Install with version pins to avoid NumPy 2.x conflicts
RUN pip install --no-cache-dir numpy==1.26.4 onnxruntime==1.16.3 pillow torch torchvision \
    && pip install --no-cache-dir -r /tmp/requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code into the Lambda task root
COPY src/ ${LAMBDA_TASK_ROOT}/

# Ensure large model files aren't baked into image
# (models will be downloaded dynamically from S3 at runtime)

# Set the Lambda handler
CMD ["lambda_handler.lambda_handler"]
