# The data should contain events with symbol and variable id with the same value
EVENT_INDEX = 999
TAU_EXP = [2, 3, 10]
W_EXP = [10, 20, 30]

# Input folders and files names
INPUT_FOLDER = 'input'
STI_DATA_FOLDER = 'STI data'
STI_TRAIN_FILE_NAME = 'sti_train.csv'
STI_TEST_FILE_NAME = 'sti_test.csv'
PATTERNS_FILE_NAME = 'patterns.csv'
RAW_DATA_FOLDER = 'Raw data'
RAW_TRAIN_FILE_NAME = 'raw_train.csv'
RAW_Y_TRAIN_FILE_NAME = 'train_class.csv'
RAW_TEST_FILE_NAME = 'raw_test.csv'
RAW_Y_TEST_FILE_NAME = 'test_class.csv'

# Temporal relations
TEMP_REL_BEFORE = 'b'
TEMP_REL_MEETS = 'm'
TEMP_REL_CONTAINS = 'c'
TEMP_REL_EQUALS = 'e'
TEMP_REL_FINISHED_BY = 'f'
TEMP_REL_OVERLAPS = 'o'
TEMP_REL_STARTS = 's'

# Tiep
START_TIEP = '+'
END_TIEP = '-'
REL_TIEP = '<'

# STI data column names
STI_DATA_SERIES_ID_COL_NAME = 'SeriesID'
STI_DATA_VAR_ID_COL_NAME = 'VarID'
STI_DATA_SYM_ID_COL_NAME = 'SymbolID'
STI_DATA_START_TIME_COL_NAME = 'StartTime'
STI_DATA_END_TIME_COL_NAME = 'EndTime'

# Patterns column names
PAT_STIS_COL_NAME = 'STIs'
PAT_TEMP_RELS_COL_NAME = 'TempRels'
PAT_TEMP_VS_COL_NAME = 'VerSupp'
PAT_TEMP_HS_COL_NAME = 'HorSupp'

# Models available
MOD_CLS_SCPM_NAME = 'SCPM'
MOD_CLS_XGB_NAME = 'XGB'
MOD_CLS_FCPM_NAME = 'FCPM'
MOD_REG_GAM_GLM_NAME = 'GammaRegressor'

# Aggregation function
AGG_FUN_MEAN = 'mean'

# Models params


import scipy.stats as ss
MOD_CLS_FCPM_PARAMS = {
    'epsilon': 1,
    'uncertainty_prob': 0.5,
    'sample_to_gen': 10000,  # Number of samples to generate
    'distributions': [ss.expon, ss.weibull_min, ss.lognorm, ss.pareto, ss.halfnorm, ss.exponweib],
    'default_dist': ss.norm,
    'default_dist_param': (0.0, 1.0)
}