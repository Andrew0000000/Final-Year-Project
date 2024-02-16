# print head of new module dataset
import pandas as pd

df1 = pd.read_csv('data/jobDescriptionData.csv')
col1 =     ['Select module',
    'PGTA hours excluding marking',
    'Marking hours excluding end of year exam (if required)',
    'Marking hours for end of year exam (if required)',
    'Duties']

df2 = pd.read_csv('data/newModuleData.csv')
print(df2.head())