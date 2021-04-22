# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Query Page API

# %%
import pandas as pd
import numpy as np
import mysql.connector

# %% [markdown]
# ## Connect to Database

# %%
endpoint = "seratestdatabase.c4cjk1vto1om.us-east-2.rds.amazonaws.com"
port = "3306"
usr = "admin"
pswd = "seracapstone"
region = "us-east-2b"
dbname = "teachsim"


# %%
cnx = mysql.connector.connect(user=usr, password=pswd, host=endpoint, database=dbname)


# %%
cursor = cnx.cursor(buffered=True)


# %%
def showTable(tableName, cursor):
    query = "SELECT * FROM " + tableName + ";"
    cursor.execute(query)
    result = cursor.fetchall()
    colnames = [x[0] for x in cursor.description]
    df = pd.DataFrame(result, columns=colnames)
    return df


# %%
def execute(query, cursor):
    cursor.execute(query)
    result = cursor.fetchall()
    colnames = [x[0] for x in cursor.description]
    df = pd.DataFrame(result, columns=colnames)
    return df


# %%
showTable("Identifiers", cursor)


# %%
['Identifiers', 'Participant_Measures', 'Survey_Measures', 'Performance_Measures', 'Participant_Tracker']

# %% [markdown]
# ## Functions
# %% [markdown]
# ### Background Functions

# %%
#define a function to convert the result of the query into a pandas table
def output_table(query):
    result=pd.read_sql_query(query, con=cnx)
    return result          


# %%
def all_variables(cursor):
    query = """
SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Identifiers' 
OR TABLE_NAME = 'Participant_Measures'
OR TABLE_NAME = 'Survey_Measures'
OR TABLE_NAME = 'Performance_Measures'
OR TABLE_NAME = 'Participant_Tracker'
"""
    cursor.execute(query)
    result = cursor.fetchall()
    colnames = [x[0] for x in cursor.description]
    df = pd.DataFrame(result, columns=colnames)
    names = list(df['COLUMN_NAME'])
    return names
    


# %%
def numeric(cursor):
    query = """
SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Identifiers' 
OR TABLE_NAME = 'Participant_Measures'
OR TABLE_NAME = 'Survey_Measures'
OR TABLE_NAME = 'Performance_Measures'
OR TABLE_NAME = 'Participant_Tracker'
"""
    cursor.execute(query)
    result = cursor.fetchall()
    colnames = [x[0] for x in cursor.description]
    df = pd.DataFrame(result, columns=colnames)
    df2 = df[df['DATA_TYPE'] != b'varchar']
    names = list(df2['COLUMN_NAME'])
    return names


# %%
def text(cursor):
    query = """
SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Identifiers' 
OR TABLE_NAME = 'Participant_Measures'
OR TABLE_NAME = 'Survey_Measures'
OR TABLE_NAME = 'Performance_Measures'
OR TABLE_NAME = 'Participant_Tracker'
"""
    cursor.execute(query)
    result = cursor.fetchall()
    colnames = [x[0] for x in cursor.description]
    df = pd.DataFrame(result, columns=colnames)
    df2 = df[df['DATA_TYPE'] == b'varchar']
    names = list(df2['COLUMN_NAME'])
    return names


# %%
def table_variables(tableNames, cursor):
    if len(tableNames) == 0:
        return None
    query = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"
    query = query + tableNames[0] + "' "
    if len(tableNames) > 1:
        for table in tableNames[1:]:
            query = query + "OR TABLE_NAME = '" + table + "' "
    cursor.execute(query)
    result = cursor.fetchall()
    colnames = [x[0] for x in cursor.description]
    df = pd.DataFrame(result, columns=colnames)
    names = list(df['COLUMN_NAME'])
    
    return names


# %%
def convert_semester(time_list):
    converted_list = []
    if "Fall 2017" in time_list or "Spring 2018" in time_list:
        converted_list.append(1718)
    if "Fall 2018" in time_list or "Spring 2019" in time_list:
        converted_list.append(1819)
    if "Fall 2019" in time_list or "Spring 2020" in time_list:
        converted_list.append(1920)
    if "Fall 2020" in time_list or "Spring 2021" in time_list:
        converted_list.append(2021)
    return converted_list
        


