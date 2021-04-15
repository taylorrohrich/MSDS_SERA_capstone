import pandas as pd
import numpy as np

def getColumnNames(tableName, cursor):
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'" + tableName + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    result2 = [x[0] for x in result]
    
    return result2

def overlapColumns(cols1, cols2):
    overlap = []
    for col in cols1:
        if col in cols2:
            overlap = overlap + [col]
    return overlap

def getExistingIds(tableName, cursor):
    query = "SELECT id_participant FROM " + str(tableName)
    cursor.execute(query)
    result = cursor.fetchall()
    existing_ids = [x[0] for x in result]
    return existing_ids

def list_queries(df, columns, tableName, existing_ids):
    queries = []
    for index, row in df.iterrows():
        pid = row['id_participant']
        valid_pid = False
        if type(pid) == str:
            if len(pid) >= 10 and len(pid) <= 12:
                valid_pid = True
                
        # if the row for that participant already exists, just update it
        if pid in existing_ids:
            req_update = False
            query = "UPDATE " + tableName + " SET "
            for col in columns:
                newval = row[col]
                if type(newval) == str:
                    query = query + col + " = '" + newval + "' , "
                    req_update = True
                elif np.isnan(float(newval)) == False: 
                    query = query + col + " = " + str(newval) + " , "
                    req_update = True
            if req_update == True:
                query = query[:-2]
                query = query + "WHERE id_participant = '" + row["id_participant"] + "';"
                queries = queries + [query]
        
        # if that participant is not in the database, create/replace the row
        elif valid_pid == True:
            req_update = False
            query = "REPLACE INTO " +  tableName + " "
            cols = "("
            vals = "("
            for col in columns:
                val = row[col] 
                if type(val) == str:
                    cols = cols + str(col) + ", "
                    vals = vals + "'" + val + "', "
                    req_update = True
                elif np.isnan(float(val)) == False: 
                    cols = cols + str(col) + ", "
                    vals = vals + str(val) + ", "
                    req_update = True
            query = query + cols[:-2] + ") " + 'VALUES ' + vals[:-2] + ");"
            if req_update == True:
                queries = queries + [query]
                existing_ids = existing_ids + [row['id_participant']]
            
    return queries
    

def generateQueries(df, tableName, cursor):
    df_cols = df.columns
    tab_cols = getColumnNames(tableName, cursor)
    overlap = overlapColumns(df_cols, tab_cols)
    
    existing_ids = getExistingIds(tableName, cursor)
    
    query_list = list_queries(df, overlap, tableName, existing_ids)
    
    return query_list