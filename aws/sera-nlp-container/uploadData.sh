nlp_raw_bucket='sera-nlp-raw-data'
read -p "Enter Local Directory to copy to S3: " directory
aws s3 cp $directory s3://$nlp_raw_bucket/$directory --recursive