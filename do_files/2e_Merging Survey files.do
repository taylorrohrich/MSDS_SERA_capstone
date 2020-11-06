********************************************************************************
* Importing and cleaning self-report exit survey data for Spring 2019
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

* Reading in Summer 2018 baseline dataset 
use "Working STATA files/Summer2018_Baseline_Post-Survey_Merged_Cleaned.dta", replace

* Append using Fall 2018 baseline dataset
append using "Working STATA files/Fall2018_Baseline_Post-Survey_Cleaned.dta"

* Append using Post-coaching dataset
append using "Working STATA files/Spring2019_Coaching_Post-Survey_Cleaned.dta"

* Append using exit sims dataset
append using "Working STATA files/Spring2019_Exit_Post-Survey_Cleaned.dta"

* Dropping participants who exited the study
drop if email=="bsd7cv@virginia.edu" | email=="bh4fk@virginia.edu" | email=="alh8pk@virginia.edu" | email=="ahm4kv@virginia.edu"

* Saving final dataset
save "Final Analytic files/Fall2018Spring2019_Post-Survey_Cleaned.dta", replace

* Merging with randomization information
merge m:1 email using "Working STATA files/SimTeacher_Randomization_Complete_Fall2018_Spring2019.dta"
drop if _merge!=3
drop _merge

** Merging with CPP covariate data
merge m:1 email using "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/CPP data/2018_2019_CPP_data.dta"
drop if _merge!=3
drop _merge

* Saving final dataset
save "Final Analytic files/SurveyOutcomes_Randomization_CPP_Merged.dta", replace
