const API_ENDPOINT = 'https://nzjj6m9o33.execute-api.us-east-1.amazonaws.com/api'
const TRACKER_COLUMNS=['Participant_ID','Participant_Information_Survey','Baseline_Survey','Classroom_Norms_Coding_Baseline','Classroom_Norms_Coding_Precoach','Classroom_Norms_Coding_Postcoach','Classroom_Norms_Coding_Exit','Classroom_Norms_Post_Sim_Survey','Exit_Survey']
const ROUTES={JSON:{path:"/json",parameters:['time_list','measure_list','group_list','specific_measure_list','field_type_list']},CSV:{path:"/csv",parameters:['time_list','measure_list','group_list','specific_measure_list','field_type_list']},TRACKER:{path:'/tracker',parameters:[]}}
const QUERY_FIELDS=[
    {type: 'time_list', label: 'Time List',values :['All','Spring 2018','Fall 2018','Spring 2019','Fall 2019']},
    {type: 'measure_list',label: 'Measure List',values :['Identifiers','Participant Measures','Survey Measures','Performance Measures']},
    // {type: 'group_list',label: 'Group List',values :['a','b','c','d','e']},
    {type: 'field_type_list',label:'Field Type List',values :['Numeric','Text']},
    {type: 'specific_identifier',label: 'Specific Identifier List',values :['br_treat_cond','br_treat_cond_mr', 'br_treat_cond_iat', 'email', 'fb_treat_cond', 'f17_treat_cond', 's18_treat_cond', 'fb_treat_cond_iat', 'id_participant', 'id_section', 'id_site', 'id_study', 'id_year']},
    {type: 'specific_participant',label: 'Specific Participant List',values :['ccs_cohort','ccs_stutype', 'ccs_major', 'ccs_majother', 'ccs_gpa', 'partch', 'moedu', 'faedu', 'gender', 'age', 'race', 'raceother', 'holang', 'holangother', 'hstype', 'hstypeother', 'hsloc', 'hsses', 'hsrace', 'hsach', 'fustuses', 'fusturace', 'fustuach', 'futeases', 'futearace', 'futeaach', 'program', 'neo_02', 'neo_04', 'neo_05', 'neo_06', 'neo_07', 'neo_10', 'neo_11', 'neo_13', 'neo_17', 'neo_19', 'neo_20', 'neo_21', 'neo_22', 'neo_25', 'neo_26', 'neo_28', 'neo_32', 'neo_34', 'neo_35', 'neo_36', 'neo_37', 'neo_40', 'neo_41', 'neo_43', 'neo_47', 'neo_49', 'neo_50', 'neo_51', 'neo_52', 'neo_53', 'neo_56', 'neo_58', 'neo_60', 'r_neo_01', 'r_neo_03', 'r_neo_08', 'r_neo_09', 'r_neo_12', 'r_neo_14', 'r_neo_15', 'r_neo_16', 'r_neo_18', 'r_neo_23', 'r_neo_24', 'r_neo_27', 'r_neo_29', 'r_neo_30', 'r_neo_31', 'r_neo_33', 'r_neo_38', 'r_neo_39', 'r_neo_42', 'r_neo_44', 'r_neo_45', 'r_neo_46', 'r_neo_48', 'r_neo_54', 'r_neo_55', 'r_neo_57', 'r_neo_59', 'neo_n', 'neo_e', 'neo_o', 'neo_a', 'neo_c', 'tse_03', 'tse_04', 'tse_15', 'tse_09', 'tse_11', 'tse_13', 'tse_06', 'tse_16', 'tse_18', 'tse_20', 'tse_22', 'tse_23', 'tse_01', 'tse_02', 'tse_05', 'tse_07', 'tse_08', 'tse_10', 'tse_12', 'tse_14', 'tse_17', 'tse_19', 'tse_21', 'tse_24', 'tse_se', 'tse_is', 'tse_cm', 'tse_total', 'das_01', 'das_02', 'das_03', 'das_04', 'das_05', 'das_06', 'das_07', 'das_08', 'das_09', 'das_10', 'das_11', 'das_12', 'das_13', 'das_14', 'das_15', 'das_16', 'das_17', 'das_18', 'das_19', 'das_20', 'das_21', 'das_depression', 'das_anxiety', 'das_stress', 'fit_01', 'fit_04', 'fit_05', 'fit_06', 'fit_07', 'fit_08', 'fit_09', 'fit_10', 'fit_11', 'fit_12', 'fit_13', 'fit_total', 'ytrt_01', 'ytrt_02', 'ytrt_03', 'ytrt_04', 'ytrt_05', 'ytrt_total', 'tmas_01', 'tmas_02', 'tmas_04', 'tmas_07', 'tmas_10', 'tmas_11', 'tmas_13', 'tmas_14', 'tmas_17', 'tmas_18', 'r_tmas_03', 'r_tmas_06', 'r_tmas_12', 'r_tmas_15', 'r_tmas_16', 'r_tmas_19', 'r_tmas_20', 'tmas_total', 'imts_01', 'imts_02', 'imts_03', 'imts_04', 'imts_05', 'imts_total', 'rsq_03', 'rsq_10', 'rsq_27', 'rsq_30', 'r_rsq_01', 'r_rsq_05', 'r_rsq_07', 'r_rsq_11', 'r_rsq_12', 'r_rsq_13', 'r_rsq_17', 'r_rsq_20', 'r_rsq_21', 'r_rsq_23', 'r_rsq_24', 'r_rsq_28', 'r_rsq_29', 'rsq_total', 'grit_01', 'grit_04', 'grit_06', 'grit_09', 'grit_10', 'grit_12', 'r_grit_02', 'r_grit_03', 'r_grit_05', 'r_grit_07', 'r_grit_08', 'r_grit_11', 'grit_total', 'crtse_05', 'crtse_06', 'crtse_07', 'crtse_08', 'crtse_09', 'crtse_10', 'crtse_12', 'crtse_13', 'crtse_14', 'crtse_15', 'crtse_16', 'crtse_17', 'crtse_18', 'crtse_19', 'crtse_20', 'crtse_22', 'crtse_23', 'crtse_24', 'crtse_25', 'crtse_27', 'crtse_28', 'crtse_30', 'crtse_31', 'crtse_33', 'crtse_35', 'crtse_36', 'crtse_41', 'crtse_total']},    
    {type: 'specific_survey',label:'Specific Survey List',values :['br_base_affect','base_app_dev_adjust','base_app_dev_challenge', 'base_app_dev_coach', 'base_app_dev_counselor', 'base_app_dev_discuss', 'base_app_dev_parconf', 'base_app_dev_plan', 'base_app_dev_referral', 'base_app_dev_request', 'base_app_dev_space', 'base_app_dev_sped', 'base_app_dev_spend_time', 'base_app_dev_studconf', 'base_app_eth_adjust', 'base_app_eth_challenge', 'base_app_eth_coach', 'base_app_eth_counselor', 'base_app_eth_discuss', 'base_app_eth_parconf', 'base_app_eth_plan', 'base_app_eth_referral', 'base_app_eth_request', 'base_app_eth_space', 'base_app_eth_sped', 'base_app_eth_spend_time', 'base_app_eth_studconf', 'base_beh_dev_attention', 'base_beh_dev_behavior', 'base_beh_dev_contribute', 'base_beh_dev_defiant', 'base_beh_dev_demand', 'base_beh_dev_distracted', 'base_beh_dev_disturb', 'base_beh_dev_excitable', 'base_beh_dev_fidget', 'base_beh_dev_hum', 'base_beh_dev_mood', 'base_beh_dev_quarrel', 'base_beh_dev_rating', 'base_beh_dev_rating_impulsive', 'base_beh_dev_rating_opdefiant', 'base_beh_dev_restless', 'base_beh_dev_smart', 'base_beh_dev_temper', 'base_beh_dev_uncoop', 'base_beh_eth_attention', 'base_beh_eth_behavior', 'base_beh_eth_contribute', 'base_beh_eth_defiant', 'base_beh_eth_demand', 'base_beh_eth_distracted', 'base_beh_eth_disturb', 'base_beh_eth_excitable', 'base_beh_eth_fidget', 'base_beh_eth_hum', 'base_beh_eth_mood', 'base_beh_eth_quarrel', 'base_beh_eth_rating', 'base_beh_eth_rating_impulsive', 'base_beh_eth_rating_opdefiant', 'base_beh_eth_restless', 'base_beh_eth_smart', 'base_beh_eth_temper', 'base_beh_eth_uncoop', 'base_enddate', 'base_manage_app_dev_negative', 'base_manage_app_dev_positive', 'base_manage_app_dev_punitive', 'base_manage_app_eth_negative', 'base_manage_app_eth_positive', 'base_manage_app_eth_punitive', 'base_sim_beneficial', 'base_sim_cmsk', 'base_sim_conf', 'base_sim_conf_authentic', 'base_sim_conf_different', 'base_sim_conf_rapport', 'base_sim_enough_time', 'base_sim_fbsk', 'base_sim_fbsk_prepare', 'base_sim_fbsk_support', 'base_sim_like_use_again', 'base_sim_nervous', 'base_sim_recommend', 'base_sim_relevant_prof', 'base_sim_relevant_studies', 'base_sim_sufficient_prep', 'base_sim_txt_beneficial', 'base_sim_txt_cmsk', 'base_sim_txt_concerns', 'base_sim_txt_conf', 'base_sim_txt_conf_authentic', 'base_sim_txt_conf_rapport', 'base_sim_txt_fbsk', 'base_sim_txt_improve_exp', 'base_sim_txt_supports', 'base_sim_useful_tool', 'base_sim_worried_perform', 'base_startdate', 'big5_ag_1', 'big5_ag_1_r', 'big5_ag_10', 'big5_ag_2', 'big5_ag_3', 'big5_ag_3_r', 'big5_ag_4', 'big5_ag_5', 'big5_ag_5_r', 'big5_ag_6', 'big5_ag_7', 'big5_ag_7_r', 'big5_ag_8', 'big5_ag_9', 'big5_ag_total', 'big5_con_1', 'big5_con_10', 'big5_con_2', 'big5_con_2_r', 'big5_con_3', 'big5_con_4', 'big5_con_4_r', 'big5_con_5', 'big5_con_6', 'big5_con_6_r', 'big5_con_7', 'big5_con_8', 'big5_con_8_r', 'big5_con_9', 'big5_con_total', 'big5_emo_1', 'big5_emo_1_r', 'big5_emo_10', 'big5_emo_10_r', 'big5_emo_2', 'big5_emo_3', 'big5_emo_3_r', 'big5_emo_4', 'big5_emo_5', 'big5_emo_5_r', 'big5_emo_6', 'big5_emo_6_r', 'big5_emo_7', 'big5_emo_7_r', 'big5_emo_8', 'big5_emo_8_r', 'big5_emo_9', 'big5_emo_9_r', 'big5_emo_total', 'big5_enddate', 'big5_ext_1', 'big5_ext_10', 'big5_ext_10_r', 'big5_ext_2', 'big5_ext_2_r', 'big5_ext_3', 'big5_ext_4', 'big5_ext_4_r', 'big5_ext_5', 'big5_ext_6', 'big5_ext_6_r', 'big5_ext_7', 'big5_ext_8', 'big5_ext_8_r', 'big5_ext_9', 'big5_ext_total', 'big5_intell_1', 'big5_intell_10', 'big5_intell_2', 'big5_intell_2_r', 'big5_intell_3', 'big5_intell_4', 'big5_intell_4_r', 'big5_intell_5', 'big5_intell_6', 'big5_intell_6_r', 'big5_intell_7', 'big5_intell_8', 'big5_intell_9', 'big5_intell_total', 'br_post_app_dev_adjust', 'br_post_app_dev_challenge', 'br_post_app_dev_coach', 'br_post_app_dev_counselor', 'br_post_app_dev_discuss', 'br_post_app_dev_parconf', 'br_post_app_dev_plan', 'br_post_app_dev_referral', 'br_post_app_dev_request', 'br_post_app_dev_space', 'br_post_app_dev_sped', 'br_post_app_dev_spend_time', 'br_post_app_dev_studconf', 'br_post_app_eth_adjust', 'br_post_app_eth_challenge', 'br_post_app_eth_coach', 'br_post_app_eth_counselor', 'br_post_app_eth_discuss', 'br_post_app_eth_parconf', 'br_post_app_eth_plan', 'br_post_app_eth_referral', 'br_post_app_eth_request', 'br_post_app_eth_space', 'br_post_app_eth_sped', 'br_post_app_eth_spend_time', 'br_post_app_eth_studconf', 'br_post_beh_desire_other_text', 'br_post_beh_dev_attention', 'br_post_beh_dev_behavior', 'br_post_beh_dev_contribute', 'br_post_beh_dev_defiant', 'br_post_beh_dev_demand', 'br_post_beh_dev_distracted', 'br_post_beh_dev_disturb', 'br_post_beh_dev_excitable', 'br_post_beh_dev_fidget', 'br_post_beh_dev_hum', 'br_post_beh_dev_mood', 'br_post_beh_dev_quarrel', 'br_post_beh_dev_rating', 'br_post_beh_dev_rating_impulsive', 'br_post_beh_dev_rating_opdefiant', 'br_post_beh_dev_restless', 'br_post_beh_dev_smart', 'br_post_beh_dev_temper', 'br_post_beh_dev_uncoop', 'br_post_beh_eth_attention', 'br_post_beh_eth_behavior', 'br_post_beh_eth_contribute', 'br_post_beh_eth_defiant', 'br_post_beh_eth_demand', 'br_post_beh_eth_distracted', 'br_post_beh_eth_disturb', 'br_post_beh_eth_excitable', 'br_post_beh_eth_fidget', 'br_post_beh_eth_hum', 'br_post_beh_eth_mood', 'br_post_beh_eth_quarrel', 'br_post_beh_eth_rating', 'br_post_beh_eth_rating_impulsive', 'br_post_beh_eth_rating_opdefiant', 'br_post_beh_eth_restless', 'br_post_beh_eth_smart', 'br_post_beh_eth_temper', 'br_post_beh_eth_uncoop', 'br_post_beh_follow_quest', 'br_post_beh_positive_tone', 'br_post_beh_praise_app', 'br_post_beh_praise_contr', 'br_post_beh_redirect_inapp', 'br_post_beh_redirect_quick', 'br_post_beh_specific_lang', 'br_post_beh_talk_min', 'br_post_enddate', 'br_post_manage_app_dev_negative', 'br_post_manage_app_dev_positive', 'br_post_manage_app_dev_punitive', 'br_post_manage_app_eth_negative', 'br_post_manage_app_eth_positive', 'br_post_manage_app_eth_punitive', 'br_post_me_post_coach', 'br_post_me_pre_coach', 'br_post_sim_beneficial', 'br_post_sim_cmsk', 'br_post_sim_enough_time', 'br_post_sim_first_cmsk', 'br_post_sim_like_use_again', 'br_post_sim_nervous', 'br_post_sim_recommend', 'br_post_sim_relevant_prof', 'br_post_sim_relevant_studies', 'br_post_sim_sec_cmsk', 'br_post_sim_sufficient_prep', 'br_post_sim_txt_beneficial', 'br_post_sim_txt_cmsk', 'br_post_sim_txt_concerns', 'br_post_sim_txt_improve_exp', 'br_post_sim_txt_supports', 'br_post_sim_useful_tool', 'br_post_sim_worried_perform', 'br_post_startdate', 'br_post_tse_01', 'br_post_tse_02', 'br_post_tse_03', 'br_post_tse_04', 'br_post_tse_05', 'br_post_tse_06', 'br_post_tse_07', 'br_post_tse_08', 'br_post_tse_09', 'br_post_tse_10', 'br_post_tse_11', 'br_post_tse_12', 'br_post_tse_13', 'br_post_tse_14', 'br_post_tse_15', 'br_post_tse_16', 'br_post_tse_17', 'br_post_tse_18', 'br_post_tse_19', 'br_post_tse_20', 'br_post_tse_21', 'br_post_tse_22', 'br_post_tse_23', 'br_post_tse_24', 'br_post_tse_cm', 'br_post_tse_is', 'br_post_tse_overall', 'br_post_tse_se', 'br_pre_enddate', 'br_pre_misbehavior_anticipate', 'br_pre_stai_calm', 'br_pre_stai_calm_rc', 'br_pre_stai_content', 'br_pre_stai_content_rc', 'br_pre_stai_relaxed', 'br_pre_stai_relaxed_rc', 'br_pre_stai_tense', 'br_pre_stai_total', 'br_pre_stai_upset', 'br_pre_stai_worried', 'br_pre_startdate', 'br_pre_tse_03', 'br_pre_tse_05', 'br_pre_tse_08', 'br_pre_tse_13', 'br_pre_tse_15', 'br_pre_tse_16', 'br_pre_tse_19', 'br_pre_tse_21', 'br_pre_tse_cm', 'exit_app_eth_adjust', 'exit_app_eth_challenge', 'exit_app_eth_coach', 'exit_app_eth_counselor', 'exit_app_eth_discuss', 'exit_app_eth_parconf', 'exit_app_eth_plan', 'exit_app_eth_referral', 'exit_app_eth_request', 'exit_app_eth_space', 'exit_app_eth_sped', 'exit_app_eth_spend_time', 'exit_app_eth_studconf', 'exit_beh_eth_attention', 'exit_beh_eth_behavior', 'exit_beh_eth_contribute', 'exit_beh_eth_defiant', 'exit_beh_eth_demand', 'exit_beh_eth_distracted', 'exit_beh_eth_disturb', 'exit_beh_eth_excitable', 'exit_beh_eth_fidget', 'exit_beh_eth_hum', 'exit_beh_eth_mood', 'exit_beh_eth_quarrel', 'exit_beh_eth_rating', 'exit_beh_eth_rating_impulsive', 'exit_beh_eth_rating_opdefiant', 'exit_beh_eth_restless', 'exit_beh_eth_smart', 'exit_beh_eth_temper', 'exit_beh_eth_uncoop', 'exit_enddate', 'exit_manage_app_eth_negative', 'exit_manage_app_eth_positive', 'exit_manage_app_eth_punitive', 'exit_sim_beneficial', 'exit_sim_cmsk', 'exit_sim_enough_time', 'exit_sim_fbsk', 'exit_sim_like_use_again', 'exit_sim_nervous', 'exit_sim_recommend', 'exit_sim_relevant_prof', 'exit_sim_relevant_studies', 'exit_sim_sufficient_prep', 'exit_sim_txt_beneficial', 'exit_sim_txt_cmsk', 'exit_sim_txt_concerns', 'exit_sim_txt_fbsk', 'exit_sim_txt_improve_exp', 'exit_sim_txt_supports', 'exit_sim_useful_tool', 'exit_sim_worried_perform', 'exit_startdate', 'fb_post_coach_beneficial', 'fb_post_coach_clear', 'fb_post_coach_expertise', 'fb_post_coach_friendly', 'fb_post_coach_support', 'fb_post_coaching', 'fb_post_enddate', 'fb_post_me_post_coach', 'fb_post_me_pre_coach', 'fb_post_sim_beneficial', 'fb_post_sim_coach_recommend', 'fb_post_sim_coach_use_again', 'fb_post_sim_enough_time', 'fb_post_sim_first_fbsk', 'fb_post_sim_first_sort_did', 'fb_post_sim_first_sort_did_oth', 'fb_post_sim_first_sort_didnt', 'fb_post_sim_first_sort_didnt_oth', 'fb_post_sim_first_txt_fbsk', 'fb_post_sim_like_use_again', 'fb_post_sim_nervous', 'fb_post_sim_prepare_differently', 'fb_post_sim_recommend', 'fb_post_sim_relevant_prof', 'fb_post_sim_relevant_studies', 'fb_post_sim_sec_fbsk', 'fb_post_sim_sec_sort_did', 'fb_post_sim_sec_sort_did_oth', 'fb_post_sim_sec_sort_didnt', 'fb_post_sim_sec_sort_didnt_oth', 'fb_post_sim_sec_txt_fbsk', 'fb_post_sim_sr_recommend', 'fb_post_sim_sr_use_again', 'fb_post_sim_sufficient_prep', 'fb_post_sim_support', 'fb_post_sim_teach_change', 'fb_post_sim_teach_change_rate', 'fb_post_sim_txt_beneficial', 'fb_post_sim_txt_concerns', 'fb_post_sim_txt_improve_exp', 'fb_post_sim_used_before', 'fb_post_sim_useful_tool', 'fb_post_sim_worried_perform', 'fb_post_sr_clear', 'fb_post_sr_knowledge_skills', 'fb_post_sr_practice_change', 'fb_post_sr_sufficient_reflect', 'fb_post_sr_support', 'fb_post_srcoach_beneficial', 'fb_post_srcoach_text_support', 'fb_post_startdate', 'fb_post_tse_01', 'fb_post_tse_02', 'fb_post_tse_03', 'fb_post_tse_04', 'fb_post_tse_05', 'fb_post_tse_06', 'fb_post_tse_07', 'fb_post_tse_08', 'fb_post_tse_09', 'fb_post_tse_10', 'fb_post_tse_11', 'fb_post_tse_12', 'fb_post_tse_13', 'fb_post_tse_14', 'fb_post_tse_15', 'fb_post_tse_16', 'fb_post_tse_17', 'fb_post_tse_18', 'fb_post_tse_19', 'fb_post_tse_20', 'fb_post_tse_21', 'fb_post_tse_22', 'fb_post_tse_23', 'fb_post_tse_24', 'fb_pre_enddate', 'fb_pre_sim_beneficial', 'fb_pre_sim_excited', 'fb_pre_sim_nervous', 'fb_pre_sim_relevant_prof', 'fb_pre_sim_relevant_studies', 'fb_pre_sim_txt_concerns', 'fb_pre_sim_txt_fbk_purpose', 'fb_pre_sim_txt_fbk_steps', 'fb_pre_sim_txt_goals', 'fb_pre_sim_txt_inference', 'fb_pre_sim_txt_look_forward', 'fb_pre_sim_txt_questions', 'fb_pre_sim_txt_study_diverge1', 'fb_pre_sim_txt_study_diverge2', 'fb_pre_sim_txt_study_diverge3', 'fb_pre_sim_txt_study_exemplar1', 'fb_pre_sim_txt_study_exemplar2', 'fb_pre_sim_txt_study_exemplar3', 'fb_pre_sim_txt_study_feedback3', 'fb_pre_sim_txt_study_reader1', 'fb_pre_sim_txt_study_reader2', 'fb_pre_sim_txt_study_response1', 'fb_pre_sim_txt_study_response2', 'fb_pre_sim_txt_skill_purpose', 'fb_pre_sim_txt_support_inf', 'fb_pre_sim_used_before', 'fb_pre_sim_useful_tool', 'fb_pre_sim_worried_perform', 'fb_pre_startdate', 'haber_approach_to_students', 'haber_at_risk_students', 'haber_explain_stud_suc', 'haber_explain_teach_suc', 'haber_fallibility', 'haber_org_and_plan', 'haber_persistence', 'haber_survive_in_bureaucracy', 'haber_testdate', 'haber_theory_to_practice', 'haber_total', 'haber_values_students_learning']},
    {type: 'specific_performance',label: 'Specific Performance List',values :['br_base_b1ac', 'br_base_b1ac_agree', 'br_base_b1cu', 'br_base_b1cu_agree', 'br_base_b1oc', 'br_base_b1oc_agree', 'br_base_b1re', 'br_base_b1re_agree', 'br_base_b1sp', 'br_base_b1sp_agree', 'br_base_b1su', 'br_base_b1su_agree', 'br_base_b1ti', 'br_base_b1ti_agree', 'br_base_b2ac', 'br_base_b2ac_agree', 'br_base_b2cu', 'br_base_b2cu_agree', 'br_base_b2oc', 'br_base_b2oc_agree', 'br_base_b2re', 'br_base_b2re_agree', 'br_base_b2sp', 'br_base_b2sp_agree', 'br_base_b2su', 'br_base_b2su_agree', 'br_base_b2ti', 'br_base_b2ti_agree', 'br_base_b3ac', 'br_base_b3ac_agree', 'br_base_b3cu', 'br_base_b3cu_agree', 'br_base_b3oc', 'br_base_b3oc_agree', 'br_base_b3re', 'br_base_b3re_agree', 'br_base_b3sp', 'br_base_b3sp_agree', 'br_base_b3su', 'br_base_b3su_agree', 'br_base_b3ti', 'br_base_b3ti_agree', 'br_base_b4ac', 'br_base_b4ac_agree', 'br_base_b4cu', 'br_base_b4cu_agree', 'br_base_b4oc', 'br_base_b4oc_agree', 'br_base_b4re', 'br_base_b4re_agree', 'br_base_b4sp', 'br_base_b4sp_agree', 'br_base_b4su', 'br_base_b4su_agree', 'br_base_b4ti', 'br_base_b4ti_agree', 'br_base_b5ac', 'br_base_b5ac_agree', 'br_base_b5cu', 'br_base_b5cu_agree', 'br_base_b5oc', 'br_base_b5oc_agree', 'br_base_b5re', 'br_base_b5re_agree', 'br_base_b5sp', 'br_base_b5sp_agree', 'br_base_b5su', 'br_base_b5su_agree', 'br_base_b5ti', 'br_base_b5ti_agree', 'br_base_b6ac', 'br_base_b6ac_agree', 'br_base_b6cu', 'br_base_b6cu_agree', 'br_base_b6oc', 'br_base_b6oc_agree', 'br_base_b6re', 'br_base_b6re_agree', 'br_base_b6sp', 'br_base_b6sp_agree', 'br_base_b6su', 'br_base_b6su_agree', 'br_base_b6ti', 'br_base_b6ti_agree', 'br_base_cid', 'br_base_cid2', 'br_base_dc', 'br_base_descript', 'br_base_quality', 'br_base_quality_agree', 'br_base_rationale', 'br_base_rubric_affect', 'br_base_rubric_dial', 'br_base_rubric_engage', 'br_base_rubric_norms', 'br_base_rubric_spec', 'br_base_rubric_suc', 'br_base_tot_ac', 'br_base_tot_ac_agree', 'br_base_tot_cu', 'br_base_tot_cu_agree', 'br_base_tot_nb', 'br_base_tot_nb_agree', 'br_base_tot_oc', 'br_base_tot_oc_agree', 'br_base_tot_se', 'br_base_tot_se_agree', 'br_base_tot_sp', 'br_base_tot_sp_agree', 'br_base_tot_su', 'br_base_tot_su_agree', 'br_base_tot_ti', 'br_base_tot_ti_agree', 'br_base_vid', 'br_exit_affect', 'br_exit_b1ac', 'br_exit_b1ac_agree', 'br_exit_b1cu', 'br_exit_b1cu_agree', 'br_exit_b1oc', 'br_exit_b1oc_agree', 'br_exit_b1re', 'br_exit_b1re_agree', 'br_exit_b1sp', 'br_exit_b1sp_agree', 'br_exit_b1su', 'br_exit_b1su_agree', 'br_exit_b1ti', 'br_exit_b1ti_agree', 'br_exit_b2ac', 'br_exit_b2ac_agree', 'br_exit_b2cu', 'br_exit_b2cu_agree', 'br_exit_b2oc', 'br_exit_b2oc_agree', 'br_exit_b2re', 'br_exit_b2re_agree', 'br_exit_b2sp', 'br_exit_b2sp_agree', 'br_exit_b2su', 'br_exit_b2su_agree', 'br_exit_b2ti', 'br_exit_b2ti_agree', 'br_exit_b3ac', 'br_exit_b3ac_agree', 'br_exit_b3cu', 'br_exit_b3cu_agree', 'br_exit_b3oc', 'br_exit_b3oc_agree', 'br_exit_b3re', 'br_exit_b3re_agree', 'br_exit_b3sp', 'br_exit_b3sp_agree', 'br_exit_b3su', 'br_exit_b3su_agree', 'br_exit_b3ti', 'br_exit_b3ti_agree', 'br_exit_b4ac', 'br_exit_b4ac_agree', 'br_exit_b4cu', 'br_exit_b4cu_agree', 'br_exit_b4oc', 'br_exit_b4oc_agree', 'br_exit_b4re', 'br_exit_b4re_agree', 'br_exit_b4sp', 'br_exit_b4sp_agree', 'br_exit_b4su', 'br_exit_b4su_agree', 'br_exit_b4ti', 'br_exit_b4ti_agree', 'br_exit_b5ac', 'br_exit_b5ac_agree', 'br_exit_b5cu', 'br_exit_b5cu_agree', 'br_exit_b5oc', 'br_exit_b5oc_agree', 'br_exit_b5re', 'br_exit_b5re_agree', 'br_exit_b5sp', 'br_exit_b5sp_agree', 'br_exit_b5su', 'br_exit_b5su_agree', 'br_exit_b5ti', 'br_exit_b5ti_agree', 'br_exit_b6ac', 'br_exit_b6ac_agree', 'br_exit_b6cu', 'br_exit_b6cu_agree', 'br_exit_b6oc', 'br_exit_b6oc_agree', 'br_exit_b6re', 'br_exit_b6re_agree', 'br_exit_b6sp', 'br_exit_b6sp_agree', 'br_exit_b6su', 'br_exit_b6su_agree', 'br_exit_b6ti', 'br_exit_b6ti_agree', 'br_exit_cid', 'br_exit_cid2', 'br_exit_dc', 'br_exit_descript', 'br_exit_quality', 'br_exit_quality_agree', 'br_exit_rationale', 'br_exit_tot_ac', 'br_exit_tot_ac_agree', 'br_exit_tot_cu', 'br_exit_tot_cu_agree', 'br_exit_tot_nb', 'br_exit_tot_nb_agree', 'br_exit_tot_oc', 'br_exit_tot_oc_agree', 'br_exit_tot_se', 'br_exit_tot_se_agree', 'br_exit_tot_sp', 'br_exit_tot_sp_agree', 'br_exit_tot_su', 'br_exit_tot_su_agree', 'br_exit_tot_ti', 'br_exit_tot_ti_agree', 'br_exit_vid', 'br_post_affect', 'br_post_b1ac', 'br_post_b1ac_agree', 'br_post_b1cu', 'br_post_b1cu_agree', 'br_post_b1oc', 'br_post_b1oc_agree', 'br_post_b1re', 'br_post_b1re_agree', 'br_post_b1sp', 'br_post_b1sp_agree', 'br_post_b1su', 'br_post_b1su_agree', 'br_post_b1ti', 'br_post_b1ti_agree', 'br_post_b2ac', 'br_post_b2ac_agree', 'br_post_b2cu', 'br_post_b2cu_agree', 'br_post_b2oc', 'br_post_b2oc_agree', 'br_post_b2re', 'br_post_b2re_agree', 'br_post_b2sp', 'br_post_b2sp_agree', 'br_post_b2su', 'br_post_b2su_agree', 'br_post_b2ti', 'br_post_b2ti_agree', 'br_post_b3ac', 'br_post_b3ac_agree', 'br_post_b3cu', 'br_post_b3cu_agree', 'br_post_b3oc', 'br_post_b3oc_agree', 'br_post_b3re', 'br_post_b3re_agree', 'br_post_b3sp', 'br_post_b3sp_agree', 'br_post_b3su', 'br_post_b3su_agree', 'br_post_b3ti', 'br_post_b3ti_agree', 'br_post_b4ac', 'br_post_b4ac_agree', 'br_post_b4cu', 'br_post_b4cu_agree', 'br_post_b4oc', 'br_post_b4oc_agree', 'br_post_b4re', 'br_post_b4re_agree', 'br_post_b4sp', 'br_post_b4sp_agree', 'br_post_b4su', 'br_post_b4su_agree', 'br_post_b4ti', 'br_post_b4ti_agree', 'br_post_b5ac', 'br_post_b5ac_agree', 'br_post_b5cu', 'br_post_b5cu_agree', 'br_post_b5oc', 'br_post_b5oc_agree', 'br_post_b5re', 'br_post_b5re_agree', 'br_post_b5sp', 'br_post_b5sp_agree', 'br_post_b5su', 'br_post_b5su_agree', 'br_post_b5ti', 'br_post_b5ti_agree', 'br_post_b6ac', 'br_post_b6ac_agree', 'br_post_b6cu', 'br_post_b6cu_agree', 'br_post_b6oc', 'br_post_b6oc_agree', 'br_post_b6re', 'br_post_b6re_agree', 'br_post_b6sp', 'br_post_b6sp_agree', 'br_post_b6su', 'br_post_b6su_agree', 'br_post_b6ti', 'br_post_b6ti_agree', 'br_post_cid', 'br_post_cid2', 'br_post_dc', 'br_post_descript', 'br_post_quality', 'br_post_quality_agree', 'br_post_rationale', 'br_post_rubric_affect', 'br_post_rubric_dial', 'br_post_rubric_engage', 'br_post_rubric_norms', 'br_post_rubric_spec', 'br_post_rubric_suc', 'br_post_tot_ac', 'br_post_tot_ac_agree', 'br_post_tot_cu', 'br_post_tot_cu_agree', 'br_post_tot_nb', 'br_post_tot_nb_agree', 'br_post_tot_oc', 'br_post_tot_oc_agree', 'br_post_tot_se', 'br_post_tot_se_agree', 'br_post_tot_sp', 'br_post_tot_sp_agree', 'br_post_tot_su', 'br_post_tot_su_agree', 'br_post_tot_ti', 'br_post_tot_ti_agree', 'br_post_vid', 'br_pre_affect', 'br_pre_b1ac', 'br_pre_b1ac_agree', 'br_pre_b1cu', 'br_pre_b1cu_agree', 'br_pre_b1oc', 'br_pre_b1oc_agree', 'br_pre_b1re', 'br_pre_b1re_agree', 'br_pre_b1sp', 'br_pre_b1sp_agree', 'br_pre_b1su', 'br_pre_b1su_agree', 'br_pre_b1ti', 'br_pre_b1ti_agree', 'br_pre_b2ac', 'br_pre_b2ac_agree', 'br_pre_b2cu', 'br_pre_b2cu_agree', 'br_pre_b2oc', 'br_pre_b2oc_agree', 'br_pre_b2re', 'br_pre_b2re_agree', 'br_pre_b2sp', 'br_pre_b2sp_agree', 'br_pre_b2su', 'br_pre_b2su_agree', 'br_pre_b2ti', 'br_pre_b2ti_agree', 'br_pre_b3ac', 'br_pre_b3ac_agree', 'br_pre_b3cu', 'br_pre_b3cu_agree', 'br_pre_b3oc', 'br_pre_b3oc_agree', 'br_pre_b3re', 'br_pre_b3re_agree', 'br_pre_b3sp', 'br_pre_b3sp_agree', 'br_pre_b3su', 'br_pre_b3su_agree', 'br_pre_b3ti', 'br_pre_b3ti_agree', 'br_pre_b4ac', 'br_pre_b4ac_agree', 'br_pre_b4cu', 'br_pre_b4cu_agree', 'br_pre_b4oc', 'br_pre_b4oc_agree', 'br_pre_b4re', 'br_pre_b4re_agree', 'br_pre_b4sp', 'br_pre_b4sp_agree', 'br_pre_b4su', 'br_pre_b4su_agree', 'br_pre_b4ti', 'br_pre_b4ti_agree', 'br_pre_b5ac', 'br_pre_b5ac_agree', 'br_pre_b5cu', 'br_pre_b5cu_agree', 'br_pre_b5oc', 'br_pre_b5oc_agree', 'br_pre_b5re', 'br_pre_b5re_agree', 'br_pre_b5sp', 'br_pre_b5sp_agree', 'br_pre_b5su', 'br_pre_b5su_agree', 'br_pre_b5ti', 'br_pre_b5ti_agree', 'br_pre_b6ac', 'br_pre_b6ac_agree', 'br_pre_b6cu', 'br_pre_b6cu_agree', 'br_pre_b6oc', 'br_pre_b6oc_agree', 'br_pre_b6re', 'br_pre_b6re_agree', 'br_pre_b6sp', 'br_pre_b6sp_agree', 'br_pre_b6su', 'br_pre_b6su_agree', 'br_pre_b6ti', 'br_pre_b6ti_agree', 'br_pre_cid', 'br_pre_cid2', 'br_pre_dc', 'br_pre_descript', 'br_pre_quality', 'br_pre_quality_agree', 'br_pre_rationale', 'br_pre_rubric_affect', 'br_pre_rubric_dial', 'br_pre_rubric_engage', 'br_pre_rubric_norms', 'br_pre_rubric_spec', 'br_pre_rubric_suc', 'br_pre_tot_ac', 'br_pre_tot_ac_agree', 'br_pre_tot_cu', 'br_pre_tot_cu_agree', 'br_pre_tot_nb', 'br_pre_tot_nb_agree', 'br_pre_tot_oc', 'br_pre_tot_oc_agree', 'br_pre_tot_se', 'br_pre_tot_se_agree', 'br_pre_tot_sp', 'br_pre_tot_sp_agree', 'br_pre_tot_su', 'br_pre_tot_su_agree', 'br_pre_tot_ti', 'br_pre_tot_ti_agree', 'br_pre_vid', 'fb_base_cid', 'fb_base_cid2', 'fb_base_dc', 'fb_base_f_desc', 'fb_base_f_desc_agree', 'fb_base_f_ntxt', 'fb_base_f_ntxt_agree', 'fb_base_f_perf', 'fb_base_f_perf_agree', 'fb_base_f_rest', 'fb_base_f_rest_agree', 'fb_base_f_txt', 'fb_base_f_txt_agree', 'fb_base_quality', 'fb_base_quality_agree', 'fb_base_tot_hit', 'fb_base_tot_hit_agree', 'fb_base_tot_oc', 'fb_base_tot_oc_agree', 'fb_base_vid', 'fb_exit_cid', 'fb_exit_cid2', 'fb_exit_dc', 'fb_exit_f_desc', 'fb_exit_f_desc_agree', 'fb_exit_f_ntxt', 'fb_exit_f_ntxt_agree', 'fb_exit_f_perf', 'fb_exit_f_perf_agree', 'fb_exit_f_rest', 'fb_exit_f_rest_agree', 'fb_exit_f_txt', 'fb_exit_f_txt_agree', 'fb_exit_quality', 'fb_exit_quality_agree', 'fb_exit_tot_hit', 'fb_exit_tot_hit_agree', 'fb_exit_tot_oc', 'fb_exit_tot_oc_agree', 'fb_exit_vid', 'fb_post_cid', 'fb_post_cid2', 'fb_post_dc', 'fb_post_f_desc', 'fb_post_f_desc_agree', 'fb_post_f_ntxt', 'fb_post_f_ntxt_agree', 'fb_post_f_perf', 'fb_post_f_perf_agree', 'fb_post_f_rest', 'fb_post_f_rest_agree', 'fb_post_f_txt', 'fb_post_f_txt_agree', 'fb_post_quality', 'fb_post_quality_agree', 'fb_post_tot_hit', 'fb_post_tot_hit_agree', 'fb_post_tot_oc', 'fb_post_tot_oc_agree', 'fb_post_vid', 'fb_pre_cid', 'fb_pre_cid2', 'fb_pre_dc', 'fb_pre_f_desc', 'fb_pre_f_desc_agree', 'fb_pre_f_ntxt', 'fb_pre_f_ntxt_agree', 'fb_pre_f_perf', 'fb_pre_f_perf_agree', 'fb_pre_f_rest', 'fb_pre_f_rest_agree', 'fb_pre_f_txt', 'fb_pre_f_txt_agree', 'fb_pre_quality', 'fb_pre_quality_agree', 'fb_pre_tot_hit', 'fb_pre_tot_hit_agree', 'fb_pre_tot_oc', 'fb_pre_tot_oc_agree', 'fb_pre_vid']},
]

export {QUERY_FIELDS,API_ENDPOINT,ROUTES,TRACKER_COLUMNS}
