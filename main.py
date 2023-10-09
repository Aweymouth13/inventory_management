#import libraries

import pandas as pd #holding dataframe
from datetime import datetime #timestamp
import os #check files/folders

#function is passed equipment ID and checks how many times it has been logged
#if it is an even amount returns checked out, else returns checked in
def determine_status(equipment):
    df = pd.read_csv('log.csv')
    count = df[df['Equipment'] == equipment].shape[0]
    return 'checked in' if count % 2 == 1 else 'checked out'


#define columns for the CSV
columns = ['Equipment', 'Techs', 'Cabinet', 'Shelf', 'Status', 'Timestamp']

# If CSV doesn't exist, create one with headers
if not os.path.exists('log.csv'):
    with open('log.csv', 'w') as f:
        f.write(','.join(columns) + '\n')

entries = []

try:
    while True:
        print("=== New Item ===")
        current_entry = {}

        # Input for each item
        for col in columns[:-2]:  # We handle Status and Timestamp separately
            user_input = input(f"Please Scan the {col}: ")

            # Check for special inputs
            if user_input == 'new_line':
                # Save to CSV immediately
                current_entry['Status'] = determine_status(current_entry.get('Equipment', ''))
                current_entry['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open('log.csv', 'a') as f:
                    f.write(','.join([str(current_entry.get(col, '')) for col in columns]) + '\n')
                break
            elif user_input == 'Void':
                print("Entry Voided: Please scan Item again")
                current_entry = {}
                break

            current_entry[col] = user_input

        else:  # This part will run if the loop completes without a 'break'
            # If some data was entered
            if current_entry:
                current_entry['Status'] = determine_status(current_entry['Equipment'])
                current_entry['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # Save to CSV
                with open('log.csv', 'a') as f:
                    f.write(','.join([str(current_entry[col]) for col in columns]) + '\n')

except KeyboardInterrupt:
    print("\nLogging ended.")


