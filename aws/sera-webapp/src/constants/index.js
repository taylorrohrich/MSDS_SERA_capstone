import {API_ENDPOINT} from './env'
const TRACKER_COLUMNS=['Participant_ID','Participant_Information_Survey','Baseline_Survey','Classroom_Norms_Coding_Baseline','Classroom_Norms_Coding_Precoach','Classroom_Norms_Coding_Postcoach','Classroom_Norms_Coding_Exit','Classroom_Norms_Post_Sim_Survey','Exit_Survey']
const ROUTES={NLP: {path:'/nlp', parameters:['filename']},JSON:{path:"/json",parameters:['time_list','measure_list','group_list','specific_measure_list','field_type_list']},CSV:{path:"/csv",parameters:['time_list','measure_list','group_list','specific_measure_list','field_type_list']},TRACKER:{path:'/tracker',parameters:[]}}
const QUERY_FIELDS=[
    {type: 'time_list', label: 'Time',values :['All','Spring 2018','Fall 2018','Spring 2019','Fall 2019']},
    {type: 'measure_list',label: 'Measure',values :['Identifiers','Participant_Measures','Survey_Measures','Performance_Measures']},
    // {type: 'group_list',label: 'Group List',values :['a','b','c','d','e']},
    {type: 'field_type_list',label:'Field Type',values :['Numeric','Text']},
    {type: 'specific_identifier',label: 'Specific Identifier ',values:['primary_treatment_condition','mental_rehearsement_treatment_condition', 'iat_treatment_condition', 'university_email_address', 'primary_treatment_condition for Feedback Simulation', 'original_treatment_condition_fall_2017', 'original_treatment_condition_spring_2018', 'iat_treatment_condition_for_feedback_simulation', 'participant_id', 'section_identifier', 'site_identifier', 'study_identifier', 'year_identifier'], labels:['Primary Treatment Condition','Mental Rehearsement Treatment Condition','IAT Treatment Condition','University Email Address','Primary Treatment Condition for Feedback Simulation','Original Treatment Condition Fall 2017','Original Treatment Condition Spring 2018','IAT Treatment Condition for Feedback Simulation','Participant Id','Section Identifier','Site Identifier','Study Identifier','Year Identifier'] },
    {type: 'specific_survey',label:'Specific Survey',values: ['participant_survey_measures','Baseline_post-survey','big5', 'behavioral_redirections_post_treatment', 'behavioral_redirections_pre_treatment', 'exit_post_survey',  'feedback_post_treatment', 'feedback_pre_treatment' , 'haberman'], labels: [ 'Participant Survey Measures','Baseline Post-Survey','Big5', 'Behavioral Redirections Post Treatment', 'Behavioral Redirections Pre Treatment', 'Exit Post Survey',  'Feedback Post Treatment',    'Feedback Pre Treatment' , 'Haberman']},
    {type: 'specific_performance',label: 'Specific Performance',values :['behavioral_redirections_baseline','behavioral_redirections_pre_treatment', 'behavioral_redirections_post_treatment','behavioral_redirections_exit','feedback_baseline','feedback_pre_treatment','feedback_post_treatment','feedback_exit'],labels :['Behavioral Redirections Baseline','Behavioral Redirections Pre Treatment', 'Behavioral Redirections Post Treatment','Behavioral Redirections Exit','Feedback Baseline','Feedback Pre Treatment','Feedback Post Treatment','Feedback Exit']},
]

export {QUERY_FIELDS,API_ENDPOINT,ROUTES,TRACKER_COLUMNS}
