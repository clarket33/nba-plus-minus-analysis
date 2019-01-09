#progarm that reads through data from NBA Games to calculate players'
#plus/minuses in every single game
#Thomas Clarke, Gordon Tsang

#quarterly changes in lineups, at the start of every quarter
#puts in the players that were listed as quarter starters in
#the Lineup file
def changeLineup(new, name, games, curGame):
    curLineup = games[curGame][name][0].copy()
    bench = games[curGame][name][1].copy()
    for player in curLineup:
        found = False
        for newP in new:
            if newP == player[0]:
                found = True
        if found == False:
            games[curGame][name][0].remove(player)
            games[curGame][name][1].append(player)
            
    for newP in new:
        found = False
        for player in games[curGame][name][0]:
            if newP == player[0]:
                found = True
        if found == False:
            for b in bench:
                if b[0] == newP:
                    games[curGame][name][0].append(b)
                    games[curGame][name][1].remove(b)                    


#takes in two players from the same team and takes the player from the bench 
#and puts him with the starters, and vice versa
def substitute(teamName, playerOut, playerIn, games, curGame):
    curLineup = games[curGame][teamName][0].copy()
    bench = games[curGame][teamName][1].copy()  
    for b in bench:
        if b[0] == playerIn:
            games[curGame][teamName][0].append(b)
            games[curGame][teamName][1].remove(b)
            
    for c in curLineup:
        if c[0] == playerOut:
            games[curGame][teamName][1].append(c)
            games[curGame][teamName][0].remove(c)
            
            
    
    

