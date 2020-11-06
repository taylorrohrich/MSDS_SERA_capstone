********************************************************************************
* Merging baseline, coaching and exit simulations data 
*
* Spring Behavioral Redirections Study
* 
* Created by AKC on 08/14/2019
********************************************************************************

/* Notes:	This do file merges working STATA files (.dta) for baseline, coaching 
            and exit simulation data for coded performance outcomes from the Spring
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

cd "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/Coded performance outcomes"

** Step 1: Open baseline data
use "Working STATA files/Baseline_PerformanceOutcomes_Cleaned.dta", clear

** Step 2: Merging with coaching data 
append using "Working STATA files/Coaching_PerformanceOutcomes_Cleaned.dta"

** Step 3: Merging exit simulation data
append using "Working STATA files/Exit_PerformanceOutcomes_Cleaned.dta"
replace id_interact="to fill" if id_interact==""
replace id_coach="not applicable" if id_coach==""

** Step 4: Saving as analytic file
save "Final Analytic files/PerformanceOutcomes_Merged.dta", replace

