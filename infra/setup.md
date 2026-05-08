# AWS Infrastructure Setup Guide

Follow these steps to provision all required AWS resources for the MLOps POC pipeline.

---

## 1. S3 Bucket

```bash
aws s3 mb s3://your-mlops-bucket --region us-east-1

# Enable versioning (recommended)
aws s3api put-bucket-versioning \
  --bucket your-mlops-bucket \
  --versioning-configuration Status=Enabled
```

Create the following prefixes (folders):
- `input/` — raw data uploads
- `output/` — SageMaker job output
- `models/` — saved model artifacts

---

## 2. IAM Roles

### Lambda Execution Role
Attach the following policies:
- `AWSLambdaBasicExecutionRole`
- `AmazonS3ReadOnlyAccess`
- `AWSStepFunctionsFullAccess`

### SageMaker Execution Role
Attach the following policies:
- `AmazonSageMakerFullAccess`
- `AmazonS3FullAccess`
- `AmazonEC2ContainerRegistryReadOnly`

---

## 3. Amazon ECR Repository

```bash
aws ecr create-repository --repository-name mlops-processing --region us-east-1
```

---

## 4. Lambda Function

1. Zip the handler:
   ```bash
   cd lambda
   zip trigger_stepfunction.zip trigger_stepfunction.py
   ```

2. Create the function:
   ```bash
   aws lambda create-function \
     --function-name mlops-trigger \
     --runtime python3.11 \
     --role arn:aws:iam::<account-id>:role/<lambda-role> \
     --handler trigger_stepfunction.lambda_handler \
     --zip-file fileb://trigger_stepfunction.zip \
     --environment Variables={STATE_MACHINE_ARN=<state-machine-arn>}
   ```

3. Add S3 trigger (replace values):
   ```bash
   aws lambda add-permission \
     --function-name mlops-trigger \
     --statement-id s3-invoke \
     --action lambda:InvokeFunction \
     --principal s3.amazonaws.com \
     --source-arn arn:aws:s3:::your-mlops-bucket

   aws s3api put-bucket-notification-configuration \
     --bucket your-mlops-bucket \
     --notification-configuration file://s3-notification.json
   ```

---

## 5. Step Functions State Machine

```bash
aws stepfunctions create-state-machine \
  --name mlops-pipeline \
  --definition file://stepfunctions/workflow_definition.json \
  --role-arn arn:aws:iam::<account-id>:role/<stepfunctions-role>
```

---

## 6. Amazon CloudWatch

CloudWatch logs are automatically created for Lambda and SageMaker. To create an alarm for job failures:

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name mlops-job-failure \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:<region>:<account-id>:<sns-topic>
```

---

## 7. Amazon QuickSight

1. Open QuickSight in the AWS Console.
2. Create a new dataset → choose **S3** as the source.
3. Point to `s3://your-mlops-bucket/output/predictions.csv`.
4. Build dashboards from the predictions data.
