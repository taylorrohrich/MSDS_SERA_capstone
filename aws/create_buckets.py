
import sys
import boto3

bucketNames = sys.argv[1:]
names = ['raw_bucket','parsed_bucket','webapp_bucket']
print('Creating Buckets...')
s3_client = boto3.client('s3')
for name in bucketNames:
        try:
            print(f'Creating bucket {name}...')
            s3_client.create_bucket(Bucket=name)
            print('Done.')
        except:
            print('Bucket already exists.')

with open("env.py", "w") as f:
    for name,bucketName in zip(names,bucketNames):
        f.write(f'{name}="{bucketName}"\n')
