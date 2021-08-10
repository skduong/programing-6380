#open the file and read its content, separating each listed team by a new line
infile = open('WorldSeriesWinners.txt').read().split('\n')
#Adding semicolon to each name
infile = [item + ':' for item in infile]
#Creating a years list
years = list(range(1903, 2010))
years.remove(1904)
years.remove(1994)

pairs=[(infile[i],years[i]) for i in range(0, len(infile))]
#initialize the dictionary of winning teams and their corresponding win years
teams = dict()
for key, value in pairs:
	if key not in teams:
		teams[key] = []	
	teams[key].append(value)

#(part 1) print header and separator, followed by the win years
print('------------------------------------------\nTeams: \t Win Years'.expandtabs(32))
print('------------------------------------------')
for team, winyears in sorted(teams.items()): 
	#team(s) with longer list of wins (eg.New York Yankees) have their years printed in 2 lines for neatness
	if len(winyears) < 15:
		print('%-*s' %(32, team), winyears)
	else:
		print('%-*s' %(32, team), winyears[0:13], '\n\t'.expandtabs(32), winyears[14:])

#list of teams and their total win count, which is then sorted and turned into a dictionary
winCount = [[infile.count(team), team] for team in infile]
winCount = dict((teams, wins) for wins, teams in sorted(winCount, reverse=True))

#(part 2) print a header with the corresponding total wins  
print('\n-------------------------------------------\nTeams: \t Total Wins'.expandtabs(30))
print('-------------------------------------------')
for team, wins in winCount.items():
	print('%-*s %i' %(32, team, wins))

#(part 3) print header and the star/bar graph using the same info from part 2
print('\n--------------------------------------------------\nTeams: \t Total Wins Bar Graph'.expandtabs(28))
print('--------------------------------------------------')
for team, wins in winCount.items():
	print('%-*s %s' %(28, team[:-1]+'('+str(wins)+'):', '*'*wins))
	