import pandas as pd
import numpy as np
from utils import *
import os
os.chdir('/Users/taylorrohrich/Desktop/Taylor Rohrich/Code/MSDS_SERA_capstone/data')
###### 01_cpp_clean.ipynb

crtse = pd.read_excel("2018_2019_CRTSE_SummerSecondary_PGMT_4thyrBMT_ItemsRemoved.xls", sheet_name='Sheet1')
crtse = basic(crtse)
crtse = new_col_mean(crtse, "crtse_total", first="crtse_05", last="crtse_41")

das = pd.read_excel("2018_2019_DAS_SummerSecondary_PGMT_4thyrBMT_Recoded_Missing_ItemNamesRemoved.xls", sheet_name='Sheet1')
das = basic(das)
das = new_col_mean(das, "das_depression", included=["das_03", "das_05", "das_10", "das_13", "das_16", "das_17", "das_21"])
das = new_col_mean(das, "das_anxiety", included=["das_02", "das_04", "das_07", "das_09", "das_15", "das_19", "das_20"])
das = new_col_mean(das, "das_stress", included=["das_01", "das_06", "das_08", "das_11", "das_12", "das_14", "das_18"])

demog = pd.read_excel("2018_2019_Demography_Survey_SummerSecondary_PGMT.xls", sheet_name="Sheet1")
demog = lower_skip(demog)

miss = pd.read_excel("2017_2018_CCS1_DemographySurvey_NumID_NoConsentRemoved.xlsx",engine='openpyxl')
miss = lower_skip(miss)

demog_merged = append_data(demog, miss)
demog_merged = basic(demog_merged)
demog_merged = dates(demog_merged, "assessed")
demog_merged = demog_merged.query("student != 2176293 | assessed != '09162017'")

fit = pd.read_excel("2018_2019_FIT_SummerSecondary_PGMT_4thyrBMT_Recoded_ItemNamesRemoved.xls", sheet_name="Sheet1")
fit = basic(fit)
fit = new_col_mean(fit, "fit_total", first="fit_01", last="fit_13")

grit = pd.read_excel("2018_2019_GRIT_SummerSecondary_PGMT_4thyrBMT_ReverseCoded_OrigRemoved.xls", sheet_name="Sheet1")
grit = basic(grit)
grit = new_col_mean(grit, "grit_total", first="r_grit_02", last="r_grit_11")

imts = pd.read_excel("2018_2019_IMTS_SummerSecondary_PGMT_4thyrBMT_Missing_ItemNamesRemoved.xls", sheet_name="Sheet1")
imts = basic(imts)
imts = new_col_mean(imts, "imts_total", first="imts_01", last="imts_05")

neo = pd.read_excel("2018_2019_NEO_SummerSecondary_PGMT_ReverseCoded_OrigRemoved.xls", sheet_name="Sheet1")
neo = lower_skip(neo)
neo = basic(neo)

contact = pd.read_excel("Student_Contact_2018_2019.xls")

neo_merged = neo.merge(contact, on='student', how='left')
neo_merged = neo_merged.drop(['name', 'universitycomputingid', 'studentacademicyr'], axis=1)

neo_2017 = pd.read_excel("NEO 2017 09 27.xlsx")
neo_2017 = lower_skip(neo_2017)
neo_2017 = neo_2017.rename({"recipientemail":"email"}, axis=1)
neo_2017 = neo_2017.sort_values(by='recipientfirstname', ascending=True)

neo_2017_merged = neo_2017.merge(contact, on='email', how='outer')
neo_2017_merged = neo_2017_merged.drop(['name', 'universitycomputingid', 'studentacademicyr'], axis=1)
neo_2017_merged = basic(neo_2017_merged)

neo_2017_merged = destring(neo_2017_merged, first="neo_1", last="neo_60")

include = ["neo_1", "neo_3", "neo_8", "neo_9", "neo_12", "neo_14", "neo_15", "neo_16", "neo_18", "neo_23", \
           "neo_24", "neo_27", "neo_29", "neo_30", "neo_31", "neo_33", "neo_38", "neo_39", "neo_42", \
           "neo_44", "neo_45", "neo_46", "neo_48", "neo_54", "neo_55", "neo_57", "neo_59"]
