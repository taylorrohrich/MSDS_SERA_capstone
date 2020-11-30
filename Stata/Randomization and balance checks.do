********************************************************************************
* Randomizing and balance checks- Fall 2019
* 
* Added by AKC on 09/04/2019    
********************************************************************************
/* Notes:	This do-file randomizes scenario order for Fall 2019 elementary students
            and checks balance
*/

***If running the individual do.file, uncomment and define your directories below.
	
	*location of Box sync folder
	*global root_drive "D:\Box Sync\Project SimTeacher\9. Data\2019-20\Fall2019\Randomization"

* Establishing local directory
cd "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Fall2019/Randomization"

set obs 1000000
set seed 3501

* Reading-in analytic file
use "Working STATA files/2019_2020_RosterDemo_Fall2019_CoachingSessions_Final.dta", clear

* Assigning random numbers
encode program, gen(strata)
bysort strata: generate rannum = uniform()    
sort strata rannum
tab strata, gen(strata)
gen coaching = mod(_n, 2)

label define coaching 0 "Self-Reflection" ///
                       1 "Coaching" 
					   
label values coaching coaching
label variable coaching "Coaching condition"
tab program coaching

* Saving randomization
save "Final Randomization/Randomization_Fall2019_Coaching_Final.dta", replace

* Checking random assignment
local covariates futeaach futearace futeases ///
	                 fustuach fusturace fustuses ///
					 hsach hsrace hsses hsloc ///
					 hstypeother hstype holangother ///
					 holang faedu moedu partch	

* Generating variables
foreach cov in `covariates' {
destring `cov', replace
tab `cov', gen(`cov')
}

* Locals for covariates
local cov_hs1 "hsach1 hsach2 hsach3"
local cov_hs2 "hsses1 hsses2 hsses3 hsloc1 hsloc2 hsloc3"
local cov_futstu "futeaach1 futeaach2 futeaach3 futeases1 futeases2 futeases3"
local cov_paredu "faedu1 faedu2 faedu3 faedu4 faedu5 moedu1 moedu2 moedu3 moedu4 moedu5"
local cov_partch "partch1 partch2"
local cov_tses "tses_overall"

foreach cov in `covariates1' {
regress `cov' i.coaching
}

* Reading in balance
local covariates "gender_female age cumulativegpa race ytrt_overall tse_overall tmas_overall rsq_overall"
include "Do-files/Coaching sessions/cov_balance_unwt_modified_fall2019.do"
ttest_cov_unwt, t(coaching) c(`covariates') b(`blocks')
keep if _n==1
gen id=_n
drop student
drop email-coaching

* Reshaping dataset
reshape long `covariates', i(id) j(coach) string
xpose, varname clear
rename v1 es
rename v2 var
rename _varname variable
drop if _n==1 | _n==2
gen id=_n
*reshape long es var, i(id) j(coach)
rename var variance
drop id
encode variable, gen(nvariable)

* Create Standardized vs Variance Ratio Plot **
		graph twoway ///
			(scatter variance es if es <= .25  & es >= -.25 & variance >.25 & variance <1, mcolor(green) msymbol(circle_hollow) mlabel(nvariable) mlabs(tiny) mlabposition(12)) ///
			(scatter variance es if (es < -.25 | es > .25) | (variance <.25 | variance > 1), mcolor(red) msymbol(circle_hollow) mlabel(nvariable) mlabs(tiny) mlabposition(12)), ///
			xline(.25, lpattern(dot) lwidth(vthin)) ///
			xline(-.25, lpattern(dot) lwidth(vthin)) ///
			yline(.25, lpattern(dot) lwidth(vthin)) ///
			yline(1, lpattern(dot) lwidth(vthin)) ///
			legend(off) xtitle(Effect Size Difference) ytitle(Variance Ratio) ///
			title(RCT Balance Plot) 
