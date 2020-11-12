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

def generateCalculatedColumns(df):
    for name,cols in CALCULATED_COLUMNS:
        print(len(cols))
        if len(cols)==1:
            df[name]=df[cols[0]]
        else:
            print(cols)
            df[name]=df[cols[0]] / df[cols[1]]
    
    
    