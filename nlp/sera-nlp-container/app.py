from flask import Flask
from flask import request, jsonify
# %%
#Standard Library Modules
import os
import re
import sys
from io import StringIO
#Related 3rd Party Modules
import pandas
import numpy

# #set current working directory to where this file is saved
# thisdir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(thisdir)
# # Add higher directory to python module's path
# sys.path.append("..") 

#Local Application Modules
import DocSim_class
import boto3

s3 = boto3.client(
    's3',
    # aws_access_key_id=ACCESS_KEY,
    # aws_secret_access_key=SECRET_KEY,
)

## Change before prod
LOCAL_DEV = False
def loadTextData(prefix,path):
    
    folder = f'{path}{prefix}'
    print(folder)
    try: 
        os.mkdir(folder) 
    except OSError as error: 
        print(error)  
    BUCKET = 'sera-nlp-raw-data'
    response = s3.list_objects(
            Bucket=BUCKET,
            Prefix = prefix,
            MaxKeys=100 )
    itemKeys = [item['Key'] for item in response['Contents'] if item['Key'] != prefix]  
    for i,itemKey in enumerate(itemKeys):
        s3.download_file(BUCKET,itemKey,f'{path}{itemKey}')


app = Flask(__name__)



@app.route('/nlp', methods=['GET'])
def index():
    inputFolders = request.args.get('inputFolders')
    if inputFolders is None:
        return jsonify({'status':'error'})
    try:
        inputFolders=inputFolders.split(',')
    except:
        return jsonify({'status':'error'})
    prefix = '/Users/taylorrohrich/Desktop/Taylor Rohrich/Code/MSDS_SERA_capstone/aws/nlp/tmp/' if LOCAL_DEV else '/tmp/'
    LINKING = 'linking_files_deidentified.csv'
    PERIOD_MODEL = "period_model.csv"
    SCRIPT_SKILLS = "script_skills.csv"
    METADATA = [LINKING,PERIOD_MODEL,SCRIPT_SKILLS]
    for filename in METADATA:
        s3.download_file('sera-nlp-metadata',filename,f'{prefix}{filename}')

   

    # %%
    ##########################################
    ## IDENTIFY AND OPEN SOURCE DIRECTORIES

    #base directory for file incorporation
    # folder containing .txt transcripts of coaching sessions
    # each transcript must identify speakers in form SPEAKER: 
    # each line of the document must include utterances of only 1 speaker
    for folder in inputFolders:
        loadTextData(folder, prefix)
        loadTextData(folder, prefix)
    print(prefix)
    text_process = DocSim_class.PreprocessCorpusText(prefix,
        recursive=True)
    #raw_text = DocSim_Function.get_src_txt(basedir)
    # %%
    # linking table including: 
    #   [id] of subject - matching transcript filename, 
    #   [skill] of focus - matching script,
    #   [period] semester_yyyy - matching transcript,
    #   [speaker] identifying coach in transcript text
    linking = prefix + "linking_files_deidentified.csv"
    linking = pandas.read_csv(linking, dtype=object)
    # period/model lookup table including: 
    #   [period] matching linking files and transcript,
    #   [model] "feedback" or "behavior" matching script
    period_model = prefix + "period_model.csv"
    period_model = pandas.read_csv(period_model, dtype=object)

    # script source table including: 
    #   [model] matching period_model file
    #   [skill] matching linking file
    #   [rawtext] text of script to be followed by coach in transcript
    script_skills = prefix + "script_skills.csv"
    script_skills = pandas.read_csv(script_skills, dtype=object)
    script_skills.filename = script_skills.filename.str.replace(".txt", "")

    # %%
    # ##########################################
    # ## PROCESS CONTENT FROM SOURCE DIRECTORIES

    # add model type to linking content
    linking = pandas.merge(linking, period_model, how="inner", on="period",
            left_index=False, right_index=False)


    # clean text from transcripts
    # clean = DocSim_Function.clean_text(raw_text)
    text_process = text_process.SERA_clean_text()
    # text_process = text_process.new_text_column("text")

    # transform to 1 row per combination of 
    # document and speaker
    text_process = text_process.group_by_speaker("speaker")

    # # combine corpus and linkages for clean output
    # transcripts = DocSim_Function.linkages_connection(stc, linking)

    text_process.df.filename = text_process.df.filename.str.replace(".txt", "")

    transcripts = pandas.merge(text_process.df, linking, how="inner", on=["filename", "period", "speaker"])

    # join transcripts with scripts
    # add [doctype] column to identify transcripts and scripts
    all_cols = ["filename", "study", "model", "skill", "coach", "text", 'doctype']
    transcripts['doctype'] = "transcript"
    transcripts = transcripts[all_cols]
    script_skills['doctype'] = "script"
    script_skills['coach'] = ""

    # make doctype first column, not last
    all_documents = transcripts.append(script_skills).reset_index()
    all_documents.head()
    # %%
    all_documents = all_documents[ ['doctype'] + \
        [ col for col in all_documents.columns if col != 'doctype' ] ]

    #REMOVE FEEDBACK FOR NOW, no transcripts to support it 
    all_documents = all_documents[all_documents['model'] == 'behavior']
    # %%
    # #all_documents.to_csv(bdir + r"\all_documents.csv", index=False)
    # # #calculate document similarity across all documents
    docsim_obj = DocSim_class.DocSim(all_documents, "skill", 
        "study", "doctype", "filename", "text")

    fill_words = ["uh", "um", "uhm", "just", "like", \
                            "yeah", "right", "okay",  \
                            "alright", "so", "mhmm"]
    # %%
    # Output Format 1
    output = docsim_obj.normal_comparison(method = "cosine",
                                        remove_stopwords = True,          
                                        filler_words = fill_words, 
                                        stem = False, 
                                        lemm = True,
                                        tfidf = True, 
                                        tfidf_level = "skill",
                                        lsa = True, 
                                        lsa_n_components = 100, 
                                        ngram = 1)

    #output.to_csv("normal_comparison_output_status.csv")
    csv_buffer = StringIO()
    output.to_csv(csv_buffer,index=False)
    s3_resource = boto3.resource('s3', 
    #    aws_access_key_id=ACCESS_KEY,
    # aws_secret_access_key=SECRET_KEY
    )
    s3_resource.Object('sera-nlp-parsed-data', "normal_comparison_output_status.csv").put(Body=csv_buffer.getvalue())

    # %%
    # Output Format 2
    output = docsim_obj.within_study_normal_average(method = "cosine",
                                        remove_stopwords = True,          
                                        filler_words = fill_words, 
                                        stem = False, 
                                        lemm = True,
                                        tfidf = True, 
                                        tfidf_level = "skill",
                                        lsa = True, 
                                        lsa_n_components = 100, 
                                        ngram = 1)

    #output.to_csv("within_study_normal_average_output_status.csv")
    csv_buffer = StringIO()
    output.to_csv(csv_buffer,index=False)
    s3_resource.Object('sera-nlp-parsed-data', "within_study_normal_average_output_status.csv").put(Body=csv_buffer.getvalue())
    return jsonify({'status':'complete'})

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)