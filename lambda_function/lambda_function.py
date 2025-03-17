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
