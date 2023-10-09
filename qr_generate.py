import os
import pandas as pd
import qrcode


#Read in the csv file containing all unique barcodes we need.
df = pd.read_csv('qr_generate.csv')

print(df.shape)
"""
#There are 6 Columns, each column needs to be looped and saved into a folder
#to generate a unique QR code for each row.

"""

# Check if 'QR codes' folder exists; if not, create it
base_folder = 'QR_codes'
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

# Loop over each column to generate QR codes
for column in df.columns:
    # Create a folder for each column inside 'QR codes' if it doesn't exist
    folder_path = os.path.join(base_folder, column.replace(' ', '_'))  # To make sure folder names don't have spaces
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # For each unique value in the column, generate a QR code
    for value in df[column].unique():
        if pd.isna(value): #replace nan with empty string
            continue
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=6,
            border=3,
        )
        qr.add_data(str(value))
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Remove spaces and special chars for filename
        filename = str(value).replace(" ", "_").replace(".", "").replace("-", "_")

        # Save QR code as png in the respective subfolder inside 'QR codes'
        img.save(os.path.join(folder_path, f'{filename}.png'))


print('All QR codes generated successfully!')
