********************************************************************************
* Merging performance outcomes, survey outcomes, randomization information and
*  CPP data
*
* Spring Behavioral Redirections Study
* 
* Created by AKC on 12/10/2019
********************************************************************************

/* Notes:	This do file merges working STATA files (.dta) for coded performance
            outcome data and CPP covariate information from the Spring
			2019 semester
			
*/

/*	location of Box sync folder
	global root_drive "D:\Box Sync\Project SimTeacher\9. Data\2018-19"
	
	*location of raw data 
	global raw_data "${root_drive}/Raw Data Exports"
	
	*location of working data files
	global working "${root_drive}/Data"

	cd "${root_drive}"

*/

cd "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data"

* Opening coded performance outcome data
use "Final Analytic files/PerformanceOutcomes_Randomization_CPP_Merged.dta", clear

* Merging with survey outcomes
merge 1:1 email time using "Final Analytic files/SurveyOutcomes_Randomization_CPP_Merged.dta", update
drop _merge 

* Generating correct RA for baseline balance checks
gen coach_same=1 if fall2018coachingra== spring2019coachingra
replace coach_same=0 if fall2018coachingra!= spring2019coachingra
gen spring2019coachingra_correct=0 if fall2018coachingra==1 & coach_same==1
replace spring2019coachingra_correct=1 if fall2018coachingra==0 & coach_same==1
replace spring2019coachingra_correct=spring2019coachingra if coach_same==0
gen coach_correct_same=1 if fall2018coachingra== spring2019coachingra_correct
replace coach_correct_same=0 if fall2018coachingra!= spring2019coachingra_correct

* Keeping necessary variables
keep coach_name email name sis_id program section strata spring2019_coaching_recieved spring2019coachingra spring2019coachingra_correct id score_dc_avg prop_beh_ack ti_dc_avg prop_redirect su_dc_avg time beh_rating beh_rating_opdefiant beh_rating_impulsive manage_app_negative manage_app_positive ccs_gpa partch_either moedu_colab faedu_colab gender_female gender_female_miss age_21ab age_21ab_miss race_white race_white_miss hsloc_1 hsloc_2 hsloc_3 hsses_1 hsses_2 hsses_3 hsrace_1 hsrace_2 hsrace_3 hsach_1 hsach_2 hsach_3 id_coach id_interact

* Generate encoded section number
encode section, gen(section_num)

* Generating variables with missing values
foreach var in ccs_gpa partch_either moedu_colab faedu_colab gender_female race_white age_21ab hsses_1 hsses_2 hsses_3 hsrace_1 hsrace_2 hsrace_3 hsach_1 hsach_2 hsach_3 hsloc_1 hsloc_2 hsloc_3 {
capture drop `var'_miss
gen `var'_miss=1 if `var'==.
replace `var'_miss=0 if `var'!=.
}

* Locals for Dependent Variable
local outcomes_performance "score_dc_avg prop_beh_ack ti_dc_avg prop_redirect su_dc_avg"
local outcomes_survey "beh_rating manage_app_negative manage_app_positive" 

foreach o of varlist `outcomes_performance' `outcomes_survey' {
gen `o'_bs=`o' if time==0
qui bysort id (`o'_bs): replace `o'_bs=`o'_bs[1]
qui sum `o' if spring2019coachingra==0 & time==0
	gen `o'_bs_centered=`o'_bs- r(mean)  
	}
	
* Creating standardized values
foreach o of varlist `outcomes_survey' `outcomes_performance' {
egen `o'_avg = mean(`o') if time==2
qui gsort email -time 
replace `o'_avg= `o'_avg[_n-1] if `o'_avg>= .
qui bysort email: gen `o'_diff=`o'- `o'_avg
egen `o'_sd = sd(`o') if time==2 &  spring2019coachingra==0
qui gsort email -time 
replace `o'_sd= `o'_sd[_n-1] if `o'_sd>= .
qui bysort email: gen `o'_z=`o'_diff/`o'_sd
}


* Saving as descriptive dataset
save "Final Analytic files/Performance_Survey_Randomization_CPP_Final_Descriptive.dta", replace


* Replacing missing covariate information
replace age_21ab=0 if age_21ab==.
replace race_white=0 if race_white==.
replace hsses_1=0 if hsses_1==.
replace hsses_2=0 if hsses_2==.
replace hsses_3=0 if hsses_3==.
replace hsach_1=0 if hsach_1==.
replace hsach_2=0 if hsach_2==.
replace hsach_3=0 if hsach_3==.
replace partch_either=0 if partch_either==.
replace moedu_colab=0 if moedu_colab==.
replace faedu_colab=0 if faedu_colab==.
replace gender_female=0 if gender_female==.
replace gender_female_miss=1 if gender_female_miss==.


* Saving as analytic dataset
save "Final Analytic files/Performance_Survey_Randomization_CPP_Final_Analytic.dta", replace
