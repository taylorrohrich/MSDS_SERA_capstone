********************************************************************************
* Importing and saving raw CPP data
*
* Fall 2018/Spring2019 Cohort
* 
* Created by AKC on 09/07/2019
********************************************************************************

/* Notes:	This do file imports excel files and saves STATA files for raw CPP data from
            the Fall 2018/Spring 2019 cohort
			
*/

/*	location of Box sync folder
	global root_drive "D:\Box Sync\Project SimTeacher\9. Data\2018-19"
	
	*location of raw data 
	global raw_data "${root_drive}/Raw Data Exports"
	
	*location of working data files
	global working "${root_drive}/Data"

	cd "${root_drive}"

*/

cd "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/CPP data"
clear

** CRTSE data
* Importing data
import excel "2018_2019_CRTSE/2018_2019_CRTSE_SummerSecondary_PGMT_4thyrBMT_ItemsRemoved.xls", sheet("Sheet1") firstrow
rename *, lower
destring student, replace
egen crtse_total=rowmean(crtse_05-crtse_41)
drop if student==.
save "2018_2019_CRTSE/2018_2019_CRTSE_Data.dta", replace

** DAS data
* Importing data
import excel "2018_2019_DAS/2018_2019_DAS_SummerSecondary_PGMT_4thyrBMT_Recoded_Missing_ItemNamesRemoved.xls", sheet("Sheet1") firstrow clear
rename *, lower
drop if student==""
destring student, replace
egen das_depression=rowmean(das_03 das_05 das_10 das_13 das_16 das_17 das_21)
egen das_anxiety=rowmean(das_02 das_04 das_07 das_09 das_15 das_19 das_20)
egen das_stress=rowmean(das_01 das_06 das_08 das_11 das_12 das_14 das_18)
save "2018_2019_DAS/2018_2019_DAS_Data.dta", replace

** Demographic data
* Importing and saving demog data
import excel "2018_2019_DemographicSurvey/2018_2019_Demography_Survey_SummerSecondary_PGMT.xls", sheet("Sheet1") firstrow clear
drop if _n==1
rename *,lower
save "2018_2019_DemographicSurvey/2018_2019_Demography_Survey_Data1.dta", replace
* Importing and saving data from 2017-2018 for missing data
import excel "2017_2018_CCS1_DemographySurvey_NumID_NoConsentRemoved.xls", firstrow clear
drop if _n==1
rename *,lower
save "2018_2019_DemographicSurvey/2017_2018_Demography_Survey_Data2.dta", replace
* Appending both datasets
append using "2018_2019_DemographicSurvey/2018_2019_Demography_Survey_Data1.dta"
drop if student=="2176293" & assessed=="16sep2017"
drop if student==""
destring student, replace
* Saving final dataset
save "2018_2019_DemographicSurvey/2018_2019_Demography_Survey_Data.dta", replace 

** FIT data
* Importing data
import excel "2018_2019_FIT/2018_2019_FIT_SummerSecondary_PGMT_4thyrBMT_Recoded_ItemNamesRemoved.xls", sheet("Sheet1") firstrow clear
rename *, lower
drop if student==""
destring student, replace
egen fit_total=rowmean(fit_01-fit_13)
save "2018_2019_FIT/2018_2019_FIT_Data.dta", replace 

** GRIT data
* Importing and saving GRIT data
import excel "2018_2019_GRIT/2018_2019_GRIT_SummerSecondary_PGMT_4thyrBMT_ReverseCoded_OrigRemoved.xls", sheet("Sheet1") firstrow clear
rename *, lower
drop if student==""
destring student, replace
egen grit_total=rowmean(r_grit_02-r_grit_11)
save "2018_2019_GRIT/2018_2019_GRIT_Data.dta", replace

** IMTS data
* Importing and saving IMTS data
import excel "2018_2019_IMTS/2018_2019_IMTS_SummerSecondary_PGMT_4thyrBMT_Missing_ItemNamesRemoved.xls", sheet("Sheet1") firstrow clear
rename *, lower
egen imts_total=rowmean(imts_01-imts_05)
drop if student==""
destring student, replace
save "2018_2019_IMTS/2018_2019_IMTS_Data.dta", replace

