from bs4 import BeautifulSoup
import requests
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

# Define the scope and credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('scraper-project-391720-5521d58f18ef.json', scope)

# Authorize the credentials
client = gspread.authorize(credentials)

sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1Bzedq9WqMuvgaV9VdpGXVJ4kXEjC5iVpslgnMFNYMkk/edit#gid=0').get_worksheet(0)

n = 1

prices_list = []  # Empty list to store prices
result_numbers_list = []  # Empty list to store result numbers


url = f"https://www.newegg.com/p/pl?N=100007709%20601357247%204814&d=3080&Order=3&isdeptsrh=1"

result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")

prices = doc.find_all("li", class_="price-current", limit=15)

    
for price in prices:
    strong = price.find("strong")
    sup = price.find("sup")
        
    if strong and sup:
        price_value = strong.text + sup.text
        prices_list.append(price_value)
        result_numbers_list.append(n)
        print("$" + price_value)
    else:
        print("Price information not found")
        prices_list.append("not found")
        result_numbers_list.append(n)

  
    print("result number =", n)
    print("\n")
    n += 1

# Print the final lists
print("Prices:", prices_list)
print("Result Numbers:", result_numbers_list)
# ...

# Prepare data for updating the sheet
data = []
for i in range(len(result_numbers_list)):
    if i < len(prices_list):
         data.append([result_numbers_list[i], prices_list[i], str(date.today()), "3080 GPU's"])
    else:
        data.append([result_numbers_list[i], "Price information not found"])

# Remove the last entry if it is blank
if data[-1][1] == '':
    data.pop()

# Get the last row number in the sheet
last_row = len(sheet.get_all_values())

# Update the sheet starting from the last row
sheet.update(f'I{last_row+1}:L', data)
