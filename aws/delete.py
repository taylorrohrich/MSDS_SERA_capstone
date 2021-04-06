import boto3
import env
s3 = boto3.resource('s3')
client = boto3.client('rds')
buckets = [env.raw_bucket,env.parsed_bucket,env.webapp_bucket]
print('Deleting Buckets...')
for bucket in buckets:
    print(f'Deleting Bucket {bucket}...')
    try:
        bucket = s3.Bucket(bucket)
        # Boto3
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
    except:
        print('Bucket does not exist.')
    print(f'Done.')

print('Deleting RDS...')
try:
    response = client.delete_db_instance(
        DBInstanceIdentifier='sera-db-1',
        SkipFinalSnapshot=True,
    )
except:
    print('RDS instance does not exist.')
print('Done.')
