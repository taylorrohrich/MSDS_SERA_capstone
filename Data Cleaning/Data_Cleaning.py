### Reusable Functions for Data Cleaning ###

import pandas as pd
import numpy as np

def append_data(df1, df2):
    ''' Appends the two dataframes given and returns the appended df.
    '''
    df_new = pd.concat([df1, df2], axis=0, ignore_index=True)
    return df_new

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


def col_missing_vals(df, columnName):
    ''' Generate a binary column that indicates whether the given column has a missing value.
    Provide the dataframe and the column of interest. The output will be the dataframe with one 
    additional column named {columnName}_miss that has a 1 for missing values in columnName
    and a 0 for a non-missing value in columnName.
    '''
    replace_map = {1:0, 2:0, 3:0, 0:0, np.NaN:1} # set the replacement schema
    newcol = columnName + "_miss" # generate the new column name
    df[newcol] = df[columnName].replace(replace_map) # make the new column
    return df


def dates(df, colname):
    ''' Makes the given column a string type with format mmddyyyy for easier querying.
    '''
    # make column the format mmddyyyy
    df[colname] = pd.to_datetime(df[colname], errors='ignore')
    df[colname] = df[colname].apply(lambda x: x.strftime('%m%d%Y'))
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

def drop_cols_by_name(df,start,end):
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

def drop_duplicate(data):
    '''
    function to drop duplicate observation
    data would be dataframe that need to check the duplicate
    '''
    #convert the startdate to datestamp()
    data['startdate']=pd.to_datetime(data.startdate)
    duplicated=data[data.duplicated(['email'],keep=False)]
    duplicated_email=pd.unique(duplicated['email'])
    column_n=len(data.columns)
    #for each duplicated email
    for email in duplicated_email:
        #find the observation contains duplicated email
        rows=duplicated.loc[duplicated['email'] == email]
        #count the na in the observation
        count_NA=rows.isnull().sum(axis=1).tolist()
        min_NA=min(count_NA)
        #if all duplicated observations have all information
        if sum(count_NA)==0:
            #drop the observation other the earliest start date
            drops=rows.loc[rows.startdate!=min(rows['startdate'])]
            email=drops['email']
            startdate=drops['startdate']
            i=data[((data.email == email) &( data.startdate == startdate))].index
            data=data.drop(i)
        #drop the observation with less missing value
        else:
            index=count_NA.index(min_NA)
            for i in range(len(count_NA)):
                if i != index:
                    a=rows.iloc[i,]
                    email=a.email
                    startdate=a.startdate
                    i=data[((data.email == email) &( data.startdate == startdate))].index
                    data=data.drop(i)
    return data

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


def generate_calculated_columns(df):
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


def lower_skip(df):
    ''' Makes the column names lowercase and deletes the first row of the dataframe.
    '''
    # clean column names
    df.columns = df.columns.str.lower().str.strip()
    # delete the first row
    df = df.iloc[1:,:]
    return df

def new_col_mean(df, name="RowMean", included=None, first=None, last=None):
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


def replace_emails(dataframe, csv):
    ''' Provide a dataframe and a csv name that has the first column of student ids and the second column 
    as the corresponding email address. This will replace the current email for that
    student with the one provided or simply add it if they have a missing email.
    '''
    replacements = pd.read_csv(csv)
    for index, row in replacements.iterrows():
        dataframe.loc[dataframe.student==int(row[1]), "email"] = row[2]
    return dataframe
