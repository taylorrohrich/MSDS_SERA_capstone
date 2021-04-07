nlp_raw_bucket='sera-nlp-parsed-data'
read -p "Enter Local Directory to read results to from S3: " directory
aws s3 cp s3://$nlp_raw_bucket $directory --recursive