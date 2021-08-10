import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
ecoli = pd.read_excel('Ecoli Data.xlsx') #Importing data

year_df = ecoli.groupby(ecoli['Date Collected'].dt.year)['E.coli'].mean() #getting ecoli mean by year
year_df.plot.bar() #bar chart of ecoli mean by year
plt.title('E.coli Level by Year')
plt.xlabel('Year')
plt.ylabel('Average E.coli Level')
plt.show()

month_df = ecoli.groupby(ecoli['Date Collected'].dt.month)['E.coli'].mean() #getting ecoli mean by aggregated month
month_df = month_df.rename(index = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"})
month_df.plot.bar() #bar chart of ecoli mean by aggregared month
plt.xlabel('Month')
plt.ylabel('Average E.coli Level')
plt.show()

chemcol = ecoli.columns[6:17] #getting chemical columns
for name in chemcol:
    sns.regplot('E.coli', name, data = ecoli, ci = None) #creating scatterplot with regression line for chem col v ecoli
    plt.title('E.coli Level v '+name)
    plt.show()
    
print('Correlation level to E.coli:\n',ecoli[ecoli.columns[[18]+list(range(6,17))]].corr()['E.coli'].to_string(), sep='') #correlation coefficients