import pandas as pd
import quandl, math
import numpy as np # numpy array
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
# Getting rid of some warining
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

# using preprocessing for scaling
# using cross_validation/test_split to create a training and testing sample
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

# Initialize DataFrame contains all Feature of Google Stock
df = quandl.get('WIKI/GOOGL')

# Select needed features
df = df[['Adj. Open','Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
df['Closing_Price'] = df['Adj. Close']

# Hashing new features
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
df = df[['Closing_Price', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

forecast_col = 'Closing_Price'
# As later we are shifting Closing price, at the tail of the table, we won't be getting
# Value that is ahead of its time, so we would need to fill those empty data with a value
# Panda fillna, fill all of the N/A data with a value rather than getting rid of them
df.fillna(-99999, inplace = True)

# Math.ceil rounds off value to its nearest ceil
# 1 percent of the days
forecast_out = int(math.ceil(0.01*len(df)))

# Setting label feature to predict its Closing price 1% days into the future
df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace = True)

# X: feature
# Y: label
# df.drop returns a new copy of a dataFram
# We want to return everything from our original dataframe except the label column
X = np.array(df.drop(['label'], 1))
y = np.array(df['label'])
X = preprocessing.scale(X)  # Feature scaling
y = np.array(df['label'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# classifier using LinearRegression w/ 97% accuracy
clf = LinearRegression()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)



print accuracy



# Display
#
# print "\n"
# print "######################################################################"
# print "#    Display future closing price of a certain stock at given days   #"
# print "######################################################################"
# print "\n"
#
# print df.head()
# print "---------------------------------"
# print df.tail()
