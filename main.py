# This is a sample Python script.
import pyautogui
import requests
import csv
from bs4 import BeautifulSoup


# a basic csv row writer function, capability to select a specific row will be implemented later
def write(s):
    with open('test.csv', 'w') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(s)


# initialize an array of string values and labels for the csv data
def main():
    write(['PrimerBankID', 'GenBank Association', 'FPrimer', 'FPrimer length', 'FPrimer tm', 'FPrimer location',
           'RPrimer', 'RPrimer length', 'FPrimer tm', 'RPrimer location', 'Coding Sequence', 'Validation Results'])
    s = ["https://pga.mgh.harvard.edu/cgi-bin/primerbank/new_displayDetail2.cgi?primerID=6671509a1",
         "https://pga.mgh.harvard.edu/cgi-bin/primerbank/new_displayDetail2.cgi?primerID=6671509a2"]
    for x in s:
        # data = \
        scrape(x)
        # write(data)


# scrape will eventually use beautiful soup to extract all text from the html and parse the html for a row of values.
# the values will be returned as an array of strings which will be written by the write function
def scrape(s):
    soup = BeautifulSoup(requests.get(s).content, 'html.parser')
    all_html = soup.get_text()
    for x in all_html:
        print(x)


main()

