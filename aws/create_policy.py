import sys
bucketName= sys.argv[1]
with open("webapp-policy.json", "w") as f:
    f.write('{"Version": "2012-10-17","Statement": [{"Sid": "PublicReadGetObject","Effect": "Allow","Principal": "*","Action": "s3:GetObject","Resource": "arn:aws:s3:::' +bucketName + '/*"}]}')