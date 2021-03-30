## 1 Generate .aws/credentials

# Install AWS CLI
# curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
# sudo installer -pkg AWSCLIV2.pkg -target /
# sudo installer -pkg ./AWSCLIV2.pkg -target /

#aws configure

## 2 Global Constants

# Raw Bucket Name
read -p "Enter Raw Data Bucket Name: " raw_bucket
# Parsed Bucket Name
read -p "Enter Raw Parsed Bucket Name: " parsed_bucket
# Webapp Bucket Name
read -p "Enter Webapp Bucket Name: " parsed_bucket
## 3 Chalice Deploy

## 4 Webapp Deploy

# Get api gateway endpoint

aws apigateway get-rest-apis --query 'items[?name==`sera-api`]'