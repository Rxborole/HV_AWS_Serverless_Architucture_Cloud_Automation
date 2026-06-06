# Assignment 1: Automated EC2 Instance Management Using AWS Lambda and Boto3

## Objective

The objective of this assignment is to automate the starting and stopping of Amazon EC2 instances based on resource tags using AWS Lambda and Boto3.

---

## AWS Services Used

* Amazon EC2
* AWS Lambda
* AWS IAM
* Amazon CloudWatch
* Python (Boto3 SDK)

---

## Architecture

1. Two EC2 instances were created.
2. One instance was tagged with `Action=AutoStop`.
3. Another instance was tagged with `Action=AutoStart`.
4. An AWS Lambda function was created using Python.
5. The Lambda function identifies EC2 instances based on tags.
6. Instances tagged `AutoStop` are stopped automatically.
7. Instances tagged `AutoStart` are started automatically.
8. CloudWatch logs are used for monitoring and verification.

---

## EC2 Instance Configuration

| Instance Name   | Tag Key | Tag Value |
| --------------- | ------- | --------- |
| AutoStopServer  | Action  | AutoStop  |
| AutoStartServer | Action  | AutoStart |

---

## IAM Role Configuration

### Role Name

EC2AutoManger-role

### Attached Policy

* AmazonEC2FullAccess

### Purpose

Provides permissions for Lambda to:

* Describe EC2 instances
* Start EC2 instances
* Stop EC2 instances

---

## Lambda Function Configuration

### Function Name

EC2AutoManger

### Runtime

Python 3.12

### Execution Role

EC2AutoManger-role

---

## Lambda Function Code

```python
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    stop_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['AutoStop']
            }
        ]
    )

    stop_instances = []

    for reservation in stop_response['Reservations']:
        for instance in reservation['Instances']:
            stop_instances.append(instance['InstanceId'])

    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print(f"Stopped: {stop_instances}")

    start_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['AutoStart']
            }
        ]
    )

    start_instances = []

    for reservation in start_response['Reservations']:
        for instance in reservation['Instances']:
            start_instances.append(instance['InstanceId'])

    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print(f"Started: {start_instances}")

    return {
        "statusCode": 200
    }
```

---

## Steps Performed

### Step 1: Create EC2 Instances

* Created two Amazon EC2 t2.micro instances.
* Named them AutoStopServer and AutoStartServer.

### Step 2: Configure Tags

* Added Action=AutoStop tag to AutoStopServer.
* Added Action=AutoStart tag to AutoStartServer.

### Step 3: Create IAM Role

* Created Lambda execution role.
* Attached AmazonEC2FullAccess policy.

### Step 4: Create Lambda Function

* Created Python Lambda function.
* Assigned IAM role.

### Step 5: Deploy Code

* Uploaded and deployed Python code.

### Step 6: Test Lambda Function

* Created test event.
* Invoked Lambda manually.

### Step 7: Verify Results

* Confirmed AutoStopServer was stopped.
* Confirmed AutoStartServer was running.
* Verified CloudWatch logs.

---

## Expected Output

### Before Execution

| Instance        | State   |
| --------------- | ------- |
| AutoStopServer  | Running |
| AutoStartServer | Stopped |

### After Execution

| Instance        | State   |
| --------------- | ------- |
| AutoStopServer  | Stopped |
| AutoStartServer | Running |

---

## Screenshots

Add the following screenshots in the screenshots folder:

1. EC2 Instances
2. EC2 Tags
3. IAM Role Permissions
4. Lambda Function Code
5. Lambda Test Event
6. Successful Lambda Execution
7. CloudWatch Logs
8. Final EC2 Instance Status

---

## Conclusion

Successfully implemented AWS Lambda automation using Boto3 to manage EC2 instances based on tags. The solution automatically starts and stops EC2 instances according to predefined tags, demonstrating AWS automation, serverless computing, IAM permissions, and Python scripting skills.
