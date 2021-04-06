# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Generate Database 
# %% [markdown]
# This notebook serves to create the tables in the database for the TeachSim project. 

# %%
import pandas as pd
import numpy as np
import env

# %% [markdown]
# ## Connect to the Database

# %%
import mysql.connector


# %%
user= env.user
password= env.password
host = env.host
database = env.database

# %%
cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)


# %%
cursor = cnx.cursor(buffered=True)

# %% [markdown]
# ## Read in Data

# %%
import os
print(os.getcwd())


# %%
# os.chdir("/Users/jmachita03/Desktop/Capstone/RDS Set Up")

# %% [markdown]
# ### Identifiers

# %%
identifiers = pd.read_excel("TeachSIM Data Dictionary.xlsx", sheet_name="Identifiers")


# %%
identifiers = identifiers.drop(labels=3, axis=0)


# %%
identifiers

# %% [markdown]
# ### Participant Measures

# %%
participant = pd.read_excel("TeachSIM Data Dictionary.xlsx", sheet_name="Participant Measures")


# %%
participant = participant.drop(labels=0, axis=0)


# %%
participant

# %% [markdown]
# ### Survey Measures

# %%
survey = pd.read_excel("TeachSIM Data Dictionary.xlsx", sheet_name="Survey Measures")


# %%
survey["Values"] = survey["Values"].fillna("Missing")


# %%
survey

# %% [markdown]
# ### Performance Measures

# %%
performance = pd.read_excel("TeachSIM Data Dictionary.xlsx", sheet_name="Performance Measures")


# %%
descriptions = ["Behavior 1 reason for cut off", "Behavior 2 reason for cut off",                     "Behavior 3 reason for cut off", "Behavior 4 reason for cut off",                     "Behavior 5 reason for cut off", "Behavior 6 reason for cut off",                     "Description of teacher candidate's behavior; if double coded, this is the first populated response.",                     "Rational for quality score", "Rational for scoring", "Coder id", "Second coder id for double coded sessions"]


# %%
performance

# %% [markdown]
# ## Functions

# %%
def createTableQuery(all_column_list, char_col_list, tableName, primaryKeys):
    query = "CREATE TABLE " + tableName + " ("
    for col in all_column_list:
        if col in char_col_list:
            query = query + col + " varchar(100), "
        else:
            query = query + col + " float, "
    for key in primaryKeys:
        query = query + " PRIMARY KEY (" + key + "), "
    query = query[:-2] + " );"
    return query


# %%
def showTable(tableName, cursor):
    query = "SELECT * FROM " + tableName + ";"
    cursor.execute(query)
    result = cursor.fetchall()
    colnames = [x[0] for x in cursor.description]
    df = pd.DataFrame(result, columns=colnames)
    return df

# %% [markdown]
# ## Drop Tables 
# %% [markdown]
# Execute this query to recreate the empty tables if needed for demonstartion or testing purposes.

# %%
cursor.execute("DROP TABLE IF EXISTS Identifiers, Participant_Measures, Survey_Measures, Performance_Measures, Participant_Tracker;")

# %% [markdown]
# ## Create and Execute Queries
# %% [markdown]
# ### Identifiers

# %%
ids_column_list = list(identifiers['Variable'])


# %%
identifiers_char = ["id_site", "id_participant"]


# %%
id_query = createTableQuery(ids_column_list, identifiers_char, "Identifiers", ["id_participant"])


# %%
id_query


# %%
cursor.execute(id_query)

# %% [markdown]
# ### Participant Measures

# %%
part_column_list = ["id_participant"] + list(participant['Variable'])


# %%
participant_char = ["id_participant", "ccs_cohort", "ccs_major", "ccs_gpa", "raceother", "holangother", "hstypeother", "program"]


# %%
part_query = createTableQuery(part_column_list, participant_char, "Participant_Measures", ["id_participant"])


# %%
part_query


# %%
cursor.execute(part_query)

# %% [markdown]
# ### Survey Measures

# %%
surv_column_list = ["id_participant"] + list(survey['Variable'])


# %%
survey_char = list(survey[survey["Values"] == "Missing"]["Variable"]) + ["id_participant"]


# %%
survey_char = survey_char + ["fb_post_sim_first_sort_did", "fb_post_sim_first_sort_didnt", "fb_post_sim_sec_sort_did", "fb_post_sim_sec_sort_didnt"]


# %%
surv_query = createTableQuery(surv_column_list, survey_char, "Survey_Measures", ["id_participant"])


# %%
surv_query


# %%
cursor.execute(surv_query)

# %% [markdown]
# ### Performance Measures

# %%
perf_column_list = ["id_participant"] + list(performance['Variable'])


# %%
performance_char = list(pd.DataFrame(performance[performance["Description"].isin(descriptions)])["Variable"]) + ["id_participant"]


# %%
perf_query = createTableQuery(perf_column_list, performance_char, "Performance_Measures", ["id_participant"])


# %%
perf_query


# %%
cursor.execute(perf_query)

# %% [markdown]
# ## Testing
# %% [markdown]
# ### Add Fake Data to Identifiers

# %%
data = pd.read_csv("id_data.csv")


# %%
data


# %%
cols = ",".join([str(i) for i in data.columns.tolist()])


# %%
for i,row in data.iterrows():
    sql = "INSERT INTO Identifiers (" + cols + ") VALUES " + str(tuple(row)) + ";"
    cursor.execute(sql)

# %% [markdown]
# ### Show Data in a Table

# %%
showTable("Identifiers", cursor)


# %%
showTable("Survey_Measures", cursor)

# %% [markdown]
# ### Clear All Data from Table

# %%
cursor.execute("DELETE FROM Identifiers;")


# %%
showTable("Identifiers", cursor)

# %% [markdown]
# ## Close Database Connection

# %%

# %%
names = {"Participant_Information_Survey": ["2018_2019_participant_measures.csv"],
        "Baseline_Survey": ["2018_summer_baseline_postsim_survey.csv", "2018_fall_baseline_postsim_survey.csv"],
        "Classroom_Norms_Post_Sim_Survey": ["2019_spring_precoach_br_postsim_survey.csv"],
        "Exit_Survey": ["2019_spring_ exit_postsim_survey.csv"],
        "Classroom_Norms_Coding_Baseline": ["2018_summer_baseline_br_perform.csv", "2018_fall_baseline_br_perform.csv"],
        "Classroom_Norms_Coding_Precoach": ["2019_spring_coach_br_perform.csv"],
        "Classroom_Norms_Coding_Postcoach": ["2019_spring_coach_br_perform.csv"],
        "Classroom_Norms_Coding_Exit": ["2019_spring_exit_br_perform.csv"]}


# %%
all_csvs = []
for item in list(names.values()):
    all_csvs = all_csvs + item
all_csvs

# %% [markdown]
# ## Create Table in Database



# %%
cols = ["Participant_ID"] + list(names.keys())
cols


# %%
query = "CREATE TABLE Participant_Tracker ("
for col in cols:
    query = query + col + " varchar(100), "
query = query + "PRIMARY KEY (Participant_ID) );"


# %%
query


# %%
cursor.execute(query)
cnx.commit()
cnx.close()


# %%



