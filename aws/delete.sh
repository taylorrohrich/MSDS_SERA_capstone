# 1 Delete Chalice Deploy
echo "Deleting Chalice Deploys..."
cd sera-api && chalice delete
cd .. 
cd sera-preprocessing && chalice delete
cd ..
echo "Done."


# 2 Delete Resources

python delete.py


