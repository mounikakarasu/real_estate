# 1. Force x86_64 Architecture
FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11

# 2. Install Dependencies
RUN yum update -y && \
    yum install -y gcc gcc-c++ python3-devel

RUN pip install --upgrade pip

# 3. Install compatible libraries (Using binary wheels to avoid compilation)
RUN pip install "numpy==1.26.4" "scikit-learn==1.3.2" "pandas==2.1.4" joblib boto3

# 4. Copy Code & Model
COPY app.py ${LAMBDA_TASK_ROOT}
COPY lead_scoring_model.joblib ${LAMBDA_TASK_ROOT}

# 5. CRITICAL: Fix Windows Permissions
# Ensure the files are readable/executable by the Lambda user
RUN chmod 644 ${LAMBDA_TASK_ROOT}/lead_scoring_model.joblib
RUN chmod 755 ${LAMBDA_TASK_ROOT}/app.py

CMD [ "app.handler" ]