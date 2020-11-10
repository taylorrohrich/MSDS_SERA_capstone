import numpy as np
# Constants for data cleaning


COLUMN_NAME_MAP = {
    'q2': 'cid',
    'q3': 'id',
    'q41_1': 'b1oc',
    'q41_2': 'b2oc',
    'q41_3': 'b3oc',
    'q41_4': 'b4oc',
    'q41_5': 'b5oc',
    'q41_6': 'b6oc',
    'q42_1': 'b1ac',
    'q42_2': 'b2ac',
    'q42_3': 'b3ac',
    'q42_4': 'b4ac',
    'q42_5': 'b5ac',
    'q42_6': 'b6ac',
    'q43_1_1': 'b1ti',
    'q43_2_1': 'b2ti',
    'q43_3_1': 'b3ti',
    'q43_4_1': 'b4ti',
    'q43_5_1': 'b5ti',
    'q43_6_1': 'b6ti',
    'q44_1': 'b1sp',
    'q44_2': 'b2sp',
    'q44_3': 'b3sp',
    'q44_4': 'b4sp',
    'q44_5': 'b5sp',
    'q44_6': 'b6sp',
    'q45_1': 'b1cu',
    'q45_2': 'b2cu',
    'q45_3': 'b3cu',
    'q45_4': 'b4cu',
    'q45_5': 'b5cu',
    'q45_6': 'b6cu',
    'q46_1': 'b1re',
    'q46_2': 'b2re',
    'q46_3': 'b3re',
    'q46_4': 'b4re',
    'q46_5': 'b5re',
    'q46_6': 'b6re',
    'q47_1_1': 'b1su',
    'q47_2_1': 'b2su',
    'q47_3_1': 'b3su',
    'q47_4_1': 'b4su',
    'q47_5_1': 'b5su',
    'q47_6_1': 'b6su',
    'q5': 'affect',
    'q6': 'descript',
    'q7': 'score',
    'q8': 'rationale'
}
FACTORS = [
    {"No":0, "Yes":1,".":np.nan},
    {"Next behavior":1, "Sim ended":2,".":np.nan}
]
COLUMN_FACTOR_MAP= {
    'b1oc':0,
	'b2oc':0,
	'b3oc':0,
	'b4oc':0,
	'b5oc':0,
	'b6oc':0,
	'b1ac':0,
	'b2ac':0,
	'b3ac':0,
	'b4ac':0,
	'b5ac':0,
	'b6ac':0,
    'b1sp':0,
	'b2sp':	0,
	'b3sp':	0,
	'b4sp':	0,
	'b5sp':	0,
	'b6sp':	0,
	'b1cu':	0,
	'b2cu':	0,
	'b3cu':	0,
	'b4cu':	0,
	'b5cu':	0,
	'b6cu':	0,
    'b1re':	1,
	'b2re':	1,
	'b3re':	1,
	'b4re':	1,
	'b5re':	1,
	'b6re':	1,
}

COLUMN_INT_MAP = [
    'b1ti',
   'b2ti',
    'b3ti',
    'b4ti',
   'b5ti',
    'b6ti',
    'b1su',
   'b2su',
     'b3su',
   'b4su',
   'b5su',
   'b6su',
]
CID_MAP={
    "Claire":1,
    "Helen":2,
    "Maggie":3,
    "Rachel G": 4,
    "Rachel L": 5,
    "Sarah": 6,
    "Kelly":7,
    "Rebekah":8,
    7 "Andrew" 8 "Arielle" 9 "Courtney" 10 "Mike" 11 "Rosalie" 12 "Stephanie" 13 "Vickie"
    ".":np.nan
}

BEHAVIOR_OCCURED_COLUMNS = ['b1oc','b2oc','b3oc','b4oc','b5oc','b6oc']
BEHAVIOR_ACKNOWLEDGED_COLUMNS = ['b1ac','b2ac','b3ac','b4ac','b5ac','b6ac']
BEHAVIOR_SPECIFIC_COLUMNS = ['b1sp','b2sp','b3sp','b4sp','b5sp','b6sp']
BEHAVIOR_CUTOFF_COLUMNS = ['b1cu','b2cu','b3cu','b4cu','b5cu','b6cu']
BEHAVIOR_CUTOFF_REASON_COLUMNS = ['b1re','b2re','b3re','b4re','b5re','b6re']
BEHAVIOR_TIMELY_COLUMNS = ['b1ti','b2ti','b3ti','b4ti','b5ti','b6ti']
BEHAVIOR_SUCCINT_COLUMNS = ['b1su','b2su','b3su','b4su','b5su','b6su']

BEHAVIOR_COLUMNS = zip(['tot_oc','tot_ac','tot_sp','tot_cu','total_nb_se','tot_ti','tot_su'], [BEHAVIOR_OCCURED_COLUMNS,
            BEHAVIOR_ACKNOWLEDGED_COLUMNS,
            BEHAVIOR_SPECIFIC_COLUMNS,
            BEHAVIOR_CUTOFF_COLUMNS,
            BEHAVIOR_CUTOFF_REASON_COLUMNS,
            BEHAVIOR_TIMELY_COLUMNS,
            BEHAVIOR_SUCCINT_COLUMNS])

CALCULATED_COLUMNS= zip(['score_dc_avg','prop_beh_ack','ti_dc_avg','prop_redirect','su_dc_avg'],
    [['score'],['tot_ac','tot_oc'],['tot_ti','tot_ac'],['tot_sp','tot_ac'],['tot_su','tot_ac']])