from chalice import Chalice
import numpy as np 
import pandas as pd 
import pymysql
import chalicelib.trackerFunctions as tr 
import boto3


app = Chalice(app_name='participant-tracker')
app.debug = True
@app.on_s3_event(bucket='sera-raw-data',
events=['s3:ObjectCreated:Put'])
def handler(event):

    ## Connect to S3 ##
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=event.bucket, Key=event.key)
    data = pd.read_csv(obj['Body'])

    ## Connect to Database ##
    # Configuration Values
    endpoint = "seratestdatabase.c4cjk1vto1om.us-east-2.rds.amazonaws.com"
    username = "admin"
    password = "your_password_here"
    database_name = "teachsim"

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

    return {'hello': 'world!!!'}

