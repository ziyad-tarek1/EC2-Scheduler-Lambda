# AWS EC2 Scheduler Using EventBridge and Lambda

## Introduction

The **AWS EC2 Scheduler** project provides a cost-effective solution for managing Amazon EC2 instances by automating their startup and shutdown processes. Utilizing AWS Lambda and Amazon EventBridge, this project allows users to schedule EC2 instances to run only when needed, significantly reducing unnecessary costs associated with idle resources.

By implementing this serverless architecture, users can easily manage their EC2 instances based on specific tags, ensuring that resources are utilized efficiently without manual intervention. This repository contains all the necessary configurations, including Lambda function code, IAM policies, and EventBridge rules, to help you set up and deploy this automation in your AWS environment.

![image](https://github.com/user-attachments/assets/0b8046b5-14a3-4609-95c0-e292eeeea7e9)


## Repository Structure
```
ec2-scheduler-lambda/
├── lambda_function/
│   ├── lambda_function.py  # The Python script for the Lambda function
├── iam/
│   ├── lambda_iam_policy.json  # IAM policy for the Lambda function
├── eventbridge/
│   ├── eventbridge_rule.json  # Configuration for the EventBridge rule
├── README.md  # Project documentation
```

# AWS EC2 Scheduler Using EventBridge and Lambda

## Overview
Managing AWS EC2 instances efficiently can lead to significant cost savings. This project automates the shutdown and startup of EC2 instances using AWS Lambda, EventBridge, and IAM roles. The solution ensures that EC2 instances are only running when needed, helping optimize costs.

## Architecture

1. **Amazon EventBridge**: Schedules events to trigger the Lambda function at predefined times.
2. **AWS Lambda**: Runs the automation logic to start and stop EC2 instances.
3. **Amazon EC2**: The target instances to be managed.
4. **AWS IAM Role**: Grants Lambda the necessary permissions to manage EC2 instances.

## Prerequisites
- AWS Account
- IAM Role with necessary permissions
- Tagged EC2 instances (e.g., `AutoStartStopEC2=true`)

## Installation and Setup

### 1. Create the IAM Role for Lambda
Create an IAM policy with the following JSON and attach it to a new IAM role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:StopInstances",
                "ec2:StartInstances",
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        }
    ]
}
```

### 2. Deploy the Lambda Function
1. Create a new Lambda function in AWS.
2. Use Python as the runtime.
3. Upload the following `lambda_function.py` file:

```python
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    tag_key = 'AutoStartStopEC2'
    tag_value = 'true'

    instances = ec2.describe_instances(Filters=[{'Name': 'tag:' + tag_key, 'Values': [tag_value]}])
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            
            if instance_state == 'running':
                ec2.stop_instances(InstanceIds=[instance_id])
                logger.info(f"Stopped EC2 instance {instance_id}")
            elif instance_state == 'stopped':
                ec2.start_instances(InstanceIds=[instance_id])
                logger.info(f"Started EC2 instance {instance_id}")
            else:
                logger.info(f"EC2 instance {instance_id} is in state {instance_state}, skipping.")
    
    return {
        'statusCode': 200,
        'body': 'Action executed for instances'
    }
```

### 3. Create an EventBridge Rule
Use the following JSON configuration to create an EventBridge rule to trigger the Lambda function at scheduled times.

```json
{
  "Name": "EC2-Auto-Start-Stop",
  "ScheduleExpression": "cron(0 8 * * ? *)",
  "Targets": [
    {
      "Id": "1",
      "Arn": "arn:aws:lambda:region:account-id:function:LambdaFunctionName"
    }
  ]
}
```

Modify the `ScheduleExpression` accordingly:
- `cron(0 8 * * ? *)` → Runs at 08:00 UTC every day
- `cron(0 17 * * ? *)` → Runs at 17:00 UTC every day

### 4. Tag EC2 Instances
Ensure EC2 instances have the following tag:
- **Key**: `AutoStartStopEC2`
- **Value**: `true`

## Conclusion
By setting up this automation, you can significantly reduce AWS costs by ensuring EC2 instances only run when necessary. This serverless approach is cost-effective and minimizes manual intervention.

