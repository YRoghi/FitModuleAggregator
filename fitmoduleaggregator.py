import os
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from fitparser import EFTParser

# Setting up Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scope)
client = gspread.authorize(creds)
sheet = client.open("MarketStocking").sheet1

fit_parser = EFTParser()
fits_path = os.getcwd() + "/fits"

# Quantity used as a metric for volume required on market
stock_list_quantity = dict()
# Occurrence used as a metric to determine stocking priority based on prevalence in fits
stock_list_occurrence = dict()
for filename in os.listdir(fits_path):
    file = open("fits/" + filename, "r")
    fit = fit_parser.parse_fit(file.readlines())

    for item in fit:
        if item in stock_list_quantity:
            stock_list_quantity[item] += fit[item]
            stock_list_occurrence[item] += 1
        else:
            stock_list_quantity[item] = fit[item]
            stock_list_occurrence[item] = 1

# -------------------------------
# Google Sheet Section
# -------------------------------
CURRENT_ROW = 5

for item in stock_list_occurrence:
    item_id_request = requests.get(f"https://esi.evetech.net/latest/search/?categories=inventory_type&datasource=tranquility&language=en-us&search=%20{item.replace(' ', '%20')}&strict=true")
    if item_id_request.json():
        item_id = item_id_request.json()['inventory_type'][0]
        item_info_request = requests.get(f"https://esi.evetech.net/latest/universe/types/{item_id}/?datasource=tranquility&language=en-us")
        item_packaged_volume = item_info_request.json()['packaged_volume']
        current_row = sheet.range(f"A{CURRENT_ROW}:D{CURRENT_ROW}")
        current_row[0].value = item                                                       # Item Name
        current_row[1].value = item_id                                                    # Item ID
        current_row[2].value = item_packaged_volume                                       # Volume
        current_row[3].value = stock_list_occurrence[item]/len(os.listdir(fits_path))     # Weight
        sheet.update_cells(current_row)
        CURRENT_ROW += 1
    else:
        print(f"ERROR: Could not resolve: {item}.")

print("Sheet updated COMPLETED.")