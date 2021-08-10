import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None) #to ensure all rows are displayed
#Part 1: Read in data
train = pd.read_csv("titanic_traning.csv")
features = train.columns
features = features.drop(["ID"])
total_n = train["ID"].count()
#Part 2: Identify severity of missing and inconsistent values
IV=pd.DataFrame(columns=features)   #Create empty frame to store inconsistent values
table = pd.DataFrame(index= features, columns= ["Missing Values MV", "% of MV", "Inconsistency Values (IV)", "% of IV"])    #Creating table for part 2
err_table = pd.DataFrame(columns = train.columns)   #Create dataframe to hold inconsistent and missing values
for feature in features:  
    if feature == "pclass":
        IV = train[~(train[feature].isna() | train[feature].isin([1, 2, 3]))]
    elif feature == "sex":
        IV = train[~(train[feature].isna() | train[feature].isin(['male', 'female']))]
    elif feature == "age":
        IV = train[~(train[feature].isna() | train[feature]<20)]
    elif feature == "sibsp":
        IV = train[~(train[feature].isna() | train[feature]<20)]
    elif feature == "parch":
        IV = train[~(train[feature].isna() | train[feature]<20)]
    elif feature == "fare":
        IV = train[~(train[feature].isna() | (train[feature]>=0) & (train["fare"]<1000))]
    elif feature == "embarked":
        IV = train[~(train[feature].isna() | train[feature].isin(['C', 'S', 'Q']))]
    elif feature == "survived":
        IV = train[~train[feature].isin([0, 1])]  
    MV = train[train[feature].isna()]    
    if not IV.empty:
        err_table = err_table.append(IV)        
    if not MV.empty:
        err_table = err_table.append(MV)  
    #Filling table for part 2 
    table.loc[feature][0] = MV["ID"].count()
    table.loc[feature][1] = (MV["ID"].count()/total_n)*100 #gives percentage of MV within feature
    table.loc[feature][2] = IV["ID"].count()
    table.loc[feature][3] = (IV["ID"].count()/total_n)*100 #gives percentage of IV within feature
#Part 3: List/Display table and missing/inconsistent values
print(table, '\n\n', err_table)
for feature in features:
    #Part 4: Handle missing values
    if table.loc[feature][0]!=0:
        if train[feature].dtype == np.float64: 
            train[feature].fillna(round(train[feature].mean(),1), inplace=True) #fills NaN values with mean
        elif train[feature].dtype == np.str:
            train[feature] = train[feature].fillna(train[feature].mode()[0]) #fills NaN values with mode
    #Part 5: Handle inconsistent values
    if table.loc[feature][2]!=0:
        if feature == "sex":
            train[feature] = train[feature].str.lower()
        elif feature == "embarked":
            train[feature] = train[feature].str[0]

#Part 6: Store clean data in CSV        
train.to_csv("titanic_training_new.csv", index = False)