neo_2017_merged = recode(neo_2017_merged, include)

neo_2017_merged = neo_2017_merged.rename({"r_neo_1": "r_neo_01",
                                         "neo_2": "neo_02",
                                         "r_neo_3": "r_neo_03",
                                         "neo_4": "neo_04",
                                         "neo_5": "neo_05",
                                         "neo_6": "neo_06",
                                         "neo_7": "neo_07",
                                         "r_neo_8": "r_neo_08",
                                         "r_neo_9": "r_neo_09"}, axis=1)

neo_2017_merged = neo_2017_merged.dropna(subset=['r_neo_01'])   

appended = append_data(neo_2017_merged, neo_merged)    
appended['Count'] = appended.groupby('student')['student'].transform('count')
appended = appended.query("Count==1 | email != '' ")     
appended = appended.drop(['Count'], axis=1)
appended = new_col_mean(appended, "neo_n", included=["r_neo_01", "neo_06", "neo_11", "r_neo_16", \
                                          "neo_21", "neo_26", "r_neo_31", "neo_36", "neo_41", \
                                          "r_neo_46", "neo_51", "neo_56"])    
appended = new_col_mean(appended, "neo_e", included=["neo_02", "neo_07", "r_neo_12", "neo_17", \
                                                   "neo_22", "r_neo_27", "neo_32", "neo_37", \
                                                   "r_neo_42", "neo_47", "neo_52", "r_neo_57"])
appended = new_col_mean(appended, "neo_o", included=["r_neo_03", "r_neo_08", "neo_13", "r_neo_18", \
                                                   "r_neo_23", "neo_28", "r_neo_33", "r_neo_38", \
                                                   "neo_43", "r_neo_48", "neo_53", "neo_58"])    
appended = new_col_mean(appended, "neo_a", included=["neo_04", "r_neo_09", "r_neo_14", "neo_19", \
                                                   "r_neo_24", "r_neo_29", "neo_34", "r_neo_39", \
                                                   "r_neo_44", "neo_49", "r_neo_54", "r_neo_59"])
appended = new_col_mean(appended, "neo_c", included=["neo_05", "neo_10", "r_neo_15", "neo_20", "neo_25", \
                                                   "r_neo_30", "neo_35", "neo_40", "r_neo_45", "neo_50", \
                                                   "r_neo_55", "neo_60"])

missing = pd.read_excel("2018_2019_NEO_Missing.xls")
missing.columns = missing.columns.str.lower()
missing = new_col_mean(missing, "neo_n", included=["r_neo_01", "neo_06", "neo_11", "r_neo_16", \
                                          "neo_21", "neo_26", "r_neo_31", "neo_36", "neo_41", \
                                          "r_neo_46", "neo_51", "neo_56"])
missing = new_col_mean(missing, "neo_e", included=["neo_02", "neo_07", "r_neo_12", "neo_17", \
                                                   "neo_22", "r_neo_27", "neo_32", "neo_37", \
                                                   "r_neo_42", "neo_47", "neo_52", "r_neo_57"])
missing = new_col_mean(missing, "neo_o", included=["r_neo_03", "r_neo_08", "neo_13", "r_neo_18", \
                                                   "r_neo_23", "neo_28", "r_neo_33", "r_neo_38", \
                                                   "neo_43", "r_neo_48", "neo_53", "neo_58"])
missing = new_col_mean(missing, "neo_a", included=["neo_04", "r_neo_09", "r_neo_14", "neo_19", \
                                                   "r_neo_24", "r_neo_29", "neo_34", "r_neo_39", \
                                                   "r_neo_44", "neo_49", "r_neo_54", "r_neo_59"])
missing = new_col_mean(missing, "neo_c", included=["neo_05", "neo_10", "r_neo_15", "neo_20", "neo_25", \
                                                   "r_neo_30", "neo_35", "neo_40", "r_neo_45", "neo_50", \
                                                   "r_neo_55", "neo_60"])
missing = missing.drop(['assessed', 'assessor'], axis=1)

final_neo = appended.merge(missing[['student', 'name', 'program', 'section']], on='student', how='outer')

rsq = pd.read_excel("2018_2019_RSQ_SummerSecondary_PGMT_ReverseCoded_OrigRemoved.xls", sheet_name="Sheet1")
rsq.columns = rsq.columns.str.lower()

