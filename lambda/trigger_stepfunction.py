import json
import boto3
import os

stepfunctions = boto3.client("stepfunctions")

STATE_MACHINE_ARN = os.environ["STATE_MACHINE_ARN"]


def lambda_handler(event, context):
    """
    Triggered by an S3 PutObject event.
    Starts the Step Functions ML pipeline with the uploaded S3 object as input.
    """
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        print(f"New file detected: s3://{bucket}/{key}")

        input_payload = json.dumps({
            "bucket": bucket,
            "key": key,
            "input_s3_uri": f"s3://{bucket}/{key}"
        })

        response = stepfunctions.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            input=input_payload
        )

        print(f"Step Functions execution started: {response['executionArn']}")

    return {"statusCode": 200, "body": "Pipeline triggered successfully"}
