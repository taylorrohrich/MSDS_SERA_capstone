********************************************************************************
* Importing and cleaning self-report coaching survey data for Spring 2019
* 
* Added by AKC on 10/01/2019    
********************************************************************************
/* Notes:	This do-file cleans raw self-report survey data for candidates in Spring 2019
*/

***If running the individual do.file, uncomment and define your directories below.
	
	*location of Box sync folder
	*global root_drive "D:\Box Sync\Project SimTeacher\9. Data\2018-19\"
	
** Need to update directory to Spring 2019
	cd "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/Survey responses"
	
/*	*location of raw data 
	global raw_data "${root_drive}Raw Data Exports"
	
	*location of output
	global output "${root_drive}Cleaning, Merging, and Analyzing Data/Output/"
	
	*location of graphs
	global graphs "${output}graphs"
	
	*location of tables
	global table "${output}tables"
	
	*location of random assignment
	global assignment "${root_drive}Randomization/"
	
	*location of working data files
	global working "${output}Working"
	
	*location of data files ready for analysis
	global analysis "${output}For Analysis"
	
	*Enter date of most recent sign up genius export
	*global sign_up_date "2017 11 27"
*/

* Importing baseline survey responses
import delimited "Raw excel data/Post-Simulator Student Survey (Round 1)- Spring 2019_July 24, 2019_15.25.csv", bindquote(strict) varnames(1)  maxquotedrows(100) clear 

* Dropping unnecessary variables and observations
drop enddate-userlanguage
drop if _n==1 | _n==2
drop if q1==""

* Renaming and cleaning variables
rename	q1			email
rename	q6_1		sim_cmsk
rename	q7			sim_txt_cmsk
rename	q8			sim_txt_eth_behavior
rename	q9			sim_txt_eth_contribute
rename	q10_1		beh_fidgeting
rename	q10_2		beh_humming
rename	q10_3		beh_excitable
rename	q10_4		beh_inattentive
rename	q10_5		beh_short_attention
rename	q10_6		beh_quarrelsome
rename	q10_7		beh_acts_smart
rename	q10_8		beh_unpredictable
rename	q10_9		beh_defiant
rename	q10_10		beh_uncooperative
rename	q10_11		beh_easily_frustrated
rename	q10_12		beh_disturbs_others
rename	q10_13		beh_restless
rename	q10_14		beh_mood_changes
rename	q11_1		app_coach_stu
rename	q12_1		app_adjust_expect
rename	q13_1		app_guidance_couns
rename	q14_1		app_rec_sped
rename	q15_1		app_discp_refer
rename	q16_1		app_confer_stu
rename	q17_1		app_confer_parent
rename	q18_1		app_behavior_plan
rename	q19_1		app_challenge_work
rename	q20_1		app_spend_time
rename	q21_1		app_space_regroup
rename	q22_1		app_beh_manage_coach
rename	q23_1		app_beh_manage_teach
rename	q24			sim_txt_supports
rename	q25_1		sim_nervous
rename	q25_2		sim_beneficial
rename	q25_3		sim_worried_perform
rename	q25_4		sim_useful_tool
rename	q25_5		sim_relevant_studies
rename	q25_6		sim_relevant_prof
rename	q25_7		sim_like_use_again
rename	q25_8		sim_recommend
rename	q25_9		sim_sufficient_prep
rename	q25_10		sim_enough_time
rename	q26			sim_txt_beneficial
rename	q27			sim_txt_improve_exp
rename	q28			sim_txt_concerns

* Cleaning email variable
gen email_clean=lower(email)
drop email
rename email_clean email
replace email = strtrim(email)
replace email="bh4fk@virginia.edu" if email=="bh4fk"
replace email="law2mc@virginia.edu" if email=="law2mc"
replace email="ajm8gx@virginia.edu" if email=="ajm8gx@virrginia.edu"
replace email="kra2fn@virginia.edu" if email=="kr2a2fn@virginia.edu"

* Dropping duplicate observations	
drop if email=="hwr9ex@virginia.edu" & startdate=="2019-05-09 09:31:57"
drop if email=="kmh3yj@virginia.edu" & startdate=="2019-05-09 08:17:37"
drop if email=="leo9um@virginia.edu" & startdate=="2019-05-09 07:39:03"

drop startdate

* Making numeric scores for different survey responses
foreach var of varlist beh_fidgeting-beh_mood_changes{
		replace `var' = "1" if `var'=="Not at all"
		replace `var' = "2" if `var'=="Just a little" 
		replace `var' = "3" if `var'=="Pretty much" 
		replace `var' = "4" if `var'=="Very much"
		destring `var', replace
}
label define behaviors 1 "Not at all" 2 "Just a little" 3 "Pretty much" 4 "Very much"
label values beh_fidgeting-beh_mood_changes behaviors		


foreach var of varlist app_coach_stu-app_beh_manage_teach {
        destring `var', replace
}

foreach var of varlist sim_nervous - sim_enough_time {
		replace `var' = "1" if `var'=="Strongly disagree"
		replace `var' = "2" if `var'=="Somewhat disagree" 
		replace `var' = "3" if `var'=="Undecided" 
		replace `var' = "4" if `var'=="Somewhat agree" 
		replace `var' = "5" if `var'=="Strongly agree"
		destring `var', replace
}
		
label define likert 5 "Strongly agree" 4 "Somewhat agree" 3 "Undecided" 2 "Somewhat disagree" 1 "Strongly disagree"	
label values sim_nervous - sim_enough_time likert
destring sim_cmsk, replace

* Generating total scores from Iowa Connors Scale
egen beh_rating_opdefiant=rowmean (beh_quarrelsome beh_acts_smart beh_unpredictable beh_defiant beh_uncooperative)
egen beh_rating_impulsive=rowmean (beh_fidgeting beh_humming beh_excitable beh_inattentive beh_short_attention)
egen beh_rating =rowmean (beh_fidgeting beh_humming beh_excitable beh_inattentive beh_short_attention beh_quarrelsome beh_acts_smart beh_unpredictable beh_defiant beh_uncooperative beh_easily_frustrated beh_disturbs_others beh_restless beh_mood_changes)
label var beh_rating_opdefiant "Iowa Connors Operational Defiant"
label var beh_rating_impulsive "Iowa Connors Impulsive"
label var beh_rating "Iowa Connors Overall"

*Reverse coding management approaches scale 	
foreach var of varlist app_coach_stu-app_beh_manage_teach {
		generate `var'_rc = `var'
        recode `var'_rc (1=10) (2=9) (3=8) (4=7) (5=6) (6=5) (7=4) (8=3) (9=2) (10=1)
}
	
*Creating scales for positive and negative management approaches
egen manage_app_negative = rowmean(app_coach_stu-app_discp_refer)
egen manage_app_positive = rowmean(app_confer_stu-app_beh_manage_teach)
		
*Generate time variable for appending surveys
gen time=2
	
* Saving dataset 
save "Working STATA files/Spring2019_Coaching_Post-Survey_Cleaned.dta", replace

