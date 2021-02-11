********************************************************************************
* Cleaning video coding scores
*
* Fall 2018 Behavioral Redirections Study - baseline
* 
* Created by AKC on 11/28/18
********************************************************************************

/* Notes:	This do file cleans raw Qualtrics data that was collected from five 
			raters who coded and scored videos of teacher candidates in the 
			simulator during the Fall 2018 Behavioral Redirections Study at 
			baseline. 
			
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
clear

* Importing data from Summer 2018
import excel "Raw excel data/Summer 2018 Behavioral Redirections Baseline.xlsx", sheet("Summer 2018 Behavioral Redirect") firstrow

* Cleaning data
rename *, lower
drop if _n==1 | _n==2

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
	
	
** Creating session id and video id
	gen sid = "2" // This is baseline
	gen vid = id + "_" + sid
	destring sid, replace
	
	** Order variables
	order vid id cid sid, first
	
** Labeling variables
	label var vid	"Video id"	// "participant id"_"session id" (e.g., 99_1TC)
	label var id	"id" 		// This is the participant id
	label var cid	"Coder id"
	label var sid	"Session id"
	label var b1oc	"Behavior 1 occurred" 
	label var b2oc	"Behavior 2 occurred"
	label var b3oc	"Behavior 3 occurred"
	label var b4oc	"Behavior 4 occurred"
	label var b5oc	"Behavior 5 occurred"
	label var b6oc	"Behavior 6 occurred"
	label var b1ac	"Behavior 1 acknowledged" 
	label var b2ac	"Behavior 2 acknowledged"
	label var b3ac	"Behavior 3 acknowledged"
	label var b4ac	"Behavior 4 acknowledged"
	label var b5ac	"Behavior 5 acknowledged"
	label var b6ac	"Behavior 6 acknowledged"
	label var b1ti	"Behavior 1 timely"
	label var b2ti	"Behavior 2 timely"
	label var b3ti	"Behavior 3 timely"
	label var b4ti	"Behavior 4 timely"
	label var b5ti	"Behavior 5 timely"
	label var b6ti	"Behavior 6 timely"
	label var b1sp	"Behavior 1 specific"
	label var b2sp	"Behavior 2 specific"
	label var b3sp	"Behavior 3 specific"
	label var b4sp	"Behavior 4 specific"
	label var b5sp	"Behavior 5 specific"
	label var b6sp	"Behavior 6 specific"
	label var b1cu	"Behavior 1 cut off"
	label var b2cu	"Behavior 2 cut off"
	label var b3cu	"Behavior 3 cut off"
	label var b4cu	"Behavior 4 cut off"
	label var b5cu	"Behavior 5 cut off"
	label var b6cu	"Behavior 6 cut off"
	label var b1re	"Behavior 1 reason for cut off"
	label var b2re	"Behavior 2 reason for cut off"
	label var b3re	"Behavior 3 reason for cut off"
	label var b4re	"Behavior 4 reason for cut off"
	label var b5re	"Behavior 5 reason for cut off"
	label var b6re	"Behavior 6 reason for cut off"
	label var b1su	"Behavior 1 succint"
	label var b2su	"Behavior 2 succint"
	label var b3su	"Behavior 3 succint"
	label var b4su	"Behavior 4 succint"
	label var b5su	"Behavior 5 succint"
	label var b6su	"Behavior 6 succint"
	label var affect	"Teacher candidate's affect"
	label var descript	"Description of teacher candidate's behavior"
	label var score	"Overall quality score"
	label var rationale	"Rationale for score given"

	
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
	
	destring b4ti, replace
	destring b2su, replace
	destring b3su, replace
	destring score, replace
	
	replace cid = "7" if cid=="Kelly"
	replace cid = "8" if cid=="Rebekah"
	destring cid, replace 
	
** Labeling values

	label define yesno 1 "Yes" 0 "No"
	label values b1oc - b6ac b1sp - b6cu yesno
	
	label define cutoff 1 "Next behavior" 2 "Sim ended"
	label values b1re - b6re cutoff

	label define coders 1 "Claire" 2 "Helen" 3 "Maggie" 4 "Rachel G" 5 "Rachel L" 6 "Sarah"
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
	
	egen tot_ti = rowtotal(b1ti b2ti b3ti b4ti b5ti b6ti), missing
	label var tot_ti "Total timely, in seconds, for all behaviors"
	
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

** Dropping missing ids
   	drop if id==. & b1oc==.
	
** Dropping videos entered twice (Claire entered codes for a single twice)
    drop if  id==117 & cid==1 & recordeddate=="2018-10-31 13:06:27"

** Generating time variable that indicates baseline sessions
    generate time=0

** Step 3: Saving cleaned dataset
save "Working STATA files/Summer2018_Baseline_PerformanceOutcomes_Cleaned.dta", replace


* Importing data from Fall 2018

import delimited "Raw excel data/Fall 2018 Behavioral Redirections Baseline_July 24, 2019_14.06.csv",  varnames(1) bindquote(strict) encoding(ISO-8859-1) clear

** Step 1 (Data Cleaning)

** Dropping survey preview answers 
drop if status=="Survey Preview"

** Dropping irrelevant variables	
	drop startdate-finished 
	drop responseid-userlanguage
	drop q20-q26
	drop q2-q8
	
** Dropping first two rows of data
	drop in 1/2
	
** Renaming variables
	rename q12		cid
	rename q13		id
	rename q141_1	b1oc
	rename q141_2	b2oc
	rename q141_3	b3oc
	rename q141_4	b4oc
	rename q141_5	b5oc
	rename q141_6	b6oc
	rename q142_1	b1ac
	rename q142_2	b2ac
	rename q142_3	b3ac
	rename q142_4	b4ac
	rename q142_5	b5ac
	rename q142_6	b6ac
	rename q143_1_1	b1ti
	rename q143_2_1	b2ti
	rename q143_3_1	b3ti
	rename q143_4_1	b4ti
	rename q143_5_1	b5ti
	rename q143_6_1	b6ti
	rename q144_1	b1sp
	rename q144_2	b2sp
	rename q144_3	b3sp
	rename q144_4	b4sp
	rename q144_5	b5sp
	rename q144_6	b6sp
	rename q145_1	b1cu
	rename q145_2	b2cu
	rename q145_3	b3cu
	rename q145_4	b4cu
	rename q145_5	b5cu
	rename q145_6	b6cu
	rename q146_1	b1re
	rename q146_2	b2re
	rename q146_3	b3re
	rename q146_4	b4re
	rename q146_5	b5re
	rename q146_6	b6re
	rename q147_1_1	b1su
	rename q147_2_1	b2su
	rename q147_3_1	b3su
	rename q147_4_1	b4su
	rename q147_5_1	b5su
	rename q147_6_1	b6su
	rename q15		affect
	rename q16		descript
	rename q17		score
	rename q18		rationale
	
** Cleaning id variable
	replace id = regexr(id, "_2_TC", "")
	replace id = regexr(id, "_2_2018", "")
	replace id = regexr(id, "2018_", "")
	replace id= "109" if id==" Video ID: 109"
	replace id="56" if id=="46" & cid=="Maggie" 
	replace id="88" if id=="" & cid=="Helen"
	replace id= "107" if id=="" & cid=="" & b1oc=="Yes"
	replace cid="Maggie" if id=="107" 
	
** Creating session id and video id
	gen sid = "2" // This is baseline
	gen vid = id + "_" + sid
	destring sid, replace
	
	** Order variables
	order vid id cid sid, first
	
** Labeling variables
	label var vid	"Video id"	// "participant id"_"session id" (e.g., 99_1TC)
	label var id	"id" 		// This is the participant id
	label var cid	"Coder id"
	label var sid	"Session id"
	label var b1oc	"Behavior 1 occurred" 
	label var b2oc	"Behavior 2 occurred"
	label var b3oc	"Behavior 3 occurred"
	label var b4oc	"Behavior 4 occurred"
	label var b5oc	"Behavior 5 occurred"
	label var b6oc	"Behavior 6 occurred"
	label var b1ac	"Behavior 1 acknowledged" 
	label var b2ac	"Behavior 2 acknowledged"
	label var b3ac	"Behavior 3 acknowledged"
	label var b4ac	"Behavior 4 acknowledged"
	label var b5ac	"Behavior 5 acknowledged"
	label var b6ac	"Behavior 6 acknowledged"
	label var b1ti	"Behavior 1 timely"
	label var b2ti	"Behavior 2 timely"
	label var b3ti	"Behavior 3 timely"
	label var b4ti	"Behavior 4 timely"
	label var b5ti	"Behavior 5 timely"
	label var b6ti	"Behavior 6 timely"
	label var b1sp	"Behavior 1 specific"
	label var b2sp	"Behavior 2 specific"
	label var b3sp	"Behavior 3 specific"
	label var b4sp	"Behavior 4 specific"
	label var b5sp	"Behavior 5 specific"
	label var b6sp	"Behavior 6 specific"
	label var b1cu	"Behavior 1 cut off"
	label var b2cu	"Behavior 2 cut off"
	label var b3cu	"Behavior 3 cut off"
	label var b4cu	"Behavior 4 cut off"
	label var b5cu	"Behavior 5 cut off"
	label var b6cu	"Behavior 6 cut off"
	label var b1re	"Behavior 1 reason for cut off"
	label var b2re	"Behavior 2 reason for cut off"
	label var b3re	"Behavior 3 reason for cut off"
	label var b4re	"Behavior 4 reason for cut off"
	label var b5re	"Behavior 5 reason for cut off"
	label var b6re	"Behavior 6 reason for cut off"
	label var b1su	"Behavior 1 succint"
	label var b2su	"Behavior 2 succint"
	label var b3su	"Behavior 3 succint"
	label var b4su	"Behavior 4 succint"
	label var b5su	"Behavior 5 succint"
	label var b6su	"Behavior 6 succint"
	label var affect	"Teacher candidate's affect"
	label var descript	"Description of teacher candidate's behavior"
	label var score	"Overall quality score"
	label var rationale	"Rationale for score given"
	
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
	
	replace b4ti="." if b4ti=="-"
	destring b4ti, replace
	replace b2su="." if b2su=="-"
	destring b2su, replace
	replace b3su="64" if b3su=="1:04"
	destring b3su, replace
	destring score, replace
	
	replace cid = "1" if cid=="Claire"
	replace cid = "2" if cid=="Helen"
	replace cid = "3" if cid=="Maggie"
	replace cid="4" if cid=="Rachel G"
	replace cid="5" if cid=="Rachel L"
	replace cid="6" if cid=="Sarah"
	replace cid = "." if cid==""
	destring cid, replace 
	
** Labeling values

	label define yesno 1 "Yes" 0 "No"
	label values b1oc - b6ac b1sp - b6cu yesno
	
	label define cutoff 1 "Next behavior" 2 "Sim ended"
	label values b1re - b6re cutoff

	label define coders 1 "Claire" 2 "Helen" 3 "Maggie" 4 "Rachel G" 5 "Rachel L" 6 "Sarah"
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
	
	egen tot_ti = rowtotal(b1ti b2ti b3ti b4ti b5ti b6ti), missing
	label var tot_ti "Total timely, in seconds, for all behaviors"
	
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

** Dropping missing ids
   	drop if id==. & b1oc==.
	
** Dropping videos entered twice (Claire entered codes for a single twice)
    drop if  id==117 & cid==1 & recordeddate=="2018-10-31 13:06:27"

** Generating time variable that indicates baseline sessions
    generate time=0
	
** Step 3: Saving cleaned dataset
save "Working STATA files/Fall2018_Baseline_PerformanceOutcomes_Cleaned.dta", replace

* Merging summer 2018 and fall 2018 data and keeping only one observation per candidate
use "Working STATA files/Summer2018_Baseline_PerformanceOutcomes_Cleaned.dta", clear
append using "Working STATA files/Fall2018_Baseline_PerformanceOutcomes_Cleaned.dta"
bysort id time : keep if _n==1
save "Working STATA files/Baseline_PerformanceOutcomes_Cleaned.dta", replace

