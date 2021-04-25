cap prog drop ttest_cov_unwt
set more off
program ttest_cov_unwt, rclass

*********************************************
** COVARIATE T-TEST**************************
*********************************************
syntax [if] [, Treatment(string) Covariates(string) Blocks(string)]
marksample touse
local covariates "gender_female age cumulativegpa race ytrt_overall tse_overall tmas_overall rsq_overall"
local blocks "strata2 strata3"

foreach var of varlist `covariates'{	
	tabstat `var', stat(mean var) by(coaching) save
	return list
		
		matrix coachingstats1 = r(Stat2)
		scalar `var'_tr_mean1 = coachingstats1[1,1]
			scalar `var'_tr_var1 = coachingstats1[2,1] 
			
		matrix coachingstats= r(Stat1)
		scalar `var'_co_mean = coachingstats[1,1]
			scalar `var'_co_var =coachingstats[2,1] 

		reg `var' coaching `blocks'
			scalar diff1 = _b[coaching] 


			scalar `var'_coach_es1 =(`var'_tr_mean1-`var'_co_mean)/sqrt(`var'_co_var)
			scalar `var'_coach_var1 =(`var'_tr_var1/`var'_co_var)
			scalar `var'_tr_sd1=sqrt(`var'_tr_var1)
			scalar `var'_co_sd=sqrt(`var'_co_var)
			
							
	gen `var'_coach_es1 = scalar(`var'_coach_es1)
	gen `var'_coach_var1= scalar(`var'_coach_var1)
}

return list 
end
