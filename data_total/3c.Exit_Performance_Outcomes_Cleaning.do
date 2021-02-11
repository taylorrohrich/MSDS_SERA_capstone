********************************************************************************
* Cleaning video coding scores
*
* Spring Behavioral Redirections Study - exit simulations
* 
* Created by AKC on 08/07/2019
********************************************************************************

/* Notes:	This do file cleans raw Qualtrics data that was collected from 
			raters who coded and scored videos of teacher candidates in the 
			simulator during the Spring 2019 Behavioral Redirections Study. This
			data includes exit simulations. 
			
*/

/*	location of Box sync folder
	global root_drive "D:\Box Sync\Project SimTeacher\9. Data\2018-19"
	
	*location of raw data 
	global raw_data "${root_drive}/Raw Data Exports"
	
	*location of working data files
	global working "${root_drive}/Data"

	cd "${root_drive}"

*/

cd "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/Coded performance outcomes"

import delimited "Raw excel data/2019 Spring- Exit- Behavioral Redirections_August 7, 2019_08.26.csv", bindquote(strict) varnames(1) clear

** Renaming all variables to lower case 
    rename *, lower
	
** Dropping irrelevant variables	
	drop startdate-finished 
	drop responseid-userlanguage
	
** Dropping first two rows of data
	drop in 1/2
	
** Renaming variables
	rename q25      first_beh
	rename q2		cid
	rename q3		id
	rename q41_1	b1oc
	rename q41_2	b2oc
	rename q41_3	b3oc
	rename q41_4	b4oc
	rename q41_5	b5oc
	rename q41_6	b6oc
	rename q42_1	b1ac
	rename q42_2	b2ac
	rename q42_3	b3ac
	rename q42_4	b4ac
	rename q42_5	b5ac
	rename q42_6	b6ac
	rename q43_1_1	b1ti
	rename q43_2_1	b2ti
	rename q43_3_1	b3ti
	rename q43_4_1	b4ti
	rename q43_5_1	b5ti
	rename q43_6_1	b6ti
	rename q44_1	b1sp
	rename q44_2	b2sp
	rename q44_3	b3sp
	rename q44_4	b4sp
	rename q44_5	b5sp
	rename q44_6	b6sp
	rename q45_1	b1cu
	rename q45_2	b2cu
	rename q45_3	b3cu
	rename q45_4	b4cu
	rename q45_5	b5cu
	rename q45_6	b6cu
	rename q46_1	b1re
	rename q46_2	b2re
	rename q46_3	b3re
	rename q46_4	b4re
	rename q46_5	b5re
	rename q46_6	b6re
	rename q47_1_1	b1su
	rename q47_2_1	b2su
	rename q47_3_1	b3su
	rename q47_4_1	b4su
	rename q47_5_1	b5su
	rename q47_6_1	b6su
	rename q5		affect
	rename q6		descript
	rename q7		score
	rename q8		rationale

** Cleaning id variable
    drop if id==""
	replace id = regexr(id, "2019_", "")
	replace id = regexr(id, "_8", "")
	
