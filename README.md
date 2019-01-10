# NBAPlusMinusAnalysis
Reads through NBA play-by-play text documents and parses through the given data to find every NBA player's real plus/min (RPM), the point value a player adds/subtracts when they're playing in a game, for an entire 82 game NBA season recorded as a CSV output file. 

My friend @gct38 and I participated in an NBA hackathon last summer and wrote this program. The hardest challenge was that free throws count toward the plus/minuses of the players that were on the court for the foul, not for the substituted in players during the free throws. We solved this by creating a "queue" to store pending substitutions and applying them following the free throws.

# Provided Data:
- NBA Hackathon – Event Codes.txt
o This dataset provides look up values for the event message types and action types found in the play by play dataset. Each code is converted to an English language description of the event.

- NBA Hackathon – Game Lineup Data Sample (50 Games).txt
o This dataset provides start of period player availability.
▪ Game_id – A unique game code for each game
▪ Period (Quarter) – The associated period of the line up (overtime period are indicated by values greater than 4)
▪ Person_id – A unique identifier for each player
▪ Team_id – A unique identifier for each team
▪ Status – A variable indicating whether a player is active (A) or inactive (I)

- NBA Hackathon – Play by Play Sample (50 Games).txt
o This dataset provides play by play information on the event level for each game.
o To properly sort the events in a game use the following sequence of sorted columns: Period (ascending), PC_Time (descending), WC_Time (ascending), Event_Number (ascending)
▪ Event_Number – An ordered counter for each event in a game. Note, this number may not be perfectly sequential so please use the sorting methodology outlined above
▪ Event_Msg_Type, Action_Type – Coded descriptions of what happened during the event
▪ WC_Time – The in-arena time of the event in Unix format. It is coded in tenths of a second.
▪ PC_Time – The time on the game clock in tenths of a second (e.g. 7200 corresponds to 720 seconds/12 minutes remaining in the quarter)
▪ Option 1 – On a shot attempt, this column will tell you the point value of the shot
• On free throw attempts, if the value in this column is 1, it means it was a made free throw, otherwise, it was missed.
▪ Person1, Person2 – The person_ids of the players who are directly associated with the event (e.g. If the event is an assisted made basket, Person1 is the shot maker and Person2 is the player who assisted)
• In the case of a substitution, the Event_Msg_Type will be 8, Person1 will be the ID for the player leaving the game, and Person2 will be the ID for the player entering the game.
▪ Team_id – In most scenarios, this is the Team ID associated with the Person1 column. However, there are instances when this is not the case. To accurately and consistently identify a player’s team, we suggest merging in the Game Lineup dataset on the Person1 and Person2 columns.

- output.csv
o This is the resulting file with the plus/minuses of all of the players in the given games


