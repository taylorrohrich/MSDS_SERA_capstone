from chalice import Chalice
import numpy as np 
import pandas as pd
import pymysql
import chalicelib.rdsFunctions as rd
import boto3


## Chalice Setup ##
app = Chalice(app_name='nlp-database-update')
app.debug = True

@app.on_s3_event(bucket='sera-nlp-parsed-data', events=['s3:ObjectCreated:Put'])
def handler(event):


    ## Connect to S3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=event.bucket, Key=event.key)
    uploaded_data = pd.read_csv(obj['Body']) 


    ## Connect to Database ##
    # Configuration Values
    endpoint = "seratestdatabase.c4cjk1vto1om.us-east-2.rds.amazonaws.com"
    username = "admin"
    password = "seracapstone"
    database_name = "teachsim"

    # Connection
    connection = pymysql.connections.Connection(user=username, passwd=password, host=endpoint, db=database_name)

    ## Create Cursor for Database ##
    cursor1 = connection.cursor()

    ### Generate and Execute Queries ###
    tables = ['Fidelity_Measures']
    for table in tables:
        queries = rd.generateQueries(uploaded_data, table, cursor1)
        for query in queries:
            cursor1.execute(query)

    connection.commit()
    connection.close()

    return {'hello': 'world!!!'}