rsq2 = pd.read_excel("2018_2019_RSQ_Missing.xlsx")
rsq2.columns = rsq2.columns.str.lower()

allRSQ = append_data(rsq2, rsq)
allRSQ.loc[allRSQ.name=="Gross,Hannah","student"] = 2603880
allRSQ = basic(allRSQ)
allRSQ = new_col_mean(allRSQ, "rsq_total", first="r_rsq_01", last="rsq_30")

tmas = pd.read_excel("2018_2019_TMAS_SummerSecondary_PGMT_4thyrBMT_Missing_ReverseCoded_OrigRemoved_ItemNamesRemoved.xls", sheet_name="Sheet1")
tmas = basic(tmas)
tmas = new_col_mean(tmas, "tmas_total", first="tmas_01", last="r_tmas_20")

tse = pd.read_excel("2018_2019_TSE_SummerSecondary_PGMT_4thyrBMT.xls", sheet_name="Sheet1")
tse = basic(tse)
tse = new_col_mean(tse, "tses_se", included=["tse_01", "tse_02", "tse_04", "tse_06", "tse_09", "tse_12", "tse_14", "tse_22"])
tse = new_col_mean(tse, "tses_is", included=["tse_07", "tse_10", "tse_11", "tse_17", "tse_18", "tse_20", "tse_23", "tse_24"])
tse = new_col_mean(tse, "tses_cm", included=["tse_03", "tse_05", "tse_08", "tse_13", "tse_15", "tse_16", "tse_19", "tse_21"])
tse = new_col_mean(tse, "tses_total", included=["tse_01", "tse_02", "tse_04", "tse_06", "tse_09", "tse_12", \
                                              "tse_14", "tse_22", "tse_07", "tse_10", "tse_11", "tse_17", \
                                              "tse_18", "tse_20", "tse_23", "tse_24", "tse_03", "tse_05", \
                                              "tse_08", "tse_13", "tse_15", "tse_16", "tse_19", "tse_21"])

ytrt = pd.read_excel("2018_2019_YTRT_SummerSecondary_PGMT_4thyrBMT_Missing_ItemNamesRemoved.xls", sheet_name="Sheet1")
ytrt = basic(ytrt)
ytrt = new_col_mean(ytrt, "ytrt_total", first="ytrt_01", last="ytrt_05")

full = ytrt[['student', 'ytrt_total', 'recipientlastname', 'recipientfirstname']]
full = full.merge(crtse[['student', 'crtse_total']], on='student', how='outer')
full = full.merge(das[['student', 'das_depression', 'das_anxiety', 'das_stress']], on='student', how='outer')
keep = list(demog_merged.loc[:, 'ccs_gpa':'hsach'].columns)
keep.append('student')
full = full.merge(demog_merged[keep], on='student', how='left')
full = full.merge(fit[['student', 'fit_total']], on='student', how='outer')
full = full.merge(grit[['student', 'grit_total']], on='student', how='outer')
full = full.merge(imts[['student', 'imts_total']], on='student', how='outer')
full = full.merge(final_neo[['student', 'neo_n', 'neo_e', 'neo_o', 'neo_a', 'neo_c']], on='student', how='left')
full = full.merge(allRSQ[['recipientlastname', 'recipientfirstname', 'rsq_total']], on=['recipientlastname', 'recipientfirstname'], how='left')
full = full.merge(tmas[['recipientlastname', 'recipientfirstname', 'tmas_total']], on=['recipientlastname', 'recipientfirstname'], how='outer')
full = full.merge(tse[['recipientlastname', 'recipientfirstname', 'tses_se', 'tses_is', 'tses_cm','tses_total']], on=['recipientlastname', 'recipientfirstname'], how='outer')
full['name'] = full['recipientlastname'] + "," + full['recipientfirstname']
full = full.sort_values(by=['recipientlastname'], ascending=True)

