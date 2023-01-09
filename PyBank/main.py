import os
import csv
import math #To use math.floor in order to round numbers to the nearest ¢
first_row = True
month_total = 0 #Variable initialization :D
profit_or_loss = 0 #Initialization
greatest_increase = 0
greatest_increase_stamp = ""
greatest_decrease = 0
greatest_decrease_stamp = ""
change = 0.0
average_change = 0.0
monthly_change = 0

input_csv_file = os.path.join('Resources', 'budget_data.csv')   #Defining the input .csv file
output_txt_file = os.path.join("analysis", "analysis.txt")      #Defining the output .txt file

def currency_format(x):
    cents = x*100   #cents (¢)
    mills = x*1000  #mills (₥)      1¢ = 10₥
    mills %= 1          #Mills are used in accounting, but here they are just used to round the cent up if it's half a cent or more!
    if cents % 1 != 0:
        if mills % 10 > 4:  #Four mills is less than half a cent
            cents = math.floor(cents) + 1
        else:               #Else, it's Five or more, so the cent rounds up!
            cents = math.floor(cents)
        x = cents / 100     #Converts back to dollars. The number now goes out 2 decimal places and rounds to the nearest cent! :D
    if x < 0:
        x *= -1                 #This is needed, since we are returning a string, and the negative is already included. 
        return "-$" + str(x)    #This keeps the minus sign **before** the dollar sign.
    else:
        return "$" + str(x)
with open(input_csv_file, encoding='UTF-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    csv_header = next(csvreader)    #Stores the Header Row

    for row in csvreader:
        current_row = int(row[1])
        if first_row:           #This only runs once, for the first row
            start = row[1]
            first_row = False
        else:
            monthly_change = current_row - previous_row #Calculates the change from the previous month

        month_total += 1
        profit_or_loss += int(row[1])   #adds the value for Profit/Loss in this row to the grand total
        
        if monthly_change > greatest_increase:      #This sets the greatest_increase to the monthly_change for this month, if it's higher than the current value
            greatest_increase = monthly_change
            greatest_increase_stamp = row[0]        #It also stores the corresponding month
        elif monthly_change < greatest_decrease:    #This does the same thing,
            greatest_decrease = monthly_change      #but sets greatest_decrease to the monthly_change this month, if it's lower than the current value
            greatest_decrease_stamp = row[0]
        previous_row = int(row[1])              #This is needed to calculate the change for the next month
        last_row = current_row                  #This gets re-written every row until the last row
    change = float(last_row) - float(start)
    average_change = change / (float(month_total)-1)    #The minus 1 is to exclude the first month
    print("Financial Analysis")                 #This begins printing everything to the console
    print("----------------------------")
    print(f'Total Months: {month_total}')
    print(f'Total: {currency_format(profit_or_loss)}')
    print(f'Average Change: {currency_format(average_change)}')
    print(f'Greatest Increase in Profits: {greatest_increase_stamp} ({currency_format(greatest_increase)})')
    print(f'Greatest Decrease in Profits: {greatest_decrease_stamp} ({currency_format(greatest_decrease)})')
with open(output_txt_file, 'w', encoding="UTF-8") as txt_file:
    txt_file.write("Financial Analysis")                #This does the same as above, but prints to a .txt file in the analysis folder
    txt_file.write("\n----------------------------")
    txt_file.write(f'\nTotal Months: {month_total}')
    txt_file.write(f'\nTotal: {currency_format(profit_or_loss)}')
    txt_file.write(f'\nAverage Change: {currency_format(average_change)}')
    txt_file.write(f'\nGreatest Increase in Profits: {greatest_increase_stamp} ({currency_format(greatest_increase)})')
    txt_file.write(f'\nGreatest Decrease in Profits: {greatest_decrease_stamp} ({currency_format(greatest_decrease)})')