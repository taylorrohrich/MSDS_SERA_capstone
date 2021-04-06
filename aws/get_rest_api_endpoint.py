import boto3
client = boto3.client('apigateway')

response = client.get_rest_apis(
)
apiId = list(filter(lambda x: x['name'] =='sera-api',response['items']))[0]['id']

endpoint = f'https://{apiId}.execute-api.us-east-1.amazonaws.com'

with open("env.js", "w") as f:
    f.write(f'const API_ENDPOINT="{endpoint}/api"\n')
    f.write('export {API_ENDPOINT}')