final = full.merge(contact[['student', 'email']], on='student', how='outer')
combo = {
'1382103':'set9x@virginia.edu',
'1498517':"sem4u@virginia.edu",
'2176293':"amh3ej@virginia.edu",
'2200476':"mih3f@virginia.edu",
'2437606':"ckb4y@virginia.edu",
'2468766':"npg7wf@virginia.edu",
'2498051':"hjk9dr@virginia.edu",
'2502859':"cjt4te@virginia.edu",
'2571818':"hwr9ex@virginia.edu",
'2605170':"rml3x@virginia.edu",
'2699159':"esw4au@virginia.edu",
'2699239':"rb2rf@virginia.edu",
'2699474':"smj6t@virginia.edu",
'2704548':"hw8kw@virginia.edu",
'2732302':"hlh9j@virginia.edu",
'2732372':"cml2zq@virginia.edu",
'2744059':"amh9gu@virginia.edu",
'2745617':"mca5hu@virginia.edu",
'2747552':"leo9um@virginia.edu",
'2760226':"ncb8q@virginia.edu",
'2761355':"joh2va@virginia.edu",
'2762920':"bfd8er@virginia.edu",
'2766444':"lck4hk@virginia.edu",
'2767343':"kno9b@virginia.edu",
'2767980':"oce7ph@virginia.edu",
'2772863':"es8fa@virginia.edu",
'2775384':"cc3vm@virginia.edu"
}
emails = pd.DataFrame({'student':list(combo.keys()), 'email':list(combo.values())})
emails.to_csv("Student_Emails.csv")
final = replace_emails(final, "Student_Emails.csv")
final.loc[final.student==2502859,"email"]

final = destring(final, included=['age'])
replace_map = {
    2:1, 3:1, 4:1, 5:1, 1:0
}

final["age_21ab"] = final["age"].replace(replace_map)
final = col_missing_vals(final, "age_21ab")
replace_map1 = {1:1, 2:0, 3:0}
replace_map2 = {1:0, 2:1, 3:0}
replace_map3 = {1:0, 2:0, 3:1}
final['hsloc_1'] = final.hsloc.replace(replace_map1)
final['hsloc_2'] = final.hsloc.replace(replace_map2)
final['hsloc_3'] = final.hsloc.replace(replace_map3)
final['hsses_1'] = final.hsses.replace(replace_map1)
final['hsses_2'] = final.hsses.replace(replace_map2)
final['hsses_3'] = final.hsses.replace(replace_map3)
final['hsrace_1'] = final.hsrace.replace(replace_map1)
final['hsrace_2'] = final.hsrace.replace(replace_map2)
final['hsrace_3'] = final.hsrace.replace(replace_map3)
final['hsach_1'] = final.hsach.replace(replace_map1)
final['hsach_2'] = final.hsach.replace(replace_map2)
final['hsach_3'] = final.hsach.replace(replace_map3)
replace_map = {
    "2,5":2, "3,5":3
}
final.race = final.race.replace(replace_map)
final = destring(final, included=['race'])
replace_map = {5:1, 2:0, 3:0, 4:0, 1:0}
final["race_white"] = final.race.replace(replace_map)
final = col_missing_vals(final, "race_white")
final = destring(final, included=['hsses', 'hsach'])
final = col_missing_vals(final, "hsses")
final = col_missing_vals(final, "hsach")
final = destring(final, included=['partch'])
replace_map = {1:1, 2:1, 3:1, 4:0}
final["partch_either"] = final.partch.replace(replace_map)
final = destring(final, included=['moedu', 'faedu'])
replace_map = {3:1, 4:1, 5:1, 2:0, 1:0}
final["moedu_colab"] = final.moedu.replace(replace_map)
replace_map = {3:1, 4:1, 5:1, 2:0, 1:0}
final["faedu_colab"] = final.faedu.replace(replace_map)
final.gender = final.gender.str.strip().str.lower()
replace_map = {'female':1, 'woman':1, 'male':0, 'm':0}
final["gender_female"] = final.gender.replace(replace_map)
final = col_missing_vals(final, "gender_female")
replace_map = {"3.6??":"3.6"}
final["ccs_gpa"] = final.ccs_gpa.replace(replace_map)
final = destring(final, included=['ccs_gpa'])

rand = pd.read_excel("SimTeacher Randomization Fall 2018 Spring 2019.xls")
rand = rand.rename({'Email':'email'}, axis=1).drop(['name'], axis=1)
full = final.merge(rand, on='email', how='outer')

full.to_csv('output_01_cpp_clean.csv')

######


