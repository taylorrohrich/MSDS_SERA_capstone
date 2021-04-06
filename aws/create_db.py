import boto3
import time
ec2 = boto3.client('ec2')
client = boto3.client('rds')

identifier = 'sera-db-1'
database = 'seradb'
user = 'seraadmin'
pw = 'serapassword'
subnetExists = True

try:
    client.describe_db_subnet_groups(
        DBSubnetGroupName='seradbsubnet'
    )
    print('Subnet already exists.')
except:
    subnetExists=False

if not subnetExists:
    print('Creating new subnet...')
    response = ec2.describe_security_groups( Filters=[
            {
                'Name': 'group-name',
                'Values':['default']
            }])

    vpcId = response['SecurityGroups'][0]['VpcId']

    x = ec2.describe_subnets(Filters=[
            {
                'Name': 'vpc-id',
                'Values':[vpcId]
            }])
    availZones = ['us-east-1a','us-east-1b','us-east-1c']
    subnets = list(map(lambda x: x['SubnetId'], filter(lambda x: x['AvailabilityZone'] in availZones, x['Subnets'])))
    response = client.create_db_subnet_group(
        DBSubnetGroupName='seradbsubnet',
        DBSubnetGroupDescription='sera db subnet',
        SubnetIds=subnets
    )
    print('Done.')
dbExists=True
try:
    client.describe_db_instances(DBInstanceIdentifier=identifier)
    print('Database already exists.')
except:
    dbExists=False
if not dbExists:
    print('Creating new database...')
    response = client.create_db_instance(DBInstanceIdentifier=identifier,
                                AllocatedStorage=100,
                                DBName=database,
                                Engine='mysql',
                                DBSubnetGroupName= 'seradbsubnet',
                                PubliclyAccessible=True,
                                MasterUsername=user,
                                MasterUserPassword=pw,
                                #    VpcSecurityGroupIds=['YOUR_SECURITY_GROUP_ID'],
                                DBInstanceClass='db.t2.micro')
    print('Done.')


host = None
running = True
print('Waiting for DB to load...')
while running:
    response = client.describe_db_instances(DBInstanceIdentifier=identifier)

    db_instances = response['DBInstances']
    if len(db_instances) != 1:
        raise Exception('Whoa cowboy! More than one DB instance returned; this should never happen')

    db_instance = db_instances[0]

    status = db_instance['DBInstanceStatus']

    print(f'Last DB Status: {status}')

    time.sleep(10)
    if status == 'available':
        endpoint = db_instance['Endpoint']
        host = endpoint['Address']
        # port = endpoint['Port']

        print(f'DB instance ready with host: {host}')
        host=host
        running = False      
print('Done.')                
db = client.describe_db_instances(DBInstanceIdentifier=identifier)

credentials = {'user':user,
'password':pw,
'host':host,
'database':database}

with open("env.py", "a") as f:
    for key,val in credentials.items():
        f.write(f'{key}="{val}"\n')