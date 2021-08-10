import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

data = pd.read_excel('Superstore.xls')
pages = PdfPages('hw10_graphs.pdf')

def labelplots(xlab, ylab, title, plot):
    plt.xlabel(xlab); plt.ylabel(ylab); plt.title(title); plt.show(); pages.savefig(plot)

#1 discount amount vs profits(in 1,000s of $)
discounts = data[data['Discount']>0] #exclude non-discounts
p1 = plt.scatter(discounts['Discount']*discounts['Sales'], discounts['Profit']/1000, edgecolors='w')
labelplots('Discount Amount', 'Profit(K)', 'Discount vs Sales', p1.figure)

#2 distinguish between profitability
col = np.where(discounts['Profit'] > 0,'tab:orange','b')
p2 = plt.scatter(discounts['Discount']*discounts['Sales'], discounts['Profit']/1000, c=col, edgecolors='w')
labelplots('Discount Amount', 'Profit(K)', 'Discount vs Sales by Profitability', p2.figure)

#3 sales by date (month/year) of order
salesbydate = data.groupby([data['Order Date'].apply(lambda x: x.year), data['Order Date'].apply(lambda x: x.month)])['Sales'].sum()
salesbydate.index = list(map(lambda result: f'{result[1]:02}/{result[0]}'.replace('20',''), salesbydate.index.to_flat_index()))
fig = plt.figure()
axes= fig.add_axes([0.1,0.1,0.8,0.8])
axes.set_ylim([0,550])
axes.set_xticks(list(range(2,49,6)))
axes.set_xticklabels(salesbydate.index[range(2,49,6)])
axes.plot(salesbydate.values/1000, 'b-o')
labelplots('Month of Order Date', 'Sales (K)',  'Month of Order Date vs Sales', fig)

#4 distinguish between profitable and unprofitable sales
posnegsales = data.groupby([data['Order Date'].apply(lambda x: x.year), data['Order Date'].apply(lambda x: x.month),
                           data['Profit'].apply(lambda x: x>0)])['Sales'].sum().unstack()
posnegsales.index = list(map(lambda result: f'{result[1]:02}/{result[0]}'.replace('20',''), posnegsales.index.to_flat_index()))
fig = plt.figure()
axes= fig.add_axes([0.1,0.1,0.8,0.8])
axes.set_ylim([0,550])
axes.set_xticks(list(range(2,49,6)))
axes.set_xticklabels(salesbydate.index[range(2,49,6)])
axes.plot(posnegsales[True].values/1000, 'g-o', label='Positive Profit') 
axes.plot(posnegsales[False].values/1000, 'r-o', label='Negative Profit') 
axes.legend(title = 'Profit Marker', loc="upper right")
labelplots('Month of Order Date', 'Sales (K)', 'Month of Order Date vs Sales', fig)

#5 Products by region
grouped = data.groupby(['Region', 'Product Category'])['Product Category'].count()

labels = list(np.unique(data['Region']))
tech = grouped[:, 'Technology']/data.groupby('Region')['Product Category'].count()
office = grouped[:, 'Office Supplies']/data.groupby('Region')['Product Category'].count()
furniture = grouped[:, 'Furniture']/data.groupby('Region')['Product Category'].count()

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()

#rectangles for each bar
rects1 = ax.bar(x - 2*width/3, round(office*100,2), width, label='Office Supplies', color='orange', edgecolor='w')
rects2 = ax.bar(x + width/3, round(tech*100,2), width, label='Technology', color='r', edgecolor='w')
rects3 = ax.bar(x + 4*width/3, round(furniture*100,2), width, label='Furniture', color='b', edgecolor='w')

ax.set_ylabel('Percent %')
ax.set_title('Products per Region')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(bbox_to_anchor=(1,1), loc="upper left")

#label the bars
for rects in [rects1, rects2, rects3]:
    for rect in rects: #each corresponding to a region
        height = rect.get_height()
        ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), 
                    textcoords="offset points", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
pages.savefig(fig)

#6 Visualize shipping cost for sales and profits
data = data[data['Profit']<20000] #remove any outlier
dot1 = data[data['Shipping Cost'] <= 0]
dot2 = data.loc[(data['Shipping Cost'] > 0) & (data['Shipping Cost'] <= 60)]
dot3 = data.loc[(data['Shipping Cost'] > 60) & (data['Shipping Cost'] <= 120)]
dot4 = data.loc[(data['Shipping Cost'] > 120) & (data['Shipping Cost'] <= 180)]

ax1 = dot1.plot(kind='scatter', x='Sales', y='Profit', s=20, edgecolor='w', label='0.0')    
ax2 = dot2.plot(kind='scatter', x='Sales', y='Profit', s=30, edgecolor='w', label='60.0', ax=ax1) 
ax3 = dot3.plot(kind='scatter', x='Sales', y='Profit', s=50, edgecolor='w', label='120.0', ax=ax1) 
ax4 = dot4.plot(kind='scatter', x='Sales', y='Profit', s=80, edgecolor='w', label='180.0', ax=ax1) 
ax1.legend(title = 'Shipping Cost', loc="lower right")

plt.tight_layout()    
plt.show()
pages.savefig(ax1.figure)

#7 Orders by shipping mode
with sns.axes_style("whitegrid"):
    ax = sns.boxplot(y='Order Quantity', x="Ship Mode", order=['Delivery Truck', 'Express Air', 'Regular Air'], data=data, orient='v')
    pages.savefig(ax.figure)
pages.close()