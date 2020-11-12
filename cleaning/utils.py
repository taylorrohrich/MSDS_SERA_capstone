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
    
def generateBehaviorColumns(df):
    for name,cols in BEHAVIOR_COLUMNS:
        if name == 'total_nb_se':
            df['tot_nb'] = (df[cols]==1).sum(axis=1)
            df['tot_se'] = (df[cols]==2).sum(axis=1)
        else:
            df[name]=df[cols].sum(axis=1)

def generateCalculatedColumns(df):
    for name,cols in CALCULATED_COLUMNS:
        print(len(cols))
        if len(cols)==1:
            df[name]=df[cols[0]]
        else:
            print(cols)
            df[name]=df[cols[0]] / df[cols[1]]
    
    
def lowerSkip(df):
    # clean column names
    df.columns = df.columns.str.lower().str.strip()
    # delete the first row
    df = df.iloc[1:,:]
    return df

def dates(df):
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
    Provide th dataframe and the name of the new column you want created. Then either pass a 
    list of columns to include in the calculation as included or the first and last column if
    all columns in between should also be included.
    '''
    if included == None:
        df[name] = df.loc[:,first:last].mean(axis=1)
    else:
        df[name] = df[included].mean(axis=1)
        
    return df

def destring(df, included=None, first=None, last=None):
    if included == None:
        included = list(df.loc[:,first:last].columns)
    for col in included:
        df[col] = df[col].astype(float)
    return df

def mergeData(df1, df2):
    # more of an append than a merge
    df_new = pd.concat([df1, df2], axis=0, ignore_index=True)
    return df_new

def recode(df, included):
    # used specifically in File 1
    replace_map = {1:5, 2:4, 4:2, 5:1}
    for var in included:
        name = "r_" + str(var)
        df[name] = df[var]
        df[name] = df[name].replace(replace_map)
        df = df.drop([var], axis=1)
    return df