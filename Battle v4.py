# This is the standalone game to be played by one person. The user chooses between an axe, a dagger, and a potion, each of which 
#has it's own level of risk and reward. The axe is the highest risk/reward while the dagger provides steady damage
import random

# Damage ranges. Negative represents the attacker tripping and causing damage to themselves
enemyDam = [-5, 100] # Range of damage the enemy can inflict
axeDam = [-50, 155] # Axe damage range
dagDam = [4,19,5,20,20,42] # Dagger damage ranges for each of the 3 strikes
potHeal = [54] # amount a potion heals

# Other variables
damageMultPercent = 0.05 # damage multiplier increases potential damage each turn
playerStartingHealth = 700
enemyStartingHealth = 700
playAgain = True # Player can switch to false with input if they do not want to play again
turnsMax = 30 # Max number of turns a round can take

def chooseWep(): # Asks player for weapon choice
    wep = ''
    while wep != 'AXE' and wep != 'DAG' and wep != 'POT':
        print('Choose between AXE, DAG, and POT for the turn!')
        wep = input().upper()
        print()
    return wep
    
def eAttack(damageMult): # calculates damage done after an enemy's turn
    damage = round(random.randint(enemyDam[0], enemyDam[1]) * damageMult) 
    if damage < 0:
        global EHealth
        print(f"The enemy tripped and did {int(round(damage))*-1} damage to themself...")
        EHealth += damage
    else:
        print(f"The enemy attacked and did {damage} damage to you.")
        global Health
        Health -= damage

def damCalc(damageMult): # Calculates damge done/ amount healed after player's turn
        global Health
        global EHealth
        print('Type AXE,  DAG, or POT')
        weapon = chooseWep()
        if weapon == 'AXE':
            damage = round(random.randint(axeDam[0], axeDam[1]) * damageMult)
            if damage >= 0:
                print('You did ' + str(damage) + ' damage!')
                EHealth -= damage
            else:
                print(f"You tripped using the heavy axe and did {damage * -1} to yourself.")
                Health += damage
        if weapon == 'DAG':
            ATT1 = random.randint(5, 20)
            ATT2 = random.randint(5, 20)
            ATT3 = round(random.randint(20, 40) * damageMult)
            damage = ATT1 + ATT2 + ATT3 
            EHealth -= damage
            print('You did ' + str(ATT1) + ', ' + str(ATT2) + ', and ' + str(ATT3) + ' damage!')
        if weapon == 'POT':
            heal = round(random.randint(30, 70) * damageMult)
            Health += heal
            print('You healed ' + str(heal))

while playAgain:
    Health = playerStartingHealth
    EHealth = enemyStartingHealth
    print(" _,-,   ^    ......")
    print(" T_ |   |    :.  .:")
    print("||`-'   |    .'  '.")
    print("||      |    |    |")
    print("||     (=)   |    |")
    print("~~      0    `----'")
    print("Axe, Dagger, Potion ")
    print()
    print("(ASCII art from asciiart.eu axe and dagger anonymous and potion by AMC)")
    print()
    print('Time to fight! You must take turns choosing to use the dagger, the ax, or healing potion to bring your opponent HP to zero! Dagger will strike three times for lower but more consistant damage while axe is riskier but can hit much harder. Type POT to heal. Damage increases over turns')
    print('HP 700')
    print('bad guy HP 700')
    print(f"You have {turnsMax} turns to win")

    for i in range(turnsMax):
        damageMult = 1 + (i * damageMultPercent) # each turn increases damage multiplier
        damCalc(damageMult)
        eAttack(damageMult)
        print('You have ' + str(round(Health)))
        print('Enemy has ' + str(round(EHealth)))
        print()
        if i + 2 <= turnsMax:
            print(f'Turn # {i + 2}')
        
        if Health <= 0:
            print('AW you\'re dead. GAME OVER')
            break
        if EHealth <= 0:
            print('You killed em\' dead. Good job!')
            break
    if Health > 0 and EHealth > 0:
        print("You have run out of turns")
    
    playAgain = input("Do you want to play again? Yes or No?").upper().startswith("Y")
    print()