** NEO data
* Importing data
import excel "2018_2019_NEO/2018_2019_NEO_SummerSecondary_PGMT_ReverseCoded_OrigRemoved.xls", sheet("Sheet1")firstrow clear
drop if _n==1
drop if student==""
rename *, lower
destring student, replace
destring r_neo_01-neo_60, replace
merge 1:1 student using "Student_Contact_2018_2019.dta", keepusing(email)
drop if _merge==2
drop _merge
save "2018_2019_NEO/2018_2019_NEO1_Data.dta", replace
import excel "2018_2019_NEO/NEO 2017 09 27.xlsx", firstrow clear
drop if _n==1
rename *, lower
rename recipientemail email
* Merging with contact list to get student numbers
merge 1:1 email using "Student_Contact_2018_2019.dta", keepusing(student)
drop _merge
destring student, replace
drop if student==.
*Reverse coding management approaches scale 
destring neo_1-neo_60, replace
foreach var of varlist neo_1 neo_3 neo_8 neo_9 neo_12 neo_14 neo_15 neo_16 neo_18 neo_23 neo_24 neo_27 neo_29 neo_30 neo_31 neo_33 neo_38 neo_39 neo_42 neo_44 neo_45 neo_46 neo_48 neo_54 neo_55 neo_57 neo_59 {
		generate r_`var' = `var'
        recode r_`var' (1=5) (2=4) (4=2) (5=1)
		drop `var'
}
rename r_neo_1 r_neo_01
rename neo_2 neo_02
rename r_neo_3 r_neo_03
rename neo_4 neo_04
rename neo_5 neo_05
rename neo_6 neo_06
rename neo_7 neo_07
rename r_neo_8 r_neo_08
rename r_neo_9 r_neo_09
drop if r_neo_01==.
save "2018_2019_NEO/2018_2019_NEO2_Data.dta", replace
* Appending datasets
append using "2018_2019_NEO/2018_2019_NEO1_Data.dta"
duplicates tag student, gen(dup)
drop if dup>0 & email==""
drop dup
egen neo_n=rowmean(r_neo_01 neo_06 neo_11 r_neo_16 neo_21 neo_26 r_neo_31 neo_36 neo_41 r_neo_46 neo_51 neo_56)
egen neo_e=rowmean(neo_02 neo_07 r_neo_12 neo_17 neo_22 r_neo_27 neo_32 neo_37 r_neo_42 neo_47 neo_52 r_neo_57)
egen neo_o=rowmean(r_neo_03 r_neo_08 neo_13 r_neo_18 r_neo_23 neo_28 r_neo_33 r_neo_38 neo_43 r_neo_48 neo_53 neo_58)
egen neo_a=rowmean(neo_04 r_neo_09 r_neo_14 neo_19 r_neo_24 r_neo_29 neo_34 r_neo_39 r_neo_44 neo_49 r_neo_54 r_neo_59)
egen neo_c=rowmean(neo_05 neo_10 r_neo_15 neo_20 neo_25 r_neo_30 neo_35 neo_40 r_neo_45 neo_50 r_neo_55 neo_60)
save "2018_2019_NEO/2018_2019_NEO_Data.dta", replace
* Merging with missing data to update
use "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/CPP data/2018_2019_NEO/2018_2019_NEO_Missing.dta"
rename *,lower
egen neo_n=rowmean(r_neo_01 neo_06 neo_11 r_neo_16 neo_21 neo_26 r_neo_31 neo_36 neo_41 r_neo_46 neo_51 neo_56)
egen neo_e=rowmean(neo_02 neo_07 r_neo_12 neo_17 neo_22 r_neo_27 neo_32 neo_37 r_neo_42 neo_47 neo_52 r_neo_57)
egen neo_o=rowmean(r_neo_03 r_neo_08 neo_13 r_neo_18 r_neo_23 neo_28 r_neo_33 r_neo_38 neo_43 r_neo_48 neo_53 neo_58)
egen neo_a=rowmean(neo_04 r_neo_09 r_neo_14 neo_19 r_neo_24 r_neo_29 neo_34 r_neo_39 r_neo_44 neo_49 r_neo_54 r_neo_59)
egen neo_c=rowmean(neo_05 neo_10 r_neo_15 neo_20 neo_25 r_neo_30 neo_35 neo_40 r_neo_45 neo_50 r_neo_55 neo_60)
drop assessed assessor
save "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/CPP data/2018_2019_NEO/2018_2019_NEO_Missing_Cleaned.dta", replace
* Merging two datasets
use "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/CPP data/2018_2019_NEO/2018_2019_NEO_Data.dta"
merge 1:1 student using "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/CPP data/2018_2019_NEO/2018_2019_NEO_Missing_Cleaned.dta", update
drop _merge
save "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/CPP data/2018_2019_NEO/2018_2019_NEO_Data.dta", replace

