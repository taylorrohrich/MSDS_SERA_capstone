from chalice import Chalice,BadRequestError, Response
from chalicelib.utils import *
from chalicelib.env import *
import mysql.connector
import pandas as pd
import boto3

app = Chalice(app_name='sera-api')

conn = None

def get_conn():
    global conn
    if conn is None:
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
    return conn.cursor(buffered=True)

@app.route('/json',cors=True)
def json():
    request = app.current_request.to_dict()
    query_params = request["query_params"]
    conn = get_conn()
    try:
       return fetchData(request,conn,'json')
    except:
        raise BadRequestError('Query params are not valid.')

@app.route('/csv',cors=True)
def csv():
    request = app.current_request.to_dict()
    query_params = request["query_params"]
    conn = get_conn()
    # try:
    return fetchData(request,conn,'csv')
    # except:
    #     raise BadRequestError('Query params are not valid.')


@app.route('/nlp',cors=True)
def csv():
    s3_client = boto3.client('s3')
    request = app.current_request.to_dict()
    query_params = request["query_params"]
    conn = get_conn()
    # try:
    filename=query_params["filename"]
    s3_client.download_file('sera-nlp-parsed-data', f"{filename}.csv", f"/tmp/{filename}.csv")
    with open(f"/tmp/{filename}.csv", "rb") as f:
        contents = f.read()
    f.close()
    headers = {
    "Content-Type": "text/csv"
    }
    body = contents
    return Response(body=body, headers=headers)
    # except:
    #     raise BadRequestError('Query params are not valid.')

@app.route('/tracker',cors=True)
def tracker():
    conn = get_conn()
    try:
        result=pd.read_sql_query("SELECT * FROM Participant_Tracker", con=conn)
        return result.to_json(orient='index')
    except:
        raise BadRequestError('Query params are not valid.')
# @app.route('/test')
# def test():
#     contents = '1,2\n3,4\n5,6\n'
#     headers = {
#         "Content-Type": "text/csv"
#         #"Content-Disposition": "attachment; filename={}".format(file_name),
#         #"Content-Length": str(os.path.getsize(file_path))
#     }
#     body = contents
#     return Response(body=body, headers=headers)
#connection = get_conn()
# # cursor = connection.cursor(buffered=True)
# # # view table
# # cursor.execute()
# # result = cursor.fetchall()
# result=pd.read_sql_query("SELECT * FROM Participant_Tracker", con=connection)
# print(result.to_json())
# # print(connection)
# # print(sql_request(connection,["All"],["Identifiers","Performance Measures"]).to_json())
