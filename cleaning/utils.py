from constants import COLUMN_NAME_MAP, BEHAVIOR_COLUMNS,COLUMN_FACTOR_MAP,FACTORS, CALCULATED_COLUMNS
import pandas as pd
import numpy as np

def cleanColumns(colnames):
    # Parse
    colParsed = pd.Series(colnames).str.lower().str.strip().str.replace('#','')
    mappedCols = colParsed.replace(COLUMN_NAME_MAP)
    return mappedCols

def generateScoreVariables(df):
    for column in df.columns:
        if column in COLUMN_FACTOR_MAP:
            df[column] = df[column].replace(FACTORS[COLUMN_FACTOR_MAP[column]])
def generateDuplicateColumn(df):
    vidCount = df.groupby('vid').size().reset_index()
    vidCount['duplicate']= np.where(df.groupby('vid').size().reset_index()[0] > 1, 1,0)
    df['double_code'] = df['vid'].replace({row['vid']:row['duplicate'] for index,row in vidCount.iterrows()})
def generateBehaviorColumns(df):
    for name,cols in BEHAVIOR_COLUMNS:
        if name == 'total_nb_se':
            df['tot_nb'] = (df[cols]==1).sum(axis=1)
            df['tot_se'] = (df[cols]==2).sum(axis=1)
        else:
            df[name]=df[cols].sum(axis=1)
def dropColsByName(df,start,end):
    columns = df.columns.values
    startIndex = np.where(columns==start)[0][0]
    endIndex = np.where(columns==end)[0][0] + 1
    df.drop(df.columns[startIndex:endIndex], axis=1, inplace=True)
    
def generateCalculatedColumns(df):
    for name,cols in CALCULATED_COLUMNS:
        if len(cols)==1:
            df[name]=df[cols[0]]
        else:
            df[name]=df[cols[0]] / df[cols[1]]
    
    
def lowerSkip(df):
    ''' Makes the column names lowercase and deletes the first row of the dataframe.
    '''
    # clean column names
    df.columns = df.columns.str.lower().str.strip()
    # delete the first row
    df = df.iloc[1:,:]
    return df

def dates(df):
    ''' Makes the assessed column a string type with format mmddyyyy for easier querying.
    '''
    # make assessed the format mmddyyyy
    if "assessed" in df.columns:
        df.assessed = pd.to_datetime(df.assessed, errors='ignore')
        df.assessed = df.assessed.apply(lambda x: x.strftime('%m%d%Y'))
    return df

def basic(df):
    '''
    This function makes the column names lowercase, drops missing values from student and makes 
    student an integer type.
    '''
    # make column names lowercase
    df.columns = df.columns.str.lower().str.strip()
    
    if "student" in df.columns:
        # drop NAs from student
        df = df.dropna(subset=['student'])
        # change data type of student
        df.student.astype(int, copy=False, errors='ignore')
    return df

def newColMean(df, name="RowMean", included=None, first=None, last=None):
    '''
    Provide the dataframe and the name of the new column you want created. Then either pass a 
    list of columns to include in the calculation as included or the first and last column if
    all columns in between should also be included.
    '''
    if included == None:  # turn first and last into a list
        df[name] = df.loc[:,first:last].mean(axis=1)
    else: # generate the new column
        df[name] = df[included].mean(axis=1)
        
    return df

def destring(df, included=None, first=None, last=None):
    ''' Turns the data type of all columns provided to float. Provide the dataframe and either
    a list of specified columns as included or the first and last column name where you also
    want the function to apply to all columns in between.
    '''
    if included == None: # turn first and last into a list
        included = list(df.loc[:,first:last].columns)
    for col in included: # loop through all columns specified
        df[col] = df[col].astype(float) # change the datatype
    return df

def appendData(df1, df2):
    ''' Appends the two dataframes given and returns the appended df.
    '''
    df_new = pd.concat([df1, df2], axis=0, ignore_index=True)
    return df_new

def recode(df, included):
    '''Specifically used in File 1 to swap 1s and 5s and swap 4s and 2s in 
    a new column that has r_ prior to the original column's name. Provide the dataframe
    and a list of the columns for which this should be executed. Note that the original
    column will be deleted after its corresponding new column is added.
    '''
    replace_map = {1:5, 2:4, 4:2, 5:1} # the replacement to take place
    for var in included: # loop through all columns in included
        name = "r_" + str(var) # generated the new column name
        df[name] = df[var] # set the new column values equal to the old column values
        df[name] = df[name].replace(replace_map) # make the replacement of values
        df = df.drop([var], axis=1) # drop the original column
    return df


def replaceEmail(df, combo):
    ''' Provide a dataframe and a dictionary where the student numbers are the key and 
    the corresponding emails are the values. This will replace the current email for that
    student with the one provided or simply add it if they have a missing email.
    '''
    for key in combo.keys(): # loop through keys (student numbers)
        df.loc[df.student==int(key), "email"] = combo[key] # change emails
    return df

def colMissingVals(df, columnName):
    ''' Generate a binary column that indicates whether the given column has a missing value.
    Provide the dataframe and the column of interest. The output will be the dataframe with one 
    additional column named {columnName}_miss that has a 1 for missing values in columnName
    and a 0 for a non-missing value in columnName.
    '''
    replace_map = {1:0, np.NaN:1} # set the replacement schema
    newcol = columnName + "_miss" # generate the new column name
    df[newcol] = df[columnName].replace(replace_map) # make the new column
    return df