** RSQ data
* Importing data
import excel "2018_2019_RSQ_AdultAttachment/2018_2019_RSQ_SummerSecondary_PGMT_ReverseCoded_OrigRemoved.xls", sheet("Sheet1") firstrow clear
rename *, lower
save "2018_2019_RSQ_AdultAttachment/2018_2019_RSQ1_Data.dta", replace
import excel "2018_2019_RSQ_AdultAttachment/2018_2019_RSQ_Missing.xlsx", firstrow clear
rename *, lower
save "2018_2019_RSQ_AdultAttachment/2018_2019_RSQ2_Data.dta", replace
* appending data
append using "2018_2019_RSQ_AdultAttachment/2018_2019_RSQ1_Data.dta"
replace student="2603880" if name=="Gross,Hannah"
destring student, replace
drop if student==.
egen rsq_total=rowmean(r_rsq_01-rsq_30)
* saving dataset
save "2018_2019_RSQ_AdultAttachment/2018_2019_RSQ_Data.dta", replace

** TMAS data
* Importing data
import excel "2018_2019_TMAS/2018_2019_TMAS_SummerSecondary_PGMT_4thyrBMT_Missing_ReverseCoded_OrigRemoved_ItemNamesRemoved.xls", sheet("Sheet1") firstrow clear
rename *, lower
destring student, replace
drop if student==.
egen tmas_total=rowmean(tmas_01-r_tmas_20)
save "2018_2019_TMAS/2018_2019_TMAS_Data.dta", replace

** TSE data
* Importing data
import excel "2018_2019_TSE/2018_2019_TSE_SummerSecondary_PGMT_4thyrBMT.xls", sheet("Sheet1") firstrow clear
rename *, lower
destring student, replace
drop if student==.
egen tses_se= rowmean(tse_01 tse_02 tse_04 tse_06 tse_09 tse_12 tse_14 tse_22)
egen tses_is= rowmean(tse_07 tse_10 tse_11 tse_17 tse_18 tse_20 tse_23 tse_24)
egen tses_cm= rowmean(tse_03 tse_05 tse_08 tse_13 tse_15 tse_16 tse_19 tse_21)
egen tses_total= rowmean (tse_01 tse_02 tse_04 tse_06 tse_09 tse_12 tse_14 tse_22 tse_07 tse_10 tse_11 tse_17 tse_18 tse_20 tse_23 tse_24 tse_03 tse_05 tse_08 tse_13 tse_15 tse_16 tse_19 tse_21)
save "2018_2019_TSE/2018_2019_TSE_Data.dta", replace

** YTRT data
* Importing data
import excel "2018_2019_YTRT/2018_2019_YTRT_SummerSecondary_PGMT_4thyrBMT_Missing_ItemNamesRemoved.xls", sheet("Sheet1") firstrow clear
rename *, lower
destring student, replace
drop if student==.
egen ytrt_total=rowmean(ytrt_01-ytrt_05)
save "2018_2019_YTRT/2018_2019_YTRT_Data.dta", replace
keep student ytrt_total recipientlastname recipientfirstname 

* Merging all datasets
merge 1:1 student using "2018_2019_CRTSE/2018_2019_CRTSE_Data.dta", keepusing (crtse_total)
drop _merge
merge 1:1 student using "2018_2019_DAS/2018_2019_DAS_Data.dta", keepusing(das_depression das_anxiety das_stress)
drop _merge
merge 1:1 student using "2018_2019_DemographicSurvey/2018_2019_Demography_Survey_Data.dta", keepusing (ccs_gpa-hsach)
drop if _merge==2
drop _merge
merge 1:1 student using "2018_2019_FIT/2018_2019_FIT_Data.dta", keepusing(fit_total)
drop _merge
merge 1:1 student using "2018_2019_GRIT/2018_2019_GRIT_Data.dta", keepusing (grit_total)
drop _merge
merge 1:1 student using "2018_2019_IMTS/2018_2019_IMTS_Data.dta", keepusing (imts_total)
drop _merge 
merge 1:1 student using "2018_2019_NEO/2018_2019_NEO_Data.dta", keepusing (neo_n neo_e neo_o neo_a neo_c)
drop if _merge==2
drop _merge
merge 1:1 recipientlastname recipientfirstname using "2018_2019_RSQ_AdultAttachment/2018_2019_RSQ_Data.dta", keepusing(rsq_total)
drop if _merge==2
drop _merge
merge 1:1 recipientlastname recipientfirstname using "2018_2019_TMAS/2018_2019_TMAS_Data.dta", keepusing(tmas_total)
drop _merge
merge 1:1 recipientlastname recipientfirstname using "2018_2019_TSE/2018_2019_TSE_Data.dta", keepusing(tses_se tses_is tses_cm tses_total)
drop _merge
merge 1:1 recipientlastname recipientfirstname using "2018_2019_YTRT/2018_2019_YTRT_Data.dta", keepusing (ytrt_total)
drop _merge
gen name= recipientlastname+","+ recipientfirstname

