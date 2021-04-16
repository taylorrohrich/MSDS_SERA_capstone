from chalice import Chalice
import pandas as pd
import pymysql
from chalicelib.data_cleaning import data_cleaning
from chalicelib.env import *
import chalicelib.rdsFunctions as rd
import chalicelib.trackerFunctions as tr 
import boto3



app = Chalice(app_name='sera-preprocessing')


@app.on_s3_event(bucket=raw_bucket,
events=['s3:ObjectCreated:Put'])
def on_raw_data_upload(event):
    data_cleaning()
      ## Connect to S3 ##
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=event.bucket, Key=event.key)
    data = pd.read_csv(obj['Body'])

    ## Connect to Database ##
    # Configuration Values
    endpoint = host
    username = user
    database_name = database

    # Connection
    connection = pymysql.connections.Connection(user=username, passwd=password, host=endpoint, db=database_name)

    # Create Cursor
    cursor1 = connection.cursor()

    ## Create Dictionary for CSV Names ##
    nameDict = {"Participant_Information_Survey": ["2018_2019_participant_measures.csv"],
        "Baseline_Survey": ["2018_summer_baseline_postsim_survey.csv", "2018_fall_baseline_postsim_survey.csv"],
        "Classroom_Norms_Post_Sim_Survey": ["2019_spring_precoach_br_postsim_survey.csv"],
        "Exit_Survey": ["2019_spring_ exit_postsim_survey.csv"],
        "Classroom_Norms_Coding_Baseline": ["2018_summer_baseline_br_perform.csv", "2018_fall_baseline_br_perform.csv"],
        "Classroom_Norms_Coding_Precoach": ["2019_spring_coach_br_perform.csv"],
        "Classroom_Norms_Coding_Postcoach": ["2019_spring_coach_br_perform.csv"],
        "Classroom_Norms_Coding_Exit": ["2019_spring_exit_br_perform.csv"]}

    ## Get List of All CSV Names ##
    all_csvs = []
    for item in list(nameDict.values()):
        all_csvs = all_csvs + item

    ## Get Current CSV Name ##
    csvName = str(event.key)

    ## Generate and Execute Queries ##
    if csvName in all_csvs:
        queries = tr.getTrackerQueries(nameDict, csvName, data, cursor1)
        for query in queries:
            cursor1.execute(query)

    ## Commit and Close Changes ##
    connection.commit()
    connection.close()
    return {'event':'done'}



@app.on_s3_event(bucket=parsed_bucket, events=['s3:ObjectCreated:Put'])
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
    endpoint = host
    username = user
    database_name = database

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

    return {'event': 'done'}
# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
#data_cleaning()