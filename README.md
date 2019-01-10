# NBAPlusMinusAnalysis
Reads through NBA play-by-play text documents and parses through the given data to find every NBA player's real plus/min (RPM), the point value a player adds/subtracts when they're playing in a game, for an entire 82 game NBA season recorded as a CSV output file. 

My friend @gct38 and I participated in an NBA hackathon last summer and wrote this program. The hardest challenge was that free throws count toward the plus/minuses of the players that were on the court for the foul, not for the substituted in players during the free throws. We solved this by creating a "queue" to store pending substitutions and applying them following the free throws.


