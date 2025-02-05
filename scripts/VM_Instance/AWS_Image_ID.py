import boto3

ec2_client = boto3.client('ec2') #interesują mnie EC2
images = ec2_client.describe_images(Owners=['amazon']) #Pobiera obrazy z AWS

for image in images['Images'][:5]:  # Pobiera tylko 5 pierwszych wyników
    print(f"AMI ID: {image['ImageId']}, Name: {image['Name']}")