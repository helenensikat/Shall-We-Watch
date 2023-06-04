#! /usr/bin/python3

# DOCUMENTATION

# 'Shall We Watch' tells Helen (H) and Keith (K) what film they should watch from a list of 12, evenly weighted between films Helen thinks Keith should see, films Keith thinks Helen should see, and films neither have seen yet.
#  Reference setup in https://www.makeuseof.com/tag/read-write-google-sheets-python/ to make friends with Google Sheets
#  Recommend limiting the editable range of cells for secondary users of the spreadsheet.

# IMPORTANT VARIABLES

# check_cell (positive integer; 1 = sufficient films to run; 0 = insufficient films to run)
# chosen_film (string indicating randomly selected film)
# chosen_film_cell (cell reference for film watched)
# choice (1 or 2 - user entered choice to watch a film or exit)

# LIBRARIES

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import time
from sys import stdout as terminal
from time import sleep
from itertools import cycle
from threading import Thread

# ENCODING FIX (Test)

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# LOGIC

# Rolling animation (Adapted from rudrathegreat/Loading.py)

done = False

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        terminal.write('\rRolling a D12 ' + c +'\r')
        terminal.flush()
        sleep(0.05)

t = Thread(target=animate)
t.start()
sleep(3)
done = True

# Talk to Google Sheets

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

credentials = gspread.service_account(filename=r'shall-we-watch-62362fc672fa.json')
spreadsheet = credentials.open_by_url('https://docs.google.com/spreadsheets/d/1gH4V8iAmxLY4IRIdLWw0gzFMJf8HomNocR_dvqcBIm4/edit#gid=0') 
sheet = spreadsheet.worksheet('Films') 

# Hacky forced refresh / recalc

sheet.update('I1', 'Bingo!')
sheet.update('I1', '')

# Check sheet has sufficient films in each list

check_cell = sheet.cell(5, 7).value # Gets value from G5
if (check_cell == '0'):
    print("Insufficient films - make sure at least four are in each list.")
    quit()

# Return a film to watch

chosen_film = sheet.cell(7, 7).value # Retrieves selected film from G7
print("Shall we watch " + chosen_film + "?")

# Prompt user to choose 1 (Watch chosen_film and remove from list) or 2 (Exit without change) and clean up accordingly

choice = int(input("Enter 1 to watch this film and remove it from the list, or 2 to exit without watching:  "))

# Clear selected film from the list in which it appears and confirm before exiting

if (choice == 1):
    print("Happy watching!")
    chosen_film_cell = sheet.acell('G8').value
    sheet.update(chosen_film_cell, '', raw=False)
    print("Cell " + chosen_film_cell + " cleared.")
    quit()

# Exit without modifying the film lists

elif (choice == 2):
    print("Understandable, have a nice day.")
    quit()