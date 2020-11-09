from constants import COLUMN_NAME_MAP
import pandas as pd
import numpy as np

def cleanColumns(colnames):
    # Parse
    colParsed = pd.Series(colnames).str.lower().str.strip().str.replace('#','')
    mappedCols = colParsed.replace(COLUMN_NAME_MAP)
    return mappedCols

def generateScoreVariables(df,columns,mapDictionary):
    for column in columns:
        df[column] = df[column].replace(mapDictionary).astype(int)
    
    