** Generating session id 
   gen sid="8"
   generate vid= id + "_" + sid + "TC"
   destring id sid, replace
   order sid vid, a(id)

   ** Step 2 (Generating score variables)
	foreach var of varlist b1oc - b6ac {
	replace `var' = "1" if `var'=="Yes"
	replace `var' = "0" if `var'=="No" 
	replace `var' = "." if `var'=="" 
	destring `var', replace
	}

	foreach var of varlist b1sp - b6cu {
	replace `var' = "1" if `var'=="Yes"
	replace `var' = "0" if `var'=="No" 
	replace `var' = "." if `var'==""
	destring `var', replace
	}
	
	foreach var of varlist b1re - b6re {
	replace `var' = "1" if `var'=="Next behavior"
	replace `var' = "2" if `var'=="Sim ended" 
	replace `var' = "." if `var'=="" 
	destring `var', replace
	}
	
	foreach var of varlist b1ti - b6ti {
	destring `var', replace
	}
	
	foreach var of varlist b1su - b6su {
	destring `var', replace
	}
	
	destring score, replace
	
	replace cid = "1" if cid=="Claire"
	replace cid = "5" if cid=="Rachel L"
	replace cid = "7" if cid=="Andrew"
	replace cid="8" if cid=="Arielle"
	replace cid="9" if cid=="Courtney"
	replace cid="10" if cid=="Mike"
	replace cid="11" if cid=="Rosalie"
	replace cid="12" if cid=="Stephanie"
	replace cid="13" if cid=="Vickie"
	replace cid = "." if cid==""
	destring cid, replace 
	
** Labeling values

	label define yesno 1 "Yes" 0 "No"
	label values b1oc - b6ac b1sp - b6cu yesno
	
	label define cutoff 1 "Next behavior" 2 "Sim ended"
	label values b1re - b6re cutoff

	label define coders 1 "Claire" 5 "Rachel L" 7 "Andrew" 8 "Arielle" 9 "Courtney" 10 "Mike" 11 "Rosalie" 12 "Stephanie" 13 "Vickie"
	label values cid coders
	
** Computing total scores for each measure

	local measure oc ac sp cu
	foreach stem of local measure {
	egen tot_`stem' = rowtotal(b1`stem' - b6`stem'), missing
	}	
	
	label var tot_oc "Total occurred behaviors"
	label var tot_ac "Total acknowledged behaviors"
	label var tot_sp "Total specific redirections"
	label var tot_cu "Total cut-off redirections"
	
	foreach var of varlist b1re - b6re {
	gen `var'_nb = 1 if `var'==1
	gen `var'_se = 1 if `var'==2
	}

	egen tot_nb = rowtotal(b1re_nb b2re_nb b3re_nb b4re_nb b5re_nb b6re_nb), missing
	egen tot_se = rowtotal(b1re_se b2re_se b3re_se b4re_se b5re_se b6re_se), missing
	
	drop b1re_nb - b6re_se
	
	label var tot_nb "Total next-behavior cutoffs" 
	label var tot_se "Total sim-ended cutoffs"
	
	replace b6ti="." if b6ti=="-"
	destring b6ti, replace
	egen tot_ti = rowtotal(b1ti b2ti b3ti b4ti b5ti b6ti), missing
	label var tot_ti "Total timely, in seconds, for all behaviors"
	
	replace b6su="." if b6su=="-"
	destring b6su, replace
	egen tot_su = rowtotal(b1su b2su b3su b4su b5su b6su), missing
	label var tot_su "Total succinct, in seconds, for all behaviors"

** Computing final outcome measures

* Overall Quality score averaged by coders
    bysort vid: egen score_dc_avg = mean(score)
	label var score_dc_avg "Overall Quality score averaged by coders"

* Proportions of behaviors acknowledged
    by vid: gen prop_beh_ack = tot_ac/tot_oc
	label var prop_beh_ack "Proportions of behaviors acknowledged"
	
* Average timeliness for redirections 
    by vid: gen ti_dc_avg= tot_ti/tot_ac
	label var ti_dc_avg "Average timeliness for redirections"

* Proportions of specific redirections provided
    by vid: gen prop_redirect= tot_sp/tot_ac
	label var prop_redirect "Proportions of specific redirections provided"

* Average succinctness of redirections
    by vid: gen su_dc_avg= tot_su/tot_ac
	label var su_dc_avg "Average succinctness of redirections"
	
** Replacing id as numeric for future merge
	destring id, replace
	duplicates tag vid, gen(double_code)
	
** Generating time variable for exit sessions
    gen time=3
	
** Dropping empty variables
drop q12-q26

** Keeping first observation for each candidate
bysort id time : keep if _n==1

** Step 3: saving cleaned dataset 
save "Working STATA files/Exit_PerformanceOutcomes_Cleaned.dta", replace


	
