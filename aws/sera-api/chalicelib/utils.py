
import pandas as pd
import os
import mysql.connector
from chalice import Chalice,BadRequestError, Response

def parse_url_params(params):
    defaultParams = {
        'time_list':None,
        'measure_list':None,
        'group_list':None,
        'specific_measure_list': None,
        'field_type_list': None,
        }
    for param in defaultParams.keys():
        if param in params:
            defaultParams[param] = params[param].split(',')
    return defaultParams

def fetchData(request,conn,returnType):
    query_params = request["query_params"]
    parsed_params = parse_url_params(query_params)
    df = sql_request(conn, parsed_params['time_list'],parsed_params['measure_list'],parsed_params['group_list'],parsed_params['specific_measure_list'],parsed_params['field_type_list'])
    if returnType == 'json':
        return df.to_json()
    else:
        df.to_csv(f'/tmp/query.csv', index=False)
        with open('/tmp/query.csv', "rb") as f:
            contents = f.read()
        f.close()
        headers = {
        "Content-Type": "text/csv"
        }
        body = contents
        return Response(body=body, headers=headers)

def convert_semester(time_list):
    converted_list=[]
    for element in time_list:
        if element=="Fall 2017":
            converted_list.append(1)
        elif element=="Spring 2018":
            converted_list.append(2)
        elif element=="Fall 2018":
            converted_list.append(3)
        elif element=="Spring 2019":
            converted_list.append(4)     
        elif element=="Fall 2019":
            converted_list.append(5)
        elif element=="Spring 2020":
            converted_list.append(6)  
    return converted_list
#define a function to convert the result of the query into a pandas table
def output_table(conn,query):
    result=pd.read_sql_query(query, con=conn)
    return result    

def sql_request(conn, time_list,measure_list,group_list=None,Specific_measure_list=None,field_type=None):
    query_all="""select """
    #handle exception if no level1 time parameter or no measure is provided
    #should raise error and print the error message later
    if len(time_list)==0:
        raise MyValidationError("At least one year/semester is required.")
    if len(measure_list)==0:
        raise MyValidationError("At least one measurement is required.")
        
    #return the rows according to time given
    #if user request data from all year
    time_list=[str(elem) for elem in time_list]
    time=" "
    
    if time_list[0]=="All":
        time=" "
    elif time_list[0].isdigit():
        time=time+"where id_year in ("
        time = time+",".join(map(str, time_list))
        time=time+')'
    else:
        time_list=convert_semester(time_list)
        time=time+"where id_study in ("
        time = time+",".join(map(str, time_list))
        time=time+')' 
        
    #return the table according to the measure requested
    measure_list=[elem.replace(" ","_") for elem in measure_list]
    tables="from "+measure_list[0]
    # if a combinition of measure is requested
    if len(measure_list)>1:
        for measure in measure_list[1:]:
            tables=tables+" join "+measure+" on "+measure_list[0]+".id_participant="+measure+".id_participant "
    #handle if user provide level2
    #suppose that the first variable in the list represent which group that users want to search
    if group_list==None:
        pass
    else:
        column_name=group_list[0]
        group=column_name+" in ("
        group=group+",".join(map(str,group_list[1:]))
        group=group+")"
        time=time+" AND "+group
    
    #handle if user provide level4
    if Specific_measure_list==None:
        query_all=query_all+"* "
        
    else:
        specific_measure = ",".join(map(str, Specific_measure_list))
        query_all=query_all+specific_measure+" "
    
    #handle if user provide level5
    df=pd.DataFrame()
    for elem in measure_list:
        df=df.append(output_table(conn,"SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+elem+"'"),ignore_index=True)
    if field_type==None:
        pass
    elif field_type=="Numeric":
        Numeric_cols=",".join(map(str, df[df["DATA_TYPE"]!=b'varchar']["COLUMN_NAME"].to_list()))
        query_all="SELECT "+Numeric_cols+" "
        
    elif field_type=="Text":
        text= df[df["DATA_TYPE"]==b'varchar']["COLUMN_NAME"].to_list()
        text=list(set(text))
        text=["Identifiers.id_participant" if x=="id_participant" else x for x in text]
        Text_cols=",".join(map(str, text))
        query_all="SELECT "+Text_cols+" "
        
    query_all=query_all+tables+time
    df = output_table(conn,query_all).reset_index()
    return df.loc[:,~df.columns.duplicated()]
        
        