import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    #stop Instances tagged with "AutoStop"
    stop_responce = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:AutoStop',
                'Values': ['AutoStop']
            },
        ]
    )

    stop_instances = []
    for reservation in stop_responce['Reservations']:
        for instance in reservation['Instances']:
            stop_instances.append(instance['InstanceId'])  

    if stop_instances:
        ec2.stop_instancces(InstanceIds=stop_instances)
        print(f'Stopping instances: {stop_instances}')

    #start Instances tagged with "AutoStart"
    start_responce = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:AutoStart',
                'Values': ['AutoStart']
            },
        ]
    )       

    start_instances = []
    for reservation in start_responce['Reservations']:
        for instance in reservation['Instances']:
            start_instances.append(instance['InstanceId'])

    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print(f'Starting instances: {start_instances}')

    return {
        'statusCode': 200,
        'body': 'EC2 instances have been started/stopped based on tags.'
    }