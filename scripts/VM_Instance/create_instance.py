#!python3
import boto3
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

def create_instance():
    # Pobierz zmienne z pliku .env
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_REGION')
    ami_id = os.getenv('AMI_ID')
    instance_type = os.getenv('INSTANCE_TYPE')
    key_name = os.getenv('KEY_NAME')
    security_groups = os.getenv('SECURITY_GROUPS').split(',')

    # Utwórz sesję i połączenie z EC2
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    
    ec2 = session.resource('ec2')
    
    # Tworzenie instancji EC2
    instance = ec2.create_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroups=security_groups
    )[0]
    
    print(f"Utworzono instancję {instance.id}")

create_instance()