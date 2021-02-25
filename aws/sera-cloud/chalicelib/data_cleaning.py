import pandas as pd
import numpy as np

import os
from io import StringIO
from collections import defaultdict 
from chalicelib.constants import *
from chalicelib.utils import *
import boto3

## SET TO FALSE BEFORE UPLOADING
LOCAL_DEV = False
def data_cleaning():
    if LOCAL_DEV:
        os.chdir('/Users/taylorrohrich/Desktop/Taylor Rohrich/Code/MSDS_SERA_capstone/tmp')
    prefix = '' if LOCAL_DEV else '/tmp/'
    s3 = boto3.client('s3') 
    for name, val in FILENAMES.items():
        print(name)
        filename = val['name']
        print(f'{prefix}{filename}')
        obj = s3.get_object(Bucket= INPUT_BUCKET, Key= filename) 
        pd.read_csv(obj['Body']).to_csv(f'{prefix}{filename}', index=False)





    # ###### 01_cpp_clean.ipynb

    # crtse = pd.read_csv(prefix+ CRTSE)
    # crtse = basic(crtse)
    # crtse = new_col_mean(crtse, "crtse_total", first="crtse_05", last="crtse_41")

    # das = pd.read_csv(prefix +DAS)
    # das = basic(das)
    # das = new_col_mean(das, "das_depression", included=["das_03", "das_05", "das_10", "das_13", "das_16", "das_17", "das_21"])
    # das = new_col_mean(das, "das_anxiety", included=["das_02", "das_04", "das_07", "das_09", "das_15", "das_19", "das_20"])
    # das = new_col_mean(das, "das_stress", included=["das_01", "das_06", "das_08", "das_11", "das_12", "das_14", "das_18"])

    # demog = pd.read_csv(prefix +DEMOG)
    # demog = lower_skip(demog)

    # miss = pd.read_csv(prefix +MISS)
    # miss = lower_skip(miss)

    # demog_merged = append_data(demog, miss)
    # demog_merged = basic(demog_merged)
    # demog_merged = dates(demog_merged, "assessed")
    # demog_merged = demog_merged.query("student != 2176293 | assessed != '09162017'")

    # fit = pd.read_csv(prefix +FIT)
    # fit = basic(fit)
    # fit = new_col_mean(fit, "fit_total", first="fit_01", last="fit_13")

    # grit = pd.read_csv(prefix +GRIT)
    # grit = basic(grit)
    # grit = new_col_mean(grit, "grit_total", first="r_grit_02", last="r_grit_11")

    # imts = pd.read_csv(prefix +IMTS)
    # imts = basic(imts)
    # imts = new_col_mean(imts, "imts_total", first="imts_01", last="imts_05")

    # neo = pd.read_csv(prefix +NEO)
    # neo = lower_skip(neo)
    # neo = basic(neo)

    # contact = pd.read_csv(prefix +CONTACT)

    # neo_merged = neo.merge(contact, on='student', how='left')
    # neo_merged = neo_merged.drop(['name', 'universitycomputingid', 'studentacademicyr'], axis=1)

    # neo_2017 = pd.read_csv(prefix +NEO_2017)
    # neo_2017 = lower_skip(neo_2017)
    # neo_2017 = neo_2017.rename({"recipientemail":"email"}, axis=1)
    # neo_2017 = neo_2017.sort_values(by='recipientfirstname', ascending=True)

    # neo_2017_merged = neo_2017.merge(contact, on='email', how='outer')
    # neo_2017_merged = neo_2017_merged.drop(['name', 'universitycomputingid', 'studentacademicyr'], axis=1)
    # neo_2017_merged = basic(neo_2017_merged)

    # neo_2017_merged = destring(neo_2017_merged, first="neo_1", last="neo_60")

    # include = ["neo_1", "neo_3", "neo_8", "neo_9", "neo_12", "neo_14", "neo_15", "neo_16", "neo_18", "neo_23", \
    #         "neo_24", "neo_27", "neo_29", "neo_30", "neo_31", "neo_33", "neo_38", "neo_39", "neo_42", \
    #         "neo_44", "neo_45", "neo_46", "neo_48", "neo_54", "neo_55", "neo_57", "neo_59"]
    # neo_2017_merged = recode(neo_2017_merged, include)

    # neo_2017_merged = neo_2017_merged.rename({"r_neo_1": "r_neo_01",
    #                                         "neo_2": "neo_02",
    #                                         "r_neo_3": "r_neo_03",
    #                                         "neo_4": "neo_04",
    #                                         "neo_5": "neo_05",
    #                                         "neo_6": "neo_06",
    #                                         "neo_7": "neo_07",
    #                                         "r_neo_8": "r_neo_08",
    #                                         "r_neo_9": "r_neo_09"}, axis=1)

    # neo_2017_merged = neo_2017_merged.dropna(subset=['r_neo_01'])   

    # appended = append_data(neo_2017_merged, neo_merged)    
    # appended['Count'] = appended.groupby('student')['student'].transform('count')
    # appended = appended.query("Count==1 | email != '' ")     
    # appended = appended.drop(['Count'], axis=1)
    # appended = new_col_mean(appended, "neo_n", included=["r_neo_01", "neo_06", "neo_11", "r_neo_16", \
    #                                         "neo_21", "neo_26", "r_neo_31", "neo_36", "neo_41", \
    #                                         "r_neo_46", "neo_51", "neo_56"])    
    # appended = new_col_mean(appended, "neo_e", included=["neo_02", "neo_07", "r_neo_12", "neo_17", \
    #                                                 "neo_22", "r_neo_27", "neo_32", "neo_37", \
    #                                                 "r_neo_42", "neo_47", "neo_52", "r_neo_57"])
    # appended = new_col_mean(appended, "neo_o", included=["r_neo_03", "r_neo_08", "neo_13", "r_neo_18", \
    #                                                 "r_neo_23", "neo_28", "r_neo_33", "r_neo_38", \
    #                                                 "neo_43", "r_neo_48", "neo_53", "neo_58"])    
    # appended = new_col_mean(appended, "neo_a", included=["neo_04", "r_neo_09", "r_neo_14", "neo_19", \
    #                                                 "r_neo_24", "r_neo_29", "neo_34", "r_neo_39", \
    #                                                 "r_neo_44", "neo_49", "r_neo_54", "r_neo_59"])
    # appended = new_col_mean(appended, "neo_c", included=["neo_05", "neo_10", "r_neo_15", "neo_20", "neo_25", \
    #                                                 "r_neo_30", "neo_35", "neo_40", "r_neo_45", "neo_50", \
    #                                                 "r_neo_55", "neo_60"])

    # missing = pd.read_csv(prefix +MISSING)
    # missing.columns = missing.columns.str.lower()
    # missing = new_col_mean(missing, "neo_n", included=["r_neo_01", "neo_06", "neo_11", "r_neo_16", \
    #                                         "neo_21", "neo_26", "r_neo_31", "neo_36", "neo_41", \
    #                                         "r_neo_46", "neo_51", "neo_56"])
    # missing = new_col_mean(missing, "neo_e", included=["neo_02", "neo_07", "r_neo_12", "neo_17", \
    #                                                 "neo_22", "r_neo_27", "neo_32", "neo_37", \
    #                                                 "r_neo_42", "neo_47", "neo_52", "r_neo_57"])
    # missing = new_col_mean(missing, "neo_o", included=["r_neo_03", "r_neo_08", "neo_13", "r_neo_18", \
    #                                                 "r_neo_23", "neo_28", "r_neo_33", "r_neo_38", \
    #                                                 "neo_43", "r_neo_48", "neo_53", "neo_58"])
    # missing = new_col_mean(missing, "neo_a", included=["neo_04", "r_neo_09", "r_neo_14", "neo_19", \
    #                                                 "r_neo_24", "r_neo_29", "neo_34", "r_neo_39", \
    #                                                 "r_neo_44", "neo_49", "r_neo_54", "r_neo_59"])
    # missing = new_col_mean(missing, "neo_c", included=["neo_05", "neo_10", "r_neo_15", "neo_20", "neo_25", \
    #                                                 "r_neo_30", "neo_35", "neo_40", "r_neo_45", "neo_50", \
    #                                                 "r_neo_55", "neo_60"])
    # missing = missing.drop(['assessed', 'assessor'], axis=1)

    # final_neo = appended.merge(missing[['student', 'name', 'program', 'section']], on='student', how='outer')

    # rsq = pd.read_csv(prefix +RSQ)
    # rsq.columns = rsq.columns.str.lower()

    # rsq2 = pd.read_csv(prefix +RSQ2)
    # rsq2.columns = rsq2.columns.str.lower()

    # allRSQ = append_data(rsq2, rsq)
    # allRSQ.loc[allRSQ.name=="Gross,Hannah","student"] = 2603880
    # allRSQ = basic(allRSQ)
    # allRSQ = new_col_mean(allRSQ, "rsq_total", first="r_rsq_01", last="rsq_30")

    # tmas = pd.read_csv(prefix +TMAS)
    # tmas = basic(tmas)
    # tmas = new_col_mean(tmas, "tmas_total", first="tmas_01", last="r_tmas_20")

    # tse = pd.read_csv(prefix +TSE)
    # tse = basic(tse)
    # tse = new_col_mean(tse, "tses_se", included=["tse_01", "tse_02", "tse_04", "tse_06", "tse_09", "tse_12", "tse_14", "tse_22"])
    # tse = new_col_mean(tse, "tses_is", included=["tse_07", "tse_10", "tse_11", "tse_17", "tse_18", "tse_20", "tse_23", "tse_24"])
    # tse = new_col_mean(tse, "tses_cm", included=["tse_03", "tse_05", "tse_08", "tse_13", "tse_15", "tse_16", "tse_19", "tse_21"])
    # tse = new_col_mean(tse, "tses_total", included=["tse_01", "tse_02", "tse_04", "tse_06", "tse_09", "tse_12", \
    #                                             "tse_14", "tse_22", "tse_07", "tse_10", "tse_11", "tse_17", \
    #                                             "tse_18", "tse_20", "tse_23", "tse_24", "tse_03", "tse_05", \
    #                                             "tse_08", "tse_13", "tse_15", "tse_16", "tse_19", "tse_21"])

    # ytrt = pd.read_csv(prefix +YTRT)
    # ytrt = basic(ytrt)
    # ytrt = new_col_mean(ytrt, "ytrt_total", first="ytrt_01", last="ytrt_05")

    # full = ytrt[['student', 'ytrt_total', 'recipientlastname', 'recipientfirstname']]
    # full = full.merge(crtse[['student', 'crtse_total']], on='student', how='outer')
    # full = full.merge(das[['student', 'das_depression', 'das_anxiety', 'das_stress']], on='student', how='outer')
    # keep = list(demog_merged.loc[:, 'ccs_gpa':'hsach'].columns)
    # keep.append('student')
    # full = full.merge(demog_merged[keep], on='student', how='left')
    # full = full.merge(fit[['student', 'fit_total']], on='student', how='outer')
    # full = full.merge(grit[['student', 'grit_total']], on='student', how='outer')
    # full = full.merge(imts[['student', 'imts_total']], on='student', how='outer')
    # full = full.merge(final_neo[['student', 'neo_n', 'neo_e', 'neo_o', 'neo_a', 'neo_c']], on='student', how='left')
    # full = full.merge(allRSQ[['recipientlastname', 'recipientfirstname', 'rsq_total']], on=['recipientlastname', 'recipientfirstname'], how='left')
    # full = full.merge(tmas[['recipientlastname', 'recipientfirstname', 'tmas_total']], on=['recipientlastname', 'recipientfirstname'], how='outer')
    # full = full.merge(tse[['recipientlastname', 'recipientfirstname', 'tses_se', 'tses_is', 'tses_cm','tses_total']], on=['recipientlastname', 'recipientfirstname'], how='outer')
    # full['name'] = full['recipientlastname'] + "," + full['recipientfirstname']
    # full = full.sort_values(by=['recipientlastname'], ascending=True)

    # final = full.merge(contact[['student', 'email']], on='student', how='outer')
    # combo = {
    # '1382103':'set9x@virginia.edu',
    # '1498517':"sem4u@virginia.edu",
    # '2176293':"amh3ej@virginia.edu",
    # '2200476':"mih3f@virginia.edu",
    # '2437606':"ckb4y@virginia.edu",
    # '2468766':"npg7wf@virginia.edu",
    # '2498051':"hjk9dr@virginia.edu",
    # '2502859':"cjt4te@virginia.edu",
    # '2571818':"hwr9ex@virginia.edu",
    # '2605170':"rml3x@virginia.edu",
    # '2699159':"esw4au@virginia.edu",
    # '2699239':"rb2rf@virginia.edu",
    # '2699474':"smj6t@virginia.edu",
    # '2704548':"hw8kw@virginia.edu",
    # '2732302':"hlh9j@virginia.edu",
    # '2732372':"cml2zq@virginia.edu",
    # '2744059':"amh9gu@virginia.edu",
    # '2745617':"mca5hu@virginia.edu",
    # '2747552':"leo9um@virginia.edu",
    # '2760226':"ncb8q@virginia.edu",
    # '2761355':"joh2va@virginia.edu",
    # '2762920':"bfd8er@virginia.edu",
    # '2766444':"lck4hk@virginia.edu",
    # '2767343':"kno9b@virginia.edu",
    # '2767980':"oce7ph@virginia.edu",
    # '2772863':"es8fa@virginia.edu",
    # '2775384':"cc3vm@virginia.edu"
    # }
    # emails = pd.DataFrame({'student':list(combo.keys()), 'email':list(combo.values())})
    # #emails.to_csv("Student_Emails.csv")
    # final = replace_emails(final, emails)
    # final.loc[final.student==2502859,"email"]

    # final = destring(final, included=['age'])
    # replace_map = {
    #     2:1, 3:1, 4:1, 5:1, 1:0
    # }

    # final["age_21ab"] = final["age"].replace(replace_map)
    # final = col_missing_vals(final, "age_21ab")
    # replace_map1 = {1:1, 2:0, 3:0}
    # replace_map2 = {1:0, 2:1, 3:0}
    # replace_map3 = {1:0, 2:0, 3:1}
    # final['hsloc_1'] = final.hsloc.replace(replace_map1)
    # final['hsloc_2'] = final.hsloc.replace(replace_map2)
    # final['hsloc_3'] = final.hsloc.replace(replace_map3)
    # final['hsses_1'] = final.hsses.replace(replace_map1)
    # final['hsses_2'] = final.hsses.replace(replace_map2)
    # final['hsses_3'] = final.hsses.replace(replace_map3)
    # final['hsrace_1'] = final.hsrace.replace(replace_map1)
    # final['hsrace_2'] = final.hsrace.replace(replace_map2)
    # final['hsrace_3'] = final.hsrace.replace(replace_map3)
    # final['hsach_1'] = final.hsach.replace(replace_map1)
    # final['hsach_2'] = final.hsach.replace(replace_map2)
    # final['hsach_3'] = final.hsach.replace(replace_map3)
    # replace_map = {
    #     "2,5":2, "3,5":3
    # }
    # final.race = final.race.replace(replace_map)
    # final = destring(final, included=['race'])
    # replace_map = {5:1, 2:0, 3:0, 4:0, 1:0}
    # final["race_white"] = final.race.replace(replace_map)
    # final = col_missing_vals(final, "race_white")
    # final = destring(final, included=['hsses', 'hsach'])
    # final = col_missing_vals(final, "hsses")
    # final = col_missing_vals(final, "hsach")
    # final = destring(final, included=['partch'])
    # replace_map = {1:1, 2:1, 3:1, 4:0}
    # final["partch_either"] = final.partch.replace(replace_map)
    # final = destring(final, included=['moedu', 'faedu'])
    # replace_map = {3:1, 4:1, 5:1, 2:0, 1:0}
    # final["moedu_colab"] = final.moedu.replace(replace_map)
    # replace_map = {3:1, 4:1, 5:1, 2:0, 1:0}
    # final["faedu_colab"] = final.faedu.replace(replace_map)
    # final.gender = final.gender.str.strip().str.lower()
    # replace_map = {'female':1, 'woman':1, 'male':0, 'm':0}
    # final["gender_female"] = final.gender.replace(replace_map)
    # final = col_missing_vals(final, "gender_female")
    # replace_map = {"3.6??":"3.6"}
    # final["ccs_gpa"] = final.ccs_gpa.replace(replace_map)
    # final = destring(final, included=['ccs_gpa'])

    # rand = pd.read_csv(prefix +RANDOMIZATION)
    # rand = rand.rename({'Email':'email'}, axis=1).drop(['name'], axis=1)
    # full = final.merge(rand, on='id', how='outer')
    # partOne = full
    # full.to_csv('cpp.csv',index=False)
    ###### 02_sim_survey_clean

    def convert_cols(df):
        #rename the columns in all 2(survey) stata do file to intuitive column names
        df=df.rename({
                            'q1':'email',
                            'q4_1':'sim_fbsk',
                            'q5':'sim_txt_fbsk',
                            'q6_1':'sim_cmsk',
                            'q7':'sim_txt_cmsk',
                            'q8':'sim_txt_eth_behavior',
                            'q9':'sim_txt_eth_contribute',
                            'q10_1':'beh_fidgeting',
                            'q10_2':'beh_humming',
                            'q10_3':'beh_excitable',
                            'q10_4':'beh_inattentive',
                            'q10_5':'beh_short_attention',
                            'q10_6':'beh_quarrelsome',
                            'q10_7':'beh_acts_smart',
                            'q10_8':'beh_unpredictable',
                            'q10_9':'beh_defiant',
                            'q10_10':'beh_uncooperative',
                            'q10_11':'beh_easily_frustrated',
                            'q10_12':'beh_disturbs_others',
                            'q10_13':'beh_restless',
                            'q10_14':'beh_mood_changes',
                            'q11_1':'app_coach_stu',
                            'q12_1':'app_adjust_expect',
                            'q13_1':'app_guidance_couns',
                            'q14_1':'app_rec_sped',
                            'q15_1':'app_discp_refer',
                            'q16_1':'app_confer_stu',
                            'q17_1':'app_confer_parent',
                            'q18_1':'app_behavior_plan',
                            'q19_1':'app_challenge_work',
                            'q20_1':'app_spend_time',
                            'q21_1':'app_space_regroup',
                            'q22_1':'app_beh_manage_coach',
                            'q23_1':'app_beh_manage_teach',
                            'q24':'sim_txt_supports',
                            'q25_1':'sim_nervous',
                            'q25_2':'sim_beneficial',
                            'q25_3':'sim_worried_perform',
                            'q25_4':'sim_useful_tool',
                            'q25_5':'sim_relevant_studies',
                            'q25_6':'sim_relevant_prof',
                            'q25_7':'sim_like_use_again',
                            'q25_8':'sim_recommend',
                            'q25_9':'sim_sufficient_prep',
                            'q25_10':'sim_enough_time',
                            'q26':'sim_txt_beneficial',
                            'q27':'sim_txt_improve_exp',
                            'q28':'sim_txt_concerns' 
                        },axis=1)
        return df

    def clean_survey_data(data):
        data.columns = pd.Series(data.columns).str.lower().str.strip().str.replace('#','')
        #drop unnecessary observation
        data = data[data['q1'].notna()]
        #drop unnecessary variables
        unused_columns=['enddate', 'status', 'ipaddress', 'progress',
        'duration (in seconds)', 'finished', 'recordeddate', 'responseid',
        'recipientlastname', 'recipientfirstname', 'recipientemail',
        'externalreference', 'locationlatitude', 'locationlongitude',
        'distributionchannel', 'userlanguage']
        data=data.drop(columns=unused_columns)
        #rename the columns to intuitive names
        data=convert_cols(data)
        format_email(data)
        data=drop_duplicate(data)
        data=data.drop(columns=['startdate'])
        reverse_beh = {1:"Not at all", 2: "Just a little", 3: "Pretty much" ,4: "Very much"}
        reverse_sim = {5: "Strongly agree", 4:"Somewhat agree", 3: "Undecided", 2: "Somewhat disagree", 1: "Strongly disagree"}
        beh_map={"Not at all":1,  "Just a little":2,  "Pretty much":3 , "Very much":4}
        sim_map={"Strongly agree":5, "Somewhat agree":4, "Undecided":3, "Somewhat disagree":2, "Strongly disagree":1}
        app_map = {1:10, 2:9, 3:8,4:7,5:6,6:5,7:4,8:3,9:2,10:1}
        #convert columns to right data type
        convert_columns(data,beh_map,sim_map)
        convert_numeric(data)
        #generate Iowa Score Scaling
        generate_iowa_score_scale(data)
        #reverse the approcch scale
        reverse_approach_scale(data,app_map)
        #generate approach scale
        generate_app_scale(data)
        #convert the numeric columns back to categorical data
        convert_columns(data,reverse_beh,reverse_sim)
        
        return data

    def clean_redo_data(data):
        data.columns = pd.Series(data.columns).str.lower().str.strip().str.replace('#','')
        #drop unnecessary observation
        data = data[data['q1'].notna()]
        #drop unnecessary variables
        unused_columns=['enddate', 'status', 'ipaddress', 'progress',
        'duration (in seconds)', 'finished', 'recordeddate', 'responseid',
        'recipientlastname', 'recipientfirstname', 'recipientemail',
        'externalreference', 'locationlatitude', 'locationlongitude',
        'distributionchannel', 'userlanguage']
        data=data.drop(columns=unused_columns)
        #rename the columns to intuitive names
        data=convert_cols(data)
        format_email(data)
        data=drop_duplicate(data)
        data=data.drop(columns=['startdate'])
        reverse_beh = {1:"Not at all", 2: "Just a little", 3: "Pretty much" ,4: "Very much"}
        reverse_sim = {5: "Strongly agree", 4:"Somewhat agree", 3: "Undecided", 2: "Somewhat disagree", 1: "Strongly disagree"}
        beh_map={"Not at all":1,  "Just a little":2,  "Pretty much":3 , "Very much":4}
        sim_map={"Strongly agree":5, "Somewhat agree":4, "Undecided":3, "Somewhat disagree":2, "Strongly disagree":1}
        app_map = {1:10, 2:9, 3:8,4:7,5:6,6:5,7:4,8:3,9:2,10:1}
        #generate Iowa Score Scaling
        generate_iowa_score_scale(data)
        #reverse the approcch scale
        reverse_approach_scale(data,app_map)
        #generate approach scale
        generate_app_scale(data)
        #convert the numeric columns back to categorical data
        data.loc[:,'beh_fidgeting':'beh_mood_changes']=data.loc[:,'beh_fidgeting':'beh_mood_changes'].astype("int")
        data.loc[:,'beh_fidgeting':'beh_mood_changes']=data.loc[:,'beh_fidgeting':'beh_mood_changes'].replace(reverse_beh)
        
        
        return data

    data_2a = pd.read_csv(prefix +DATA_2A,skiprows=[1,2])
    data_2a=clean_survey_data(data_2a)
    data_2a['time']=0
    data_2a = data_2a.set_index('email')
    data_2a=data_2a.sort_values(by=['email'])
    data_2a.reset_index(inplace=True)
    #data_2a.to_csv("Summer2018_Baseline_Post-Survey_Cleaned.csv",index=False)
    data_2a.head(1)
    redo = pd.read_csv(prefix +REDO,skiprows=[1,2])
    redo=clean_redo_data(redo)
    redo['time']=0
    i = redo[((redo.email == 'kr2tvd@virginia.edu'))].index
    redo.at[i,'email']="krv2td@virginia.edu"
    #redo.to_csv("Summer2018_Baseline_Redos_Post-Survey_Cleaned.csv",index=False)
    redo = redo.set_index('email')
    data_2a = data_2a.set_index('email')
    data_2a.update(redo)
    data_2a=data_2a.sort_values(by=['email'])
    data_2a.reset_index(inplace=True)
    #data_2a.to_csv("Summer2018_Baseline_Post-Survey_Merged_Cleaned.csv",index=False)
    data_2b = pd.read_csv(prefix +DATA_2B,skiprows=[1,2])
    data_2b=clean_survey_data(data_2b)
    data_2b['time']=0
    data_2b = data_2b.set_index('email')
    data_2b=data_2b.sort_values(by=['email'])
    data_2b.reset_index(inplace=True)
    #data_2b.to_csv("Fall2018_Baseline_Post-Survey_Cleaned.csv",index=False)
    data_2c = pd.read_csv(prefix +DATA_2C,skiprows=[1,2])
    data_2c=clean_survey_data(data_2c)
    data_2c['time']=2
    i = data_2c[((data_2c.email == 'kr2a2fn@virginia.edu'))].index
    data_2c.at[i,'email']="kra2fn@virginia.edu"
    data_2c = data_2c.set_index('email')
    data_2c=data_2c.sort_values(by=['email'])
    data_2c.reset_index(inplace=True)
    #data_2c.to_csv("Spring2019_Coaching_Post-Survey_Cleaned.csv",index=False)
    data_2d = pd.read_csv(prefix +DATA_2D,skiprows=[1,2])
    data_2d=clean_survey_data(data_2d)
    data_2d['time']=3
    data_2d = data_2d.set_index('email')
    data_2d=data_2d.sort_values(by=['email'])
    data_2d.reset_index(inplace=True)
    #data_2d.to_csv("Spring2019_Exit_Post-Survey_Cleaned.csv",index=False)
    data_2d.head(1)
    full=data_2a.append(data_2b)
    full=full.append(data_2c)
    full=full.append(data_2d)
    full
    full.reset_index(inplace=True)
    full=full.drop(columns=['index'])
    exit_emails=["bsd7cv@virginia.edu","bh4fk@virginia.edu","alh8pk@virginia.edu","ahm4kv@virginia.edu"]
    for email in exit_emails:
        i = full[((full.email == email))].index
        full=full.drop(i)
    full = full.set_index('email')
    full=full.sort_values(by=['email'])
    full.reset_index(inplace=True)
    #full.to_csv("Fall2018Spring2019_Post-Survey_Cleaned.csv",index=False)
    randomization=pd.read_csv(prefix +RANDOMIZATION)
    randomization.columns = pd.Series(randomization.columns).str.lower().str.strip()
    randomization
    full=full.merge(randomization,left_on='email',right_on="email",how='inner')
    full
    cpp=pd.read_csv(prefix +CPP)
    cpp
    cols_to_use = list(cpp.columns.difference(full.columns)) + ['email']
    full=full.merge(cpp[cols_to_use],on='email',how='inner')
    full

    full=full.rename(columns = {'name_full':'name'})
    # full.drop('name_x', inplace=True, axis=1)
    # full.drop('name_y', inplace=True, axis=1)
    partTwo = full
    print(partTwo.columns)
    #full.to_csv('fulltest.csv',index=False)
    ###### Rest of 2?

    ###### 3.ipynb

    def performance_clean(csv_name,isExcel=False,sheet_name=None,sid=2,time=0):
        '''
        Base function that handles core cleaning of all of the part 3 files
        '''
        # Read data
        data=pd.read_csv(prefix +f"{csv_name}.csv",skiprows=[1,2])
        #data = pd.read_excel(f"{csv_name}.csv",sheet_name=sheet_name,skiprows=[1,2]) if isExcel else pd.read_csv(prefix +f"{csv_name}.csv",skiprows=[1,2])
        # Get cleaned column names
        data.columns = clean_columns(data.columns,csv_name == 'Fall 2018 Behavioral Redirections Baseline_July 24, 2019_14.06')
        # Set sid, time, vid
        # Construct vid column
        data['sid']=sid
        data['time']=time
        data['vid'] = data['id'].astype(str) + "_" + data['sid'].astype(str)
        # Generate duplicate column
        generate_duplicate_column(data)
        # Get score variables
        generate_score_variables(data)
        # Get Behavior columns
        generate_behavior_columns(data)
        # Get calculated columns
        generate_calculated_columns(data)
        #data = data.drop_duplicates(['id','time'],keep= 'first')
        return data
    def performance_clean_pt_1(csv_name,isExcel=False,sheet_name=None,time=0):
        '''
        3a just calls base function
        '''
        base = performance_clean(csv_name,isExcel,sheet_name,time)
        base['sid']=2
        base['time']=0
        if csv_name == 'Fall 2018 Behavioral Redirections Baseline_July 24, 2019_14.06':
            drop_cols_by_name(base,'q25','q8')
            drop_cols_by_name(base,'q20','q26')
        base = base.drop_duplicates(['id','time'],keep= 'first')
        return base
    data11= performance_clean_pt_1('2018_summer_baseline_br_perform',isExcel=True, sheet_name='Summer 2018 Behavioral Redirect')
    data12= performance_clean_pt_1('2018_fall_baseline_br_perform')
    data1 = data11.append(data12)
    def performance_clean_pt_2(csv_name,isExcel=False,sheet_name=None):
        '''
        3b cleaning
        '''
        # Get base
        base = performance_clean(csv_name,isExcel,sheet_name)
        # Drop specific column ranges
        drop_cols_by_name(base,'startdate','finished')
        drop_cols_by_name(base,'responseid','userlanguage')
        # Get coaching data
        coachingData = pd.read_csv(prefix +COACHING_DATA)[['id','coder_num','codingtype','cid','sid']]
        coachingData['id']=coachingData['id'].astype('int64')
        base['id'] = base['id'].astype('int64')
        # Merge coaching
        base['sid']=np.nan
        idCount = defaultdict(int)
        newSids = []
        for index, row in base.iterrows():
            rowId = row['id']

            rowSids = coachingData.loc[coachingData['id']==rowId,'sid'].values
            if len(rowSids) > idCount[rowId]:
                newSids.append(rowSids[idCount[rowId]])
                idCount[rowId]+=1
            else:
                newSids.append(np.nan)
            # row['sid']
        base['sid'] = newSids
        withCoaching = base
        # withCoaching = base.merge(coachingData,on=['id','cid'],how='left')
        # withCoaching['sid']=withCoaching['sid_y']
        # withCoaching.drop(columns=['sid_x','sid_y'])
        # #withCoaching = withCoaching.sort_values(by=['id','sid','cid'],)
        # withCoaching = withCoaching.drop_duplicates(['id','sid','cid'],keep='first')
        # Get tracker data
        trackerData = pd.read_csv(prefix +TRACKER_DATA)[['id_student','email','id_coach','id_interactor']].rename(columns={'id_student':'id'})
        #trackerData['id']=trackerData['id'].astype('int')
        #withCoaching['id']=withCoaching['id'].astype('int')
        # Merge tracking
        withTracking = withCoaching.merge(trackerData,on='id',how='inner') 
        withTracking['time']=np.where(withTracking['sid'] == 5, 1,2)
        withTracking= withTracking.drop_duplicates(['id','time'],keep= 'first')
        return withTracking
    data2=performance_clean_pt_2('2019_spring_coach_br_perform',isExcel=True, sheet_name='Sheet1')
    def performance_clean_pt_3(csv_name,isExcel=False,sheet_name=None):
        '''
        3c cleaning
        '''
        # Call base function
        base = performance_clean(csv_name,isExcel,sheet_name)
        base['time'] = 3
        base['sid'] = 8
        # Drop columns by name
        drop_cols_by_name(base,'startdate','finished')
        drop_cols_by_name(base,'responseid','userlanguage')
        drop_cols_by_name(base,'q12','q26')
        base = base.drop_duplicates(['id','time'],keep='last')
        return base
    data3=performance_clean_pt_3('2019_spring_exit_br_perform')
    partThree = data1.append([data2, data3])
    partThree['id']=partThree['id'].astype('str')
    randomization=pd.read_csv(prefix +RANDOMIZATION)
    randomization.columns = pd.Series(randomization.columns).str.lower().str.strip()
    randomization['id']=randomization['id'].astype('str')
    partThree = partThree.merge(randomization.loc[:,['id','email']],left_on='id',right_on="id",how='left')
    # partThree['email'] = np.where(partThree['email_x'] == "", )

    partThree['email'] = [email[0] if len(email[0]) else email[1] for email in zip(partThree['email_x'].fillna(''),partThree['email_y'].fillna(''))]
    partThree=partThree.loc[partThree['email'].str.len() > 0,:]
    ###### 4
    data1 = partThree
    data2 = partTwo
    #print(data2.columns)
    #data1.update(data2, overwrite=False)
    cols_to_use = list(data2.columns.difference(data1.columns)) + ['email','time']
    #print(cols_to_use)
    outcome_merged = pd.merge(data1, data2[cols_to_use], on=['email', 'time'], how='outer')
    #outcome_merged = outcome_merged[:371]
    def colMissingVals(df, columnList):
        ''' Generate a binary column that indicates whether the given column has a missing value.
        Provide the dataframe and the column of interest. The output will be the dataframe with one 
        additional column named {columnName}_miss that has a 1 for missing values in columnName
        and a 0 for a non-missing value in columnName.
        '''
        for columnName in columnList:
            newcol = columnName + "_miss"   # create a missing column name
            for i in range(len(df)):
                if columnName in df.columns:
                    df.loc[i, newcol] = [1 if pd.isnull(df.loc[i, columnName]) else 0]
        return df
    missing_cols_list = ["ccs_gpa", "partch_either", "moedu_colab", "faedu_colab", "gender_female", "race_white", 
                        "age_21ab", "hsses_1", "hsses_2", "hsses_3", "hsrace_1", "hsrace_2", "hsrace_3", "hsach_1", 
                        "hsach_2", "hsach_3", "hsloc_1", "hsloc_2", "hsloc_3"]
    colMissingVals(outcome_merged, missing_cols_list)
    missing_cols_list_2 = ["age_21ab", "race_white", "hsses_1", "hsses_2", "hsses_3", "hsach_1", "hsach_2",
                        "hsach_3", "partch_either", "moedu_colab", "faedu_colab", "gender_female"]
    for col in missing_cols_list_2:
        if col in outcome_merged.columns:
            outcome_merged[col] = outcome_merged[col].fillna(0)
    if "gender_female_miss" in outcome_merged.columns:
        outcome_merged["gender_female_miss"] = outcome_merged["gender_female_miss"].fillna(1)
    outcome_merged = outcome_merged.sort_values(by='email')
    if LOCAL_DEV:
            outcome_merged.to_csv('outcome_merged.csv',index=False)
    else:
        csv_buffer = StringIO()
        outcome_merged.to_csv(csv_buffer,index=False)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(OUTPUT_BUCKET, 'outcome_merged.csv').put(Body=csv_buffer.getvalue())





