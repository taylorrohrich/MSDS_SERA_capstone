# Parsed Bucket Name
read -p "Enter Raw Data Bucket Name: " raw_bucket

aws s3 sync sample_files/ s3://$raw_bucket