* Merging with contact info to get emails and filling in blank emails
merge 1:1 student using "Student_Contact_2018_2019.dta", keepusing(email)
replace email="set9x@virginia.edu" if student==1382103
replace email="sem4u@virginia.edu" if student==1498517
replace email="amh3ej@virginia.edu" if student==2176293
replace email="mih3f@virginia.edu" if student==2200476
replace email="ckb4y@virginia.edu" if student==2437606
replace email="npg7wf@virginia.edu" if student==2468766
replace email="hjk9dr@virginia.edu" if student==2498051
replace email="cjt4te@virginia.edu" if student==2502859
replace email="hwr9ex@virginia.edu" if student==2571818
replace email="rml3x@virginia.edu" if student==2605170
replace email="esw4au@virginia.edu" if student==2699159
replace email="rb2rf@virginia.edu" if student==2699239
replace email="smj6t@virginia.edu" if student==2699474
replace email="hw8kw@virginia.edu" if student==2704548
replace email="hlh9j@virginia.edu" if student==2732302
replace email="cml2zq@virginia.edu" if student==2732372
replace email="amh9gu@virginia.edu" if student==2744059
replace email="mca5hu@virginia.edu" if student==2745617
replace email="leo9um@virginia.edu" if student==2747552
replace email="ncb8q@virginia.edu" if student==2760226
replace email="joh2va@virginia.edu" if student==2761355
replace email="bfd8er@virginia.edu" if student==2762920
replace email="lck4hk@virginia.edu" if student==2766444
replace email="kno9b@virginia.edu" if student==2767343
replace email="oce7ph@virginia.edu" if student==2767980
replace email="es8fa@virginia.edu" if student==2772863
replace email="cc3vm@virginia.edu" if student==2775384
drop _merge

** Step 2: Cleaning data
destring age, replace
gen age_21ab=1 if age==2 | age==3 | age==4 | age==5
replace age_21ab=0 if age==1
gen age_21ab_miss=1 if age!=.
replace age_21ab_miss=0 if age!=.
tab hsloc, gen(hsloc_)
tab hsses, gen(hsses_)
tab hsrace, gen(hsrace_)
tab hsach, gen(hsach_)

replace race="2" if race=="2,5"
replace race="3" if race=="3,5"
destring race, replace
gen race_white=1 if race==5
replace race_white=0 if race!=5 & race!=.
gen race_white_miss=1 if race_white==.
replace race_white_miss=0 if race_white!=.
destring hsses hsach, replace
gen hsses_miss=1 if hsses==.
replace hsses_miss=0 if hsses!=.
gen hsach_miss=1 if hsach==.
replace hsach_miss=0 if hsach!=.

destring partch, replace
gen partch_either=1 if partch!=4 & partch!=.
replace partch_either=0 if partch==4

destring moedu faedu, replace
gen moedu_colab=1 if moedu>2 & moedu!=.
replace moedu_colab=0 if moedu<=2 & moedu!=.
gen faedu_colab=1 if faedu>2 & faedu!=.
replace faedu_colab=0 if faedu<=2 & faedu!=.

gen gender_female=1 if gender=="Female" | gender=="Female " | gender=="female " | gender=="female" | gender=="woman"
replace gender_female=0 if gender=="m" | gender=="male" | gender=="Male"
gen gender_female_miss=1 if gender_female==.
replace gender_female_miss=0 if gender_female!=.
replace ccs_gpa="3.6" if ccs_gpa=="3.6??"
destring ccs_gpa, replace
 
* Saving final dataset
save "2018_2019_CPP_data.dta", replace

* merging with randomization information
merge 1:1 email using "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/CPP data/SimTeacher Randomization Fall 2018 Spring 2019.dta"
drop _merge
save "/Users/ananditakrishnamachari/Desktop/SimTeacher files/SimTeacher_Spring2019/Data/CPP data/SimTeacher Randomization CPP Fall 2018 Spring 2019.dta", replace
