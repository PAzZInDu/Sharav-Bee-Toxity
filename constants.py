LABELS = {0: "Non-Toxic", 1: "Toxic"}

COLUMNS = ["herbicide", "fungicide", "insecticide", "other_agrochemical", "ppdb_level"]

POSSIBLE_NULL_COLUMNS = [
    'MaxPartialCharge', 
    'MinPartialCharge',
    'MaxAbsPartialCharge', 
    'MinAbsPartialCharge', 
    'BCUT2D_MWHI', 
    'BCUT2D_MWLOW', 
    'BCUT2D_CHGHI', 
    'BCUT2D_CHGLO', 
    'BCUT2D_LOGPHI', 
    'BCUT2D_LOGPLOW', 
    'BCUT2D_MRHI', 
    'BCUT2D_MRLOW']


SINGLE_UNIQUE_VALUE_COLUMNS = [
    'SMR_VSA8', 
    'SlogP_VSA9', 
    'fr_HOCCN', 
    'fr_azide', 
    'fr_azo', 
    'fr_barbitur', 
    'fr_benzodiazepine', 
    'fr_diazo', 
    'fr_dihydropyridine', 
    'fr_isocyan', 
    'fr_isothiocyan', 
    'fr_lactam', 
    'fr_nitroso']
