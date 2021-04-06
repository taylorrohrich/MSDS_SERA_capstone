def getExistingIds(tableName, cursor):
    query = "SELECT Participant_ID FROM " + str(tableName)
    cursor.execute(query)
    result = cursor.fetchall()
    existing_ids = [x[0] for x in result]
    return existing_ids


def getColumnNames(tableName, cursor):
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'" + tableName + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    result2 = [x[0] for x in result]
    
    return result2



def getTrackerQueries(csvNameDict, csvName, data, cursor):
    # get the column name to which this csv corresponds
    corresponding_col = None
    for key in csvNameDict.keys():
        if csvName in csvNameDict[key]:
            corresponding_col = key
            
    # get a list of the participants that are already in the participant tracker table
    existing_parts = getExistingIds("Participant_Tracker", cursor)
    
    # set values to appear in the tracker
    taken = "Completed"
    notTaken = "-"
    
    # get a list of all other columns in the PT
    otherCols = getColumnNames("Participant_Tracker", cursor)
    otherCols.remove("Participant_ID")
    otherCols.remove(corresponding_col)
    
    # generate queries
    queries = []
    if 'id_participant' in data.columns:
        for participant in list(data.id_participant):
            if participant in existing_parts:
                query = "UPDATE Participant_Tracker SET " + corresponding_col + " = '" + taken + \
                "' WHERE Participant_ID = '" + participant + "';"
            else:
                query = "REPLACE INTO Participant_Tracker (Participant_ID, " + corresponding_col + ", "
                vals = "'" + participant + "', '" + taken + "', "
                for col in otherCols:
                    query = query + col + ", "
                    vals = vals + "'" + notTaken + "', "
                query = query[:-2] + ") VALUES (" + vals[:-2] + ");"
            queries = queries + [query]
            
    return queries