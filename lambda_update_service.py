import boto3
import os

## Setting variables and importing libraries.
region = "us-west-1"
client = boto3.client('ecs', region_name=region)

CONTAINER_NAME = os.environ['NAME']
DOCKER_IMAGE = os.environ['IMAGE']
FAMILY_DEF = os.environ['TASK_DEF']
CLUSTER_NAME = os.environ['CLUSTER']
SERVICE_NAME = os.environ['SERVICE']

def lambda_handler(event, context):
    print(CLUSTER_NAME)
    
    ## Register a new revision
    response = client.register_task_definition(
        family=FAMILY_DEF,
        taskRoleArn='None',
        networkMode='bridge',
        containerDefinitions=[
            {
                'name': CONTAINER_NAME,
                'image': DOCKER_IMAGE,
                'memory': 512,
                'portMappings': [
                    {
                        'containerPort': 80,
                        'hostPort': 80,
                        'protocol': 'tcp'
                    },
                ],
                'essential': True,
            },
        ],
    )

    ## Update service
    response = client.update_service(
        cluster=CLUSTER_NAME,
        service=SERVICE_NAME,
        desiredCount=1,
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 100
        },
        forceNewDeployment=True
    )
    
    print("Updated the service named {} under the cluster named {} with an updated task definition".format(SERVICE_NAME, CLUSTER_NAME))
   