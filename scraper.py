import os
import requests
from urllib.request import urlopen

def get_title(soup: str) -> (str, str):
    title = soup[soup.find("title")+8:soup.find("}") - 1]
    soup = soup.replace("title", 'XXX', 1) #get rid of it to find the next
    soup = soup.replace("}", 'XXX', 1) #get rid of it to find the next
    return title, soup

url = "https://www.binance.com/en/support/announcement/c-48"
page = urlopen(url)
html = page.read().decode("utf-8")

# Pattern is like this: "New Crypto Listings","total":742,"articles":[{"id":51953,"code":"2c64611658c645a59e05ef12f02c22ab","title":"Binance Launches Zero-Commission, Tradable Stock Tokens"},{"id":51779
search_for = "\"New Crypto Listings\",\"total\":"
start_index = html.find(search_for) + len(search_for)

analyze_this = html[start_index:start_index+1000]
first_title, analyze_this = get_title(analyze_this)
second_title, analyze_this = get_title(analyze_this)
third_title, analyze_this = get_title(analyze_this)

comma_idx = analyze_this.find(",")
new_numba = analyze_this[:comma_idx]

old_numba_file = f"{os.path.abspath(os.getcwd())}/old_numba.txt"

#Make a blank file first time
if not os.path.exists(old_numba_file):
    with open(old_numba_file, 'w'): pass
else:
    with open(old_numba_file, 'r') as f:
        old_contents = f.readlines()

changed = False
if old_contents and len(old_contents) > 0:
    changed = not (old_contents[0] == new_numba)

updates = ''
line_break = '-'*80
if changed:
    updates = f"Binance Crypto Listing Updated, Displaying last 3: \
    \n{line_break}\n1. {first_title}\n2. {second_title}\n3. {third_title}"

#Add current number as trigger for new changes
with open(old_numba_file, 'w') as file:
    file.write(f"{new_numba}")

data = {
    "content" : f"{updates}",
    "username" : "cz"
}

webhook = "https://discord.com/api/webhooks/831343191768694824/xaodDYZvqTJU_DW4jeUEWWJpmMgdIWMvBphxvpA2dleMQcXDXv9bQYVIOTkUxtA1Tzws"

if updates != '':
    print(updates)
    #result = requests.post(webhook, json = data)
