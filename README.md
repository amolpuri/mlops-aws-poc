# MLOps on AWS — End-to-End ML Pipeline POC

> **Author:** Amol Puri  
> **Stack:** Amazon S3 · Amazon SageMaker · Amazon ECR · AWS Lambda · AWS Step Functions · Amazon QuickSight · Amazon CloudWatch

---

## Overview

This repository contains a proof-of-concept for an end-to-end **MLOps pipeline** on AWS. MLOps (Machine Learning Operations) automates the full lifecycle of a machine learning model — from data ingestion and training to containerized deployment and monitoring — enabling reliable, scalable, and production-ready ML systems.

---

## Architecture

```
S3 (raw data upload)
      │
      ▼
AWS Lambda  ──────────────────────► triggers Step Functions workflow
      │
      ▼
AWS Step Functions
      │
      ├──► SageMaker Processing Job  (Docker image from ECR)
      │           │
      │           ▼
      │        S3 (predictions / output)
      │           │
      │           ▼
      │       Amazon QuickSight  (dashboards & visualizations)
      │
      └──► Amazon CloudWatch  (monitoring & alerts)
```

---

## AWS Services Used

| Service | Role |
|---|---|
| **Amazon S3** | Store raw input data, trained models, and job output |
| **Amazon SageMaker** | Train, tune, and deploy ML models at scale |
| **Amazon ECR** | Host Docker images for SageMaker processing jobs |
| **AWS Lambda** | Trigger Step Functions on new S3 uploads |
| **AWS Step Functions** | Orchestrate the end-to-end ML workflow |
| **Amazon QuickSight** | Visualize predictions and model output |
| **Amazon CloudWatch** | Monitor pipeline health and set alerts |

---

## Repository Structure

```
mlops-aws-poc/
├── data/
│   ├── raw/                  # Sample / placeholder raw input data
│   └── processed/            # Cleaned & transformed datasets
├── docker/
│   ├── Dockerfile            # Container image for SageMaker processing job
│   └── requirements.txt      # Python dependencies for the container
├── lambda/
│   └── trigger_stepfunction.py   # Lambda handler — triggers Step Functions on S3 event
├── stepfunctions/
│   └── workflow_definition.json  # Step Functions state machine definition (ASL)
├── sagemaker/
│   ├── notebooks/
│   │   └── train_and_evaluate.ipynb  # Training & evaluation notebook
│   └── scripts/
│       └── preprocess.py     # SageMaker processing script
├── infra/
│   └── setup.md              # AWS resource setup instructions
├── docs/
│   └── mlops_blog.md         # Original blog post / detailed write-up
├── .gitignore
└── README.md
```

---

## Pipeline Walkthrough

### 1. Data Ingestion
Raw data is uploaded to an **S3 bucket**. An **S3 event notification** fires when a new object arrives.

### 2. Lambda Trigger
The **Lambda function** (`lambda/trigger_stepfunction.py`) receives the S3 event and calls `start_execution` on the Step Functions state machine, passing the S3 object key as input.

### 3. Step Functions Orchestration
The **Step Functions workflow** (`stepfunctions/workflow_definition.json`) defines the sequence of states:
- Invokes a **SageMaker Processing Job**
- Passes the Docker image URI (stored in ECR) and the S3 input path

### 4. Model Training & Evaluation
Inside the SageMaker Processing Job:
- Data is cleaned, transformed, and split into train/validation sets
- A model is trained (TensorFlow / PyTorch / sklearn)
- Hyperparameters (learning rate, batch size, regularization) are tuned
- Performance metrics (accuracy, precision) are evaluated on the validation set

### 5. Output Storage
Job outputs (predictions, transformed data) are written back to **S3** in CSV / JSON / Parquet format.

### 6. Visualization
**Amazon QuickSight** connects to the output S3 bucket to render interactive dashboards and reports.

### 7. Monitoring
**Amazon CloudWatch** tracks pipeline execution, job status, and model metrics in real time.

---

## Getting Started

### Prerequisites
- AWS CLI configured with appropriate IAM permissions
- Docker installed locally
- Python 3.8+

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/mlops-aws-poc.git
   cd mlops-aws-poc
   ```

2. **Create the S3 bucket**
   ```bash
   aws s3 mb s3://your-mlops-bucket
   ```

3. **Build & push Docker image to ECR**
   ```bash
   cd docker
   # Authenticate Docker to ECR
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com

   # Build and push
   docker build -t mlops-processing .
   docker tag mlops-processing:latest <account-id>.dkr.ecr.<region>.amazonaws.com/mlops-processing:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/mlops-processing:latest
   ```

4. **Deploy Lambda function**
   See `infra/setup.md` for IAM roles and deployment steps.

5. **Create Step Functions state machine**
   Upload `stepfunctions/workflow_definition.json` via the AWS console or CLI.

6. **Upload data to trigger the pipeline**
   ```bash
   aws s3 cp data/raw/sample.csv s3://your-mlops-bucket/input/sample.csv
   ```

---

## Blog Post

The detailed write-up explaining each component is available in [`docs/mlops_blog.md`](docs/mlops_blog.md).

---

## License

MIT
