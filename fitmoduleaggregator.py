import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fitparser import EFTParser

# Setting up Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scope)
client = gspread.authorize(creds)
sheet = client.open("MarketStocking").sheet1

fit_parser = EFTParser()

stock_list_quantity = dict()
stock_list_occurrence = dict()
for filename in os.listdir(os.getcwd() + "/fits"):
    file = open("fits/" + filename, "r")
    fit = fit_parser.parse_fit(file.readlines())

    for item in fit:
        if stock_list_quantity.__contains__(item):
            stock_list_quantity[item] += fit[item]
            stock_list_occurrence[item] += 1
        else:
            stock_list_quantity[item] = fit[item]
            stock_list_occurrence[item] = 1

