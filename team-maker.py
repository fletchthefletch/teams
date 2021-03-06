from numpy import array
import pandas as pd
import sys 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

MIN_NUM_OF_PLAYERS = 8
MIN_PLAYERS_PER_TEAM = 4
MAX_PLAYERS_PER_TEAM = 5

LOCAL_FILE_NAME = 'test_data_file.xlsx'

def printHeading():
    print("________________________________________________________")
    print("THE DON'S TEAM CRAFTER")
    print("________________________________________________________\n")

def printTeams(teams, showRatings=False):
    print("TONIGHT'S TEAMS")
    i = 0
    while i < num_of_teams:
        print("________________________________________________________")
        print('[Team ' + str(i+1) + ' | Rating: ' + str(teams[i][0]['rating'].sum()) + ']')
        if showRatings:
            print(teams[i][0]) 
        else:
            print(teams[i][0]['name']) 
        i += 1

def printSubs(subs):
    if len(subs) == 0:
        print('\nNo subs tonight :-)\n')
    else: 
        print('\nOn the bench tonight is...')
        for sub in subs:
            print(sub[0] + ' : ' + str(sub[1]))

def readInPlayerValues():
    try:
        # Read spreadsheet arg
        player_sheet = pd.read_excel(sys.argv[1])
        print("Reading data...")
    except: 
        try:
            # Read local file arg
            player_sheet = pd.read_excel(open(LOCAL_FILE_NAME,'rb'), sheet_name=0)
            print("Reading data...")
            
        except:
            print("No data sheet provided!")
            quit()
    return player_sheet

def refinePlayers(playerSheet):
    newPlayerSheet = pd.DataFrame()
    i = 0

    while i < len(playerSheet):
        if (playerSheet.iloc[i][2] == 'y' or playerSheet.iloc[i][2] == 'Y'):
            # Check that player's name and score have been input
            if str(playerSheet.iloc[i][0]).strip() != '' and str(playerSheet.iloc[i][1]).strip() != '':
                newPlayerSheet = newPlayerSheet.append(playerSheet.iloc[i], ignore_index=True)
        i += 1

    return newPlayerSheet

def getNumOfTeams(numOfPlayers):
    # I thought long and hard about the best way to implement this method, 
    # but decided ultimately that the number of teams the Don may want for a 
    # given number of players could change - given venue or ability. 
    # The below statements look awful programmatically, but it's the most flexible approach.
    if (numOfPlayers < MIN_NUM_OF_PLAYERS):
        # Not enough players to field a team
        return -1
    elif numOfPlayers == 8:
        return 2
    elif numOfPlayers == 9:
        return 2
    elif numOfPlayers == 10:
        return 2
    elif numOfPlayers == 11:
        return 2
    elif numOfPlayers == 12:
        return 3
    elif numOfPlayers == 13:
        return 3
    elif numOfPlayers == 14:
        return 3
    elif numOfPlayers == 15:
        return 3
    elif numOfPlayers == 16:
        return 4
    elif numOfPlayers == 17:
        return 4
    elif numOfPlayers == 18:
        return 4
    elif numOfPlayers == 19:
        return 4
    elif numOfPlayers == 20:
        return 4
    
def getPlayersProspectiveTeam(allTeams, numOfTeams):
    # 1. Get team with the fewest players
    if numOfTeams < 1:
        return -1

    # Assign first team to be default
    smallestNumOfTeamPlayers = len(allTeams[0][0])

    i = 0
    while i < numOfTeams:
        if len(allTeams[i][0]) < smallestNumOfTeamPlayers:
            # This team has the fewest players
            smallestNumOfTeamPlayers = len(allTeams[i][0])
        i += 1

    teamsToConsider = []
    
    i = 0
    while i < numOfTeams:
        if len(allTeams[i][0]) == smallestNumOfTeamPlayers:
            teamsToConsider.append(allTeams[i])
        i += 1

    # 2. Get team with lowest rating out of teams with fewest amount of players
    targetTeam = teamsToConsider[0]
    targetTeamRating = teamsToConsider[0][0]['rating'].sum()

    i = 1 
    while i < len(teamsToConsider):
        teamRating = teamsToConsider[i][0]['rating'].sum()
        if teamRating < targetTeamRating:
            targetTeamRating = teamRating
            targetTeam = teamsToConsider[i]
        i += 1

    return targetTeam 

def createTeams(numOfTeams, numOfPlayers, playerSheet, subs):
    teams = []
    i = 0
    while i < numOfTeams:
        newTeam = pd.DataFrame(columns=['name', 'rating'])
        teams.append([newTeam, i])
        i += 1

    # Allocate players
    i = 0
    while i < numOfPlayers:
        # Get next team needing a player
        team = getPlayersProspectiveTeam(teams, numOfTeams)
        
        playerName = playerSheet.iloc[i][0]
        playerRating = playerSheet.iloc[i][1]
        
        row = pd.Series({'name':playerName, 'rating':playerRating})

        if len(team[0]) >= MAX_PLAYERS_PER_TEAM:
            # The team is full already, so add player to the floating bench! 
            subs.append(row)
        else:
            # Add player to team
            teams[team[1]][0] = team[0].append(row, ignore_index=True)
        i += 1
        
    return teams  


#### MAIN PROGRAM ####
player_sheet = readInPlayerValues()  
# Remove players who aren't playing tonight
refined_player_sheet = refinePlayers(player_sheet) 
# Randomize player order
refined_player_sheet = refined_player_sheet.sample(frac=1).reset_index(drop=True)
# Sort players by skill level
refined_player_sheet = refined_player_sheet.sort_values(by='Ability Score (1-10)', ascending=False)

num_of_players = len(refined_player_sheet)
num_of_teams = getNumOfTeams(num_of_players)

# Create team storage
subs = []
teams = createTeams(num_of_teams, num_of_players, refined_player_sheet, subs)

printHeading()
#print(player_sheet) # See all players in the Donadoni club
#print("________________________________________________________")
#print(refined_player_sheet) # See all players who want to play tonight
print('There are ' + str(num_of_players) + ' players keen on playing tonight.')
print("________________________________________________________")
#printTeams(teams)
printTeams(teams, True) # Print teams with player ratings
printSubs(subs)
