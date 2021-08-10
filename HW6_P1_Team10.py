import pandas as pd
import numpy as np

#(1) read training and test sets
trainDF = pd.read_excel('titanic_traning.xlsx')
testDF = pd.read_excel('titanic_test.xlsx')
features = ['gender', 'pclass', 'sibsp', 'parch', 'embarked']
testDF.dropna(subset = features, inplace = True) #remove blanks; there will be no predictions for these indicies

'''
To build the oneR model:
    1. Get get all the unique values (subFeatures) and count of the desired feature in the training set
    2. For each of those subsets, find the percentage of survived (#survived in the subset/total subset size)
       If that percentage is strictly over 50%, the corresponding subfeature results in survival, death otherwise
    3. decision is a series with index=subfeatures and values=survival(0 or 1). It provides the rules for the model.
    4. Apply this model/rule to each passenger(row) in the testSet 
-> returned is an n vector of 0's and 1's corresponding to each testset passenger's survival based on said feature
'''
#(2)&(3) create oneR model for the features and give decision labels
def oneR(feature, trainSet = trainDF, testSet = testDF):
    subFeatures, subFeatCount = np.unique(trainSet[feature], return_counts=True)
    survival = []
    for i in range(len(subFeatures)):
        subset = trainSet[trainSet[feature] == subFeatures[i]]
        survival += [int(np.sum(subset['survived']==1)/subFeatCount[i] > 0.5)]
    decision = pd.Series(survival, index = subFeatures)
    return testSet[feature].apply(lambda x: decision[x], 1)
 
#(4) Storing the predictions into the given spread sheets
results = pd.ExcelFile('titanic_test_predictions.xlsx')
writer = pd.ExcelWriter('titanic_test_predictions.xlsx')

sheets = results.sheet_names
truths = results.parse(0)['Ground truth'] #true results of test set
acc = [] #accuracy of predictions

#loop through each feature, build their models & get predictions, save them to the Excel file
#at the same time, get accuracies for the feature prediction
for i in range(len(features)):
    selectedResult = results.parse(sheets[i])
    selectedResult['Prediction'] = oneR(features[i])
    acc += [np.sum(selectedResult['Prediction'] == truths)/len(testDF)]
    selectedResult.to_excel(writer, sheet_name = sheets[i], index = False)

#save the accuracies
ratesResults = results.parse('Prediction_Success_Rate')
ratesResults['Success Rate '] = acc
ratesResults.to_excel(writer, sheet_name = 'Prediction_Success_Rate', index = False)

writer.save() #save to the Excel file