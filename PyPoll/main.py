import os
import csv
import math

total_votes = 0 #Initializing variables
first_row = True
add_candidate = True
winner = ""
winner_votes = 0

input_csv_file = os.path.join('Resources', 'election_data.csv')   #Defining the input .csv file
output_txt_file = os.path.join("analysis", "analysis.txt")      #Defining the output .txt file

candidate_name = []
candidate_votes = []
candidate_percent = []

with open(input_csv_file, encoding='UTF-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    csv_header = next(csvreader)    #Stores the Header Row
    for row in csvreader:
        candidate = row[2]
        if first_row:
            candidate_name.append(candidate)    #This only runs once, to add the initial vote for the initial candidate to the candidate_name and candidate_votes lists
            candidate_votes.append(1)
            first_row = False                   #This line ensures it only runs once
        else:
            for i in range(len(candidate_name)):    #Loops once for every candidate currently in the candidate_name list
                if candidate_name[i] == candidate:  #If the name of the candidate is the same as a current index . . .
                    votes = candidate_votes[i]      #Then we grab that candidate's vote total, referancing the same index in the candidate_votes list
                    votes += 1                      #1 is added to add this vote to the total
                    candidate_votes[i] = votes      #And the corresponding index in the candidate_votes list is updated
                    add_candidate = False       #Since the name matched, triggering this if statement, add_candidate is set to false, so the next code doesn't run
            if add_candidate:
                candidate_name.append(candidate)    #(see previous comment above) We only want this to run if no valuse in the candidate_name list match the name
                candidate_votes.append(1)           #of the candidate being voted for. Since this adds a new entry to both candidate_name and candidate_votes lists
            add_candidate = True            #This part needs to run here in order to reset this boolean value. Otherwise, only the first candidate will have their values stored
        total_votes += 1                #This adds 1 to the number of total votes :)
    print(f"Election Results\n----------------------------------------\nTotal Votes: {total_votes}\n----------------------------------------")
            #Here we begin printing to the console
    for i in range(len(candidate_name)):                            #This loops once for every candidate
        votes_of_this_candidate = candidate_votes[i]                #Storing this candidate's vote total
        percent = (votes_of_this_candidate / total_votes) * 100
        decimal_places = percent * 1000                             #This part takes a slightly different approach to rounding values compared to PyBank
        rounding = math.fmod(decimal_places, 1)                     #In the end, it does the same thing, rounding the value to the nearest 3 decimal places out
        if rounding < 0.5:
            decimal_places = math.floor(decimal_places)             #This code runs when rounding down
        else:
            decimal_places = math.floor(decimal_places) + 1         #And this code runs when rounding up
        percent = int(decimal_places) / 1000
        candidate_percent.append(str(percent) + "%")        #Since we are looping from index 0, adding the percentage to the end of the candidate_percent is appropriate 
        if votes_of_this_candidate > winner_votes:
            winner_votes = votes_of_this_candidate          #This updates winner_votes and winner every time a vote total is higher than the current highest recorded
            winner = candidate_name[i]                      #That way the winner and their respective vote totals can be displayed below
        print(f"{candidate_name[i]}: {candidate_percent[i]} ({candidate_votes[i]})")    #Since we are looping, this prints the respective totals once for each candidate
    print(f"----------------------------------------\nWinner: {winner}\n----------------------------------------")
with open(output_txt_file, 'w', encoding="UTF-8") as txt_file:                                  #And finally, this part does everything we did printing to the console, 
    txt_file.write(f"Election Results\n----------------------------------------")               #but instead, writing the information to a .txt file in the analysis folder
    txt_file.write(f"\nTotal Votes: {total_votes}\n----------------------------------------")
    for i in range(len(candidate_name)):
        txt_file.write(f'\n{candidate_name[i]}: {candidate_percent[i]} ({candidate_votes[i]})')
    txt_file.write(f"\n----------------------------------------\nWinner: {winner}\n----------------------------------------")