# %%
def generate_mapping(cursor):
    survey = table_variables(['Survey_Measures'], cursor)
    performance = table_variables(['Performance_Measures'], cursor)
    identifiers = table_variables(['Identifiers'], cursor)
    mapping = {'Survey_Measures': {'baseline_post-survey': [x for x in survey if 'base_' in x], 
                                'big5': [x for x in survey if 'big5_' in x], 
                                'behavioral_redirections_post_Treatment': [x for x in survey if 'br_post_' in x], 
                                'behavioral_redirections_pre_treatment': [x for x in survey if 'br_pre_' in x], 
                                'exit_post_survey': [x for x in survey if 'exit_' in x], 
                                'feedback_post_treatment': [x for x in survey if 'fb_post_' in x], 
                                'feedback_pre_treatment': [x for x in survey if 'fb_pre_' in x], 
                                'haberman': [x for x in survey if 'haber_' in x]},
            'Performance_Measures': {'behavioral_redirections_baseline': [x for x in performance if 'br_base_' in x], 
                                    'behavioral_redirections_pre_treatment': [x for x in performance if 'br_pre_' in x], 
                                    'behavioral_redirections_post_treatment': [x for x in performance if 'br_post_' in x], 
                                    'behavioral_redirections_exit': [x for x in performance if 'br_exit_' in x], 
                                    'feedback_baseline': [x for x in performance if 'fb_base' in x], 
                                    'feedback_pre_treatment': [x for x in performance if 'fb_pre_' in x], 
                                    'feedback_post_treatment': [x for x in performance if 'fb_post' in x], 
                                    'feedback_exit': [x for x in performance if 'fb_exit_' in x]},
            'Identifiers': {'primary_treatment_condition': [x for x in identifiers if x == 'br_treat_cond'],
                           'mental_rehearsement_treatment_condition': [x for x in identifiers if x == 'br_treat_cond_mr'],
                           'iat_treatment_condition': [x for x in identifiers if x == 'br_treat_cond_iat'],
                           'university_email_address': [x for x in identifiers if x == 'email'],
                           'primary_treatment_condition for Feedback Simulation': [x for x in identifiers if x == 'fb_treat_cond'],
                           'original_treatment_condition_fall_2017': [x for x in identifiers if x == 'f17_treat_cond'],
                           'original_treatment_condition_spring_2018': [x for x in identifiers if x == 's18_treat_cond'],
                           'iat_treatment_condition_for_feedback_simulation': [x for x in identifiers if x == 'fb_treat_cond_iat'],
                           'participant_id': [x for x in identifiers if x == 'id_participant'],
                           'section_identifier': [x for x in identifiers if x == 'id_section'],
                           'site_identifier': [x for x in identifiers if x == 'id_site'],
                           'study_identifier': [x for x in identifiers if x == 'id_study'],
                           'year_identifier': [x for x in identifiers if x == 'id_year']}}
    return mapping

# %% [markdown]
# ### Second Level Functions

# %%
# this function takes the overall measures provided and the specific measures and returns 
# the relevant variables in a list
def get_variables(cursor, measure_list, specific_measure_list=None, field_type=None):
    
    # the first half returns the relevant variables mapped from measure_list and specific_measure_list
    cols = []
    mapping = generate_mapping(cursor)
    for measure in measure_list:
        if measure in mapping.keys():
            specific_checked = False
            for specific in specific_measure_list:
                if specific in mapping[measure].keys():
                    specific_checked = True
                    cols = cols + mapping[measure][specific]
            if specific_checked == False:
                table_cols = table_variables([measure], cursor)
                cols = cols + table_cols
        else:
            table_cols = table_variables([measure], cursor)
            cols = cols + table_cols
            
    cols = ['id_participant'] + cols
    cols = list(set(cols))
    
    # the second half filters based on the field type
    numbs = numeric(cursor)
    texts = text(cursor)
    
    if field_type == None or field_type == ['Numeric', 'Text'] or field_type == ['Text', 'Numeric']:
        cols = cols
    elif field_type == ['Numeric']:
        cols = [x for x in cols if x in numbs]
        cols = ['id_participant'] + cols
        cols = list(set(cols))
    elif field_type == ['Text']:
        cols = [x for x in cols if x in texts]
        cols = ['id_participant'] + cols
        cols = list(set(cols))
    
    return cols
    
    


# %%
def sub_query(time_list):
    # Build main portion
    # note that the id_participant column being renamed in Participant_Tracker require
    # that it be treated differently for joins and this will include that extra column
    query = "SELECT * FROM Identifiers LEFT JOIN Participant_Measures USING (id_participant) "
    query = query + "LEFT JOIN Survey_Measures USING (id_participant) "
    query = query + "LEFT JOIN Performance_Measures USING (id_participant) "
    query = query + "LEFT JOIN Participant_Tracker c ON id_participant = c.Participant_ID "
    
    # Add Where clause to filter based on time
    time = ""
    if time_list == None or 'All' in time_list or time_list == []:
        time = ""
    else:  
        time_list = convert_semester(time_list)
        time = time + "WHERE id_year in ("
        time = time + ", ".join(map(str,time_list))
        time = time + ")"
    
    query = query + time
    return query
    

# %% [markdown]
# ### Overall Function

# %%
def request(cursor, measure_list, time_list, specific_measure_list, field_type):
    query = "SELECT "
    sub = sub_query(time_list)
    measures = ['Identifiers', 'Participant_Measures', 'Survey_Measures', 'Performance_Measures', 'Participant_Tracker']
    cols = get_variables(cursor=cursor, measure_list=measures, specific_measure_list=specific_measure_list, field_type=field_type)
    for col in cols:
        query = query + "a." + col + ", "
    query = query[:-2] + " FROM ( " + sub + " ) a"
    
    return query
    

# %% [markdown]
# ## Test

# %%
measures = ['Identifiers', 'Participant_Measures', 'Survey_Measures', 'Performance_Measures', 'Participant_Tracker']
query = request(cursor, measure_list=measures, time_list=['All'], specific_measure_list=[], field_type=['Numeric', 'Text'])


# # %%
# sub = sub_query(['All'])
# sub


# # %%
print(execute(query, cursor))


# # %%


# # %% [markdown]
# # ## Close Database Connection

# # %%
# cnx.commit()
# cnx.close()


# # %%



