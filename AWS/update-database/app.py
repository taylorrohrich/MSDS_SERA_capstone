from chalice import Chalice
import numpy as np 
import pandas as pd
import pymysql
import chalicelib.rdsFunctions as rd
import boto3


## Chalice Setup ##
app = Chalice(app_name='update-database')
app.debug = True

@app.on_s3_event(bucket='sera-parsed-data', events=['s3:ObjectCreated:Put'])
def handler(event):


    ## Fake Temporary Data
    #test_data = {'id_participant':['testID1', 'testID2'], 'id_section':[3,2], 'id_site':[1,1], 'id_year':[2021, 1819], 'fb_treat_cond':[1,0], 's18_treat_cond':[3,2]}
    #uploaded_data = pd.DataFrame(test_data)

    ## Connect to S3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=event.bucket, Key=event.key)
    uploaded_data = pd.read_csv(obj['Body']) 


    ## Connect to Database ##
    # Configuration Values
    endpoint = "seratestdatabase.c4cjk1vto1om.us-east-2.rds.amazonaws.com"
    username = "admin"
    password = "your_password_here"
    database_name = "teachsim"

    # Connection
    connection = pymysql.connections.Connection(user=username, passwd=password, host=endpoint, db=database_name)

    ## Create Cursor for Database ##
    cursor1 = connection.cursor()

    ### Generate and Execute Queries ###
    tables = ['Identifiers', 'Survey_Measures', 'Participant_Measures', 'Performance_Measures']
    for table in tables:
        queries = rd.generateQueries(uploaded_data, table, cursor1)
        for query in queries:
            cursor1.execute(query)

    connection.commit()
    connection.close()

    return {'hello': 'world!!!'}
