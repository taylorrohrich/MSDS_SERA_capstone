from constants import COLUMN_NAME_MAP, BEHAVIOR_COLUMNS,COLUMN_FACTOR_MAP,FACTORS, CALCULATED_COLUMNS
import pandas as pd
import numpy as np

def cleanColumns(colnames):
    '''
    Function to clean column names and map them to human-readable terms
    '''
    #     Will convert column names to lower, get rid of pound symbol
    colParsed = pd.Series(colnames).str.lower().str.strip().str.replace('#','')
    # Replace with human readable termns
    mappedCols = colParsed.replace(COLUMN_NAME_MAP)
    return mappedCols

def generateScoreVariables(df):
    '''
    Function to convert factor variables to encoding
    '''
    # Iterate through columns
    for column in df.columns:
        # If column a factor
        if column in COLUMN_FACTOR_MAP:
            # Replace it with the encoding
            df[column] = df[column].replace(FACTORS[COLUMN_FACTOR_MAP[column]])
def generateDuplicateColumn(df):
    '''
    Function to generate double_code column
    '''
    # get vidCount
    vidCount = df.groupby('vid').size().reset_index()
    vidCount['duplicate']= np.where(df.groupby('vid').size().reset_index()[0] > 1, 1,0)
    # Check if duplicate
    df['double_code'] = df['vid'].replace({row['vid']:row['duplicate'] for index,row in vidCount.iterrows()})
    
def generateBehaviorColumns(df):
    '''
    Function to generate Behavior Column totals
    '''
    # For each set of behavior columns...
    for name,cols in BEHAVIOR_COLUMNS:
        # Edge case: have two columns we want generated for this
        if name == 'total_nb_se':
            # Sum the # of 1's
            df['tot_nb'] = (df[cols]==1).sum(axis=1)
            # Sum the # of 2's
            df['tot_se'] = (df[cols]==2).sum(axis=1)
        else:
            # Sum the set of behavior columns row-wise
            df[name]=df[cols].sum(axis=1)
            
def dropColsByName(df,start,end):
    '''
    Function to drop a slice of columns by name
    '''
    # Get column names
    columns = df.columns.values
    # Get the start and end index of provided columns
    startIndex = np.where(columns==start)[0][0]
    endIndex = np.where(columns==end)[0][0] + 1
    # Drop this slice of columns
    df.drop(df.columns[startIndex:endIndex], axis=1, inplace=True)
    
def generateCalculatedColumns(df):
    '''
    Function to generate calculated columns
    '''
    # For each calculated column...
    for name,cols in CALCULATED_COLUMNS:
        # Divide first column name by second
        if len(cols)==1:
            df[name]=df[cols[0]]
        else:
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