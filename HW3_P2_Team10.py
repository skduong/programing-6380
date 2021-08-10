steps = list(map(float, open('steps.txt').read().split('\n')))

daysInMonth = [0,31,28,31,30,31,30,31,31,30,31,30,31]

print("%s\t %s\t %s\t %s\t" %('Month','Average', 'Minimum', 'Maximum'))
print('=================================================')

for i in range(1, 13) :
	monthlySteps = steps[sum(daysInMonth[0:i]): sum(daysInMonth[0:i+1])]
	print("%2d\t%8.2f\t%8.0f\t%8.0f" %(i, sum(monthlySteps)/daysInMonth[i], min(monthlySteps), max(monthlySteps)))