if __name__ == "__main__":
    
    fileDataGames = open("NBA Hackathon - Game Lineup Data Sample (50 Games).txt", "r")
    filePlayByPlay = open("NBA Hackathon - Play by Play Data Sample (50 Games).txt", "r")
    count = 0
    
    games = dict()
    playerToTeam = dict()
    quarterStarters = dict()
    #assigns each game to two teams, and each team has a tuple of lists
    #with starters in the first list and bench players in the second
    #sets up secondary dictionary within the game ID dictionary, with the team names being keys
    for line in fileDataGames:
            if count == 0:
                count += 1
                continue
            stats = line.strip().split("\t")
            playerToTeam[stats[2]] = dict()
            games[stats[0]] = dict()
            quarterStarters[stats[0]] = dict()
    
    count = 0
    fileDataGames = open("NBA Hackathon - Game Lineup Data Sample (50 Games).txt", "r")
    #puts a tuple of two lists(currently playing and bench) at each team key for every game
    for line in fileDataGames:
        if count == 0:
            count += 1
            continue
        stats = line.strip().split("\t")
        playerToTeam[stats[2]][stats[0]] = stats[3]
        found = False
        for team in games[stats[0]]:
            if team == stats[3]:
                found = True
        if found == False:
            games[stats[0]][stats[3]] = list(), list()
            quarterStarters[stats[0]][stats[3]] = dict()
            quarterStarters[stats[0]][stats[3]] = dict()
            quarterStarters[stats[0]][stats[3]]['2'] = list()
            quarterStarters[stats[0]][stats[3]]['3'] = list()
            quarterStarters[stats[0]][stats[3]]['4'] = list()  
            quarterStarters[stats[0]][stats[3]]['5'] = list()  

    
    count = 0
    fileDataGames = open("NBA Hackathon - Game Lineup Data Sample (50 Games).txt", "r")
    #fills the list with starters and bench players, sets up a quarterStarters
    #dictionary that holds each teams starters at the start of every quarter change in
    #every game
    for line in fileDataGames:
        if count == 0:
            count += 1
            continue
        stats = line.strip().split("\t")
        found = False
        if stats[1] == '2':
            quarterStarters[stats[0]][stats[3]]['2'].append(stats[2])
        elif stats[1] == '3':
            quarterStarters[stats[0]][stats[3]]['3'].append(stats[2])  
        elif stats[1] == '4':
            quarterStarters[stats[0]][stats[3]]['4'].append(stats[2])
        elif stats[1] == '5':
            quarterStarters[stats[0]][stats[3]]['5'].append(stats[2])
        for player in games[stats[0]][stats[3]][0]:
            if player[0] == stats[2]:
                found = True
        for player in games[stats[0]][stats[3]][1]:
            if player[0] == stats[2]:
                found = True
        if found == False:
            if stats[1] == '1':
                games[stats[0]][stats[3]][0].append((stats[2],0))
            else:                
                games[stats[0]][stats[3]][1].append((stats[2],0))
                
    fileDataGames.close() 
    count = 0
    prevPeriod = '1'
    curGame = ""
    prevGame = ""
    preserveNewLineup = list()
    chain = False
    teamName = None
    playerIn = None
    playerOut = None
    stringOfEights = False
    for line in filePlayByPlay:
            if count == 0:
                count += 1
                continue
            stats = line.strip().split("\t")
            #get rid of stats we don't need to calculate plus/minus
            if len(stats) == 14:
                del stats[13]
                del stats[10]
                del stats[9]
                del stats[8]
                del stats[5]
                del stats[4]
                del stats[1]                 
            #12 is a beginning game state, "6bcf6c1f8c373d25fca1579bc4464a91" seems to be a filler when no players involved
            #"749aad766c8aa13d72db0636afc9bfa6" and "3dcc053c4f1b3eb796205b47647cc12d" seem to mostly call timeouts and they
            #never get subbed in nor do they start a quarter, so they are never put onto the court (maybe coaches?)
            if stats[1] != "12" and stats[5] != "749aad766c8aa13d72db0636afc9bfa6" and stats[5] != "3dcc053c4f1b3eb796205b47647cc12d" and \
               stats[5] != "6bcf6c1f8c373d25fca1579bc4464a91":
                team1 = list(games[stats[0]].keys())[0]
                team2 = list(games[stats[0]].keys())[1]            
                curGame = stats[0]    
                
                
                
                #if it's a new quarter
                if prevPeriod != stats[2] and curGame == prevGame:
                    neededLineup1 = quarterStarters[stats[0]][team1][stats[2]]
                    neededLineup2 = quarterStarters[stats[0]][team2][stats[2]]
                    changeLineup(neededLineup1, team1, games, curGame)
                    changeLineup(neededLineup2, team2, games, curGame)
                if prevGame != curGame:
                    preserveNewLineup.clear()
                    chain = False
                    stringOfEights = False
                
                #if it is the first free throw of a set of free throws, begin a chain of
                #withholding subs until the free throws are over
                if(stats[1] == '3' and (stats[3] == '11' or stats[3] == '13' or \
                                         stats[3] == '21' or stats[3] == '25' or \
                                         stats[3] == '18' or stats[3] == '10' or \
                                         stats[3] == '16' or stats[3] == '17' or \
                                         stats[3] == '27')):
                    chain = True
                    stringOfEights = False
                
                
                if stats[1] == "8":
                    if chain == False:
                        stringOfEights = True
                    #if a player is coming into the game that is not saved on the current team's roster
                    if playerToTeam.get(stats[6]) == None:
                        possNewPlayer = stats[6]
                        possTeam = playerToTeam[stats[5]][curGame]                       
                        playerToTeam[possNewPlayer] = dict()
                        playerToTeam[possNewPlayer][curGame] = possTeam
                        games[stats[0]][possTeam][1].append((possNewPlayer, 0))
                    elif playerToTeam.get(stats[6]).get(curGame) == None:
                        possNewPlayer = stats[6]
                        possTeam = playerToTeam[stats[5]][curGame]                       
                        playerToTeam[possNewPlayer][curGame] = possTeam
                        games[stats[0]][possTeam][1].append((possNewPlayer, 0))                        

                    #substitute from the bench of the team 
                    teamName = playerToTeam[stats[5]][curGame] 
                    playerOut = stats[5]
                    playerIn = stats[6]
                    
                    substitute(teamName, stats[5], stats[6], games, curGame)
                    
                    
                    
                #if there has been a number of subs in a row(or just 1 in a row)
                #check if the current command is a sub, if it is, 
                #add it to the queue of subs and reverse the original substituion
                #just in case it is a part of a chain of free throws
                #if the command isn't a sub and it isn't a part of a chain of free throws,
                #send the subs in
                if(stringOfEights == True and chain == False):                  
                    if stats[1] == '8':
                        preserveNewLineup.append((playerOut,playerIn, teamName))
                        substitute(teamName, playerIn, playerOut, games, curGame) 
                    else:
                        stringOfEights = False
                        for l in preserveNewLineup:
                            substitute(l[2], l[0], l[1], games, curGame)
                        preserveNewLineup.clear() 
                
    
                    
                #if we are in the middle of free throws and a sub happens, reverse the sub
                #that happened and add it to the queue
                if(chain == True):
                    if stats[1] == '8':                       
                        preserveNewLineup.append((playerOut,playerIn, teamName))
                        substitute(teamName, playerIn, playerOut, games, curGame)  
                    
                
                
                #if there are points scored, assign the proper additions and deductions
                #to both teams
                if stats[4] != "0":
                    if stats[4] != '1' and stats[1] == 3:
                        break
                    scoringTeam = playerToTeam[stats[5]][curGame]
                    if scoringTeam == team1:
                        for p in range(len(games[stats[0]][team1][0])):
                            pM1 = games[stats[0]][team1][0][p][1] + int(stats[4])
                            games[stats[0]][team1][0][p] = (games[stats[0]][team1][0][p][0], pM1)                            
                        for p in range(len(games[stats[0]][team2][0])):
                            pM2 = games[stats[0]][team2][0][p][1] - int(stats[4])
                            games[stats[0]][team2][0][p] = (games[stats[0]][team2][0][p][0], pM2)
                    elif scoringTeam == team2:
                        for p in range(len(games[stats[0]][team2][0])):
                            pM2 = games[stats[0]][team2][0][p][1] + int(stats[4])
                            games[stats[0]][team2][0][p] = (games[stats[0]][team2][0][p][0], pM2)                        
                        for p in range(len(games[stats[0]][team1][0])):
                            pM1 = games[stats[0]][team1][0][p][1] - int(stats[4])
                            games[stats[0]][team1][0][p] = (games[stats[0]][team1][0][p][0], pM1) 
           
                #if you reach the end of a chain of free throws, send all of the subs that were made during the free throws
                #into the game to update their plus/minus for future events
                if(chain == True):
                    if(stats[1] == '3' and (stats[3] == '10' or stats[3] == '12' or \
                                            stats[3] == '15' or stats[3] == '26' or \
                                            stats[3] == '19' or stats[3] == '29' or \
                                            stats[3] == '16' or stats[3] == '17' or \
                                            stats[3] == '20' or stats[3] == '22')):
                        chain = False  
                        for l in preserveNewLineup:
                            substitute(l[2], l[0], l[1], games, curGame)
                        preserveNewLineup.clear()                        
                
                prevGame = curGame
                prevPeriod = stats[2]
              
    filePlayByPlay.close()
    #output results to the csv file
    f = open("Infinity_Guantlets_Q1_BBALL.csv", "w")
    f.write("Game_ID, Player_ID, Player_Plus/Minus\n")  
    for g in list(games.keys()):
        for team in games[g]:
            for roster in games[g][team]:
                for p in roster:
                    f.write(g)
                    f.write(",") 
                    pM = ""
                    if(p[1] > 0):
                        pM += "+"
                    pM += str(p[1])
                    f.write(p[0])
                    f.write(",")
                    f.write(pM)
                    f.write("\n")
    f.close()
        
   
    
    
    
    