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
    replace_map = {1:0, 2:0, 3:0, 0:0, np.NaN:1} # set the replacement schema
    newcol = columnName + "_miss" # generate the new column name
    df[newcol] = df[columnName].replace(replace_map) # make the new column
    return df

def fix_email_add(string):
    '''
    helper function that fixed the email address to correct format
    '''
    result=''
    #search if the email contains '@'
    index=string.find("@")
    #if the email do not contain '@'
    #the user only enter computing id
    if index==-1:
        #put @virginia.edu after the computing id
        result=string+'@virginia.edu'
    #changing all the email address to format of computing id@virginia.edu
    #this step is to fix the if has a typo in virginia.edu or entered gmail.com instead
    else:
        result=string[:index]+'@virginia.edu'
    return result 

def format_email(data):
    '''
    function to format all the email address, changing all the input email address to computingid@virginia.edu
    this function is avoid if someone just input there computing id or misspelling the virginia or input the gmail.com instead.
    '''
    data.email =data.email.str.strip()
    data.email =data.email.str.lower()
    email_fix = data.loc[~data["email"].str.contains("virginia")]
    email_fix['email']=email_fix['email'].apply(lambda x:fix_email_add(x))
    for i in email_fix.index:
        data.at[i,"email"]=email_fix.at[i,'email']   

def convert_columns(data,beh_map,sim_map):
    '''
    convert categorical column to numeric 
    data would be dataframe, beh_map is the map that changing the categorical respond in behaviour columns to numeric 
    sim_map is the map that changing the categorical respond in sim columns to numeric 
    '''
    data.loc[:,'beh_fidgeting':'beh_mood_changes']=data.loc[:,'beh_fidgeting':'beh_mood_changes'].replace(beh_map)
    data.loc[:,'sim_nervous' :'sim_enough_time']=data.loc[:,'sim_nervous' :'sim_enough_time'].replace(sim_map)

def convert_numeric(data):
    '''
    convert string columns to float for later scalling use
    '''
    data.loc[:,'app_coach_stu':'app_beh_manage_teach']=data.loc[:,'app_coach_stu':'app_beh_manage_teach'].astype('float')
    data[['sim_fbsk','sim_cmsk']]=data[['sim_fbsk','sim_cmsk']].astype('float')

def generate_Iowa_Score_Scale(data):
    '''
    function to generate Iowa score
    '''
    data['beh_rating_opdefiant']=data.loc[:,'beh_quarrelsome': 'beh_uncooperative'].mean(axis=1)
    data['beh_rating_impulsive']=data.loc[:,'beh_fidgeting':'beh_short_attention'] .mean(axis=1)
    data['beh_rating'] =data.loc[:,'beh_fidgeting':'beh_mood_changes'].mean(axis=1)
    #label var beh_rating_opdefiant "Iowa Connors Operational Defiant"
    #label var beh_rating_impulsive "Iowa Connors Impulsive"
    #label var beh_rating "Iowa Connors Overall"
    

def Reverse_Approach_Scale(data,app_map):
    '''
    Reverse coding management approaches scale 
    '''
    app_columns=[x for x in data.columns if x.startswith("app")]
    for x in app_columns:
        name_rc=x+'_rc'
        data[name_rc]=data[x].replace(app_map)
        

def Generate_App_Scale(data):
    '''
    function to generate positibe and negative app scale
    '''
    data['manage_app_negative']= data.loc[:,'app_coach_stu':'app_discp_refer'].mean(axis=1)
    data['manage_app_positive']=data.loc[:,'app_confer_stu':'app_beh_manage_teach'].mean(axis=1)
        
    