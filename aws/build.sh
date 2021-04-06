## 1 Generate .aws/credentials

# Install AWS CLI

# curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
# sudo installer -pkg AWSCLIV2.pkg -target /
# sudo installer -pkg ./AWSCLIV2.pkg -target /

# Install Python Requirements

#pip install -r requirements.txt

# Install npm packages

# # npm install create-react-app

# #aws configure

## 2 Global Constants

# Raw Bucket Name
read -p "Enter Raw Data Bucket Name: " raw_bucket
# Parsed Bucket Name
read -p "Enter Parsed Data Bucket Name: " parsed_bucket
# Webapp Bucket Name
read -p "Enter Webapp Bucket Name: " webapp_bucket

## 3 Create Buckets

python create_buckets.py $raw_bucket $parsed_bucket $webapp_bucket

## 4 Create RDS

python create_db.py 

python create_tables.py

cp env.py sera-preprocessing/chalicelib/env.py
cp env.py sera-api/chalicelib/env.py

## 5 Deploy API GATEWAY, PREPROCESSING
cd sera-api && chalice deploy
cd ..
cd sera-preprocessing && chalice deploy
cd ..

# Get api gateway endpoint
python get_rest_api_endpoint.py
cp env.js sera-webapp/src/constants/env.js

## 7 Deploy WEBAPP

python create_policy.py $webapp_bucket
aws s3api put-bucket-policy --bucket $webapp_bucket --policy file://webapp-policy.json
aws s3 website s3://$webapp_bucket/ --index-document index.html --error-document index.html
cd sera-webapp && npm run build
aws s3 sync build/ s3://$webapp_bucket

