# This program takes the stand alone game and tests a set of stats, changing one stat (axe low damage range, pot heal amount, ect) every round and 
# send the win/loss percentage rate for every round to an sqlite database. Each test stores value of all stats and if the results are helpful, can be moved to folder called Balancesheets.
# Look at a database set in Balancesheets folder to see results
# This data can be used to balance the stats for the stand alone game

import random
import sqlite3
con = sqlite3.connect('balance_sheet.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS balance(potHeal REAL, axeDam1 REAL, axeDam2 REAL, dag1 REAL, dag2 REAL, dag3 REAL, dag4 REAL, dag5 REAL, dag6 REAL, axeWin REAL, dagWin REAL, potWin REAL, axeWinPer, dagWinPer, potWinPer)')
axeDam = [-100, 155] # Low and high range of axe 
dagDam = [4,19,5,20,20,42] # Low and high range of each of the 3 strikes for the dagger
potHeal = [54] # Amount of health the potion heals
turnMax = 30 # Max number of turns per match
numMatches = 10000 # How many matches will be run with a set of stats before changing test variable. The higher, the closer the data will be to the 'true' win/loss percentage of each set of stats, but the slower the program will run
numRounds = 75 # This is how many times the test variable will be changed 
                #(eg. if the high range of the Axe weapon starts at 100 and numRounds is 150, the win rate of each weapon will be tested at each stat from 100 to 250)
# Two weapons being tested           
weapon1 = "AXE"
weapon2 = "DAG"

def TestVariableChange(): # This runs at the end of each round, altering the test variable so the next round can test the different set of stats
    axeDam[0] += 1

def damCalc(dm,weapon, attack, defend, turn, flip): #Takes each health amount remaining and returns new health remaining after attack
        if weapon == 'AXE':
            damage = round(random.randint(axeDam[0], axeDam[1]) * dm)
            if damage >= 0:
                #print(f"{tur n} did " + str(damage) + " damage!")#
                defend -= damage
            else:
                #print(f"{turn} tripped using the heavy axe and did {damage * -1} to themself.")#
                attack += damage
        if weapon == 'DAG':
            ATT1 = round(random.randint(dagDam[0], dagDam[1]) * dm)
            ATT2 = round(random.randint(dagDam[2], dagDam[3]) * dm)
            ATT3 = round(random.randint(dagDam[4], dagDam[5]) * dm)
            damage = ATT1 + ATT2 + ATT3 
            defend -= damage
            #print(f"{turn} did " + str(ATT1) + ", " + str(ATT2) + ", and " + str(ATT3) + " damage!")#
        if weapon == 'POT':
            heal = round(potHeal[0] * dm)
            attack += heal
            #print(f"{turn} healed " + str(heal))#
        if flip == "flip":    
            return (defend, attack)
        else:
            return (attack, defend)

def winnerIs(p1Wep,p2Wep): # Runs one match and returns winner
    health = [700, 700]
    for i in range(turnMax):
        DM = 1 + (i * .04) #damage multiplier
        health = damCalc(DM, p1Wep, health[0], health[1], "Player 1", "")
        health = damCalc(DM, p2Wep, health[1], health[0], "Player 2", "flip")
        #print(f"Player 1's health is {health[0]} while Player 2's is {health[1]}")#
        if health[0] <= 0:
            return "p2"
            break
        if health[1] <= 0:
            return "p1"
    if health[0] < health[1]:
        return "p2"
    else:
        return "p1"

for i in range(numRounds):
    P1 = 0
    P2 = 0
    for x in range(numMatches):
        if winnerIs(weapon1, weapon2) == "p1": # Based on whcih player wins, adds a win to that counter
            P1 += 1
        else:
            P2 += 1
    #print(str(P1) + " " + str(P2))
    print(i)
    # Converts wins to win percentage
    axeWins = 0
    dagWins = 0
    potWins = 0
    axeWinPer = 0
    dagWinPer = 0
    potWinPer = 0

    if weapon1 == "AXE":
        axeWins = P1
        axeWinPer = axeWins / (axeWins + P2) * 100
        if weapon2 == "DAG":
            dagWins = P2
            dagWinPer = 100 - axeWinPer
        else:
            potWins = P2
            potWinPer = 100 - axeWinPer
    elif weapon1 == "DAG":
        dagWins = P1
        dagWinPer = dagWins / (dagWins + P2) * 100
        if weapon2 == "AXE":
            axeWins = P2
            axeWinPer = 100 - dagWinPer
        else:
            potWins = P2
            potWinPer = 100 - dagWinPer
    else:
        potWins = P1
        potWinPer = potWins / (potWins + P2) * 100
        if weapon2 == "AXE":
            axeWins = P2
            axeWinPer = 100 - potWinPer
        else:
            dagWins = P2
            dagWinPer = 100 - potWinPer        

    cur.execute("INSERT INTO balance VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(potHeal[0], axeDam[0], axeDam[1],dagDam[0],dagDam[1],dagDam[2],dagDam[3],dagDam[4],dagDam[5],axeWins, dagWins, potWins, axeWinPer, dagWinPer, potWinPer))

################Test Variable
# Other specs are constants, this variable increases every numMatches number of matches and is then tested again with increased stat numMatches number of times.
# The stat will increase numRounds number of times
    TestVariableChange() 
#####################
con.commit()
cur.close()
con.close()