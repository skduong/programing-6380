import numpy as np

#loading the data from insurance.txt
dtype1 = np.dtype([('age', 'i'), ('sex','U6'), ('bmi','f'), ('children', 'i'), ('smoker', 'U3'), ('region','U10'), ('expenses','f')])
data = np.loadtxt('insurance.txt', dtype=dtype1, skiprows=1)

#give mean, sd, and median for a feature of the data
def stats(dataset, feature):
    return round(np.mean(dataset[feature]),4), round(np.std(dataset[feature]),4), np.median(dataset[feature])

#1 age stats 
ageStats = ('All\t', 'age') + stats(data, 'age')

#2 BMI stats
bmiStats = ('All\t', 'BMI') +stats(data,'bmi')
    
#3 BMI stats by gender
females = data[data['sex']=='female']
males = data[data['sex']=='male']

femaleBMIstats = ('females\t', 'BMI') + stats(females,'bmi')
maleBMIstats = ('males\t', 'BMI') + stats(males,'bmi')

#4 BMI stats by smoker/nonsmoker
smokers = data[data['smoker']=='yes']
nonsmokers = data[data['smoker']=='no']

smokerBMIstats = ('smokers\t', 'BMI') + stats(smokers, 'bmi')
nonsmokerBMIstats = ('nonsmokers', 'BMI') + stats(nonsmokers, 'bmi')

#5 BMI stats by region
ne = data[data['region']=='northeast']
nw = data[data['region']=='northwest']
se = data[data['region']=='southeast']
sw = data[data['region']=='southwest']

neBMIstats = ('northeast', 'BMI') + stats(ne, 'bmi')
nwBMIstats = ('northwest', 'BMI') + stats(nw, 'bmi')
seBMIstats = ('southeast', 'BMI') + stats(se, 'bmi')
swBMIstats = ('southwest', 'BMI') + stats(sw, 'bmi')

#6 BMI stats for those with more than 2 children
moreChildren = data[data['children']>2]
childrenBMIstats = ('children>2', 'BMI') + stats(moreChildren, 'bmi')

#saving to file
np.savetxt('output.txt', [ageStats, bmiStats, femaleBMIstats, maleBMIstats, 
                          smokerBMIstats, nonsmokerBMIstats, neBMIstats,
                          nwBMIstats, seBMIstats, swBMIstats, childrenBMIstats],
           fmt='%s', delimiter='\t', header = 'Group\t\tFeature\tMean\t SD\tMedian',
           comments ='')

#examining expenses
data[::-1].sort(order='expenses')
top20 = data[:len(data)//5].copy() #top 20% expenses
rest80 = data[len(data)//5:].copy() #rest of the 80%

#mean and sd for bmi
meanBMItop20 = np.mean(top20['bmi'])
sdBMItop20 = np.std(top20['bmi'])
meanBMIrest80 = np.mean(rest80['bmi'])
sdBMIrest80 = np.std(rest80['bmi'])

#mode for smokers and region
smoke20, smokecount20 = np.unique(top20['smoker'], return_counts=True)        #getting counts of each answer        
modeSmokerTop20 = smoke20[np.where(smokecount20[0]>smokecount20[1], 0, 1)]        #choosing answer with max count
region20, counts20 = np.unique(top20['region'], return_counts=True)       #getting counts of each region
modeRegionTop20 = region20[np.argmax(np.where(np.max(counts20), counts20, region20))]         #choosing region with max count

smoke80, smokecount80 = np.unique(rest80['smoker'], return_counts=True)
modeSmokerRest80 = smoke80[np.where(smokecount80[0]>smokecount80[1], 0, 1)]
region80, counts80 = np.unique(rest80['region'], return_counts=True)
modeRegionRest80 = region80[np.argmax(np.where(np.max(counts80), counts80, region80))]