import pandas as pd
import quandl

'''
Using quandl.get to get a pandas data frame

Definition:
quandl.get(":database_code/:dataset_code", returns = ":return_format")

Parameters:
The parameter returns can take the following values:

   "numpy" : returns a numpy object
   "pandas" : returns a pandas data frame
When returns is omitted, a pandas dataframe is returned.
'''

#dataframe
df = quandl.get('WIKI/GOOGL')

#Data Cleaning
df = df[['Adj. Open','Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]

# Hashing HL_PCT & PCT_change with our existing data.
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

# Generating new data
df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

print df.head()
