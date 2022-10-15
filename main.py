# This is a sample Python script.
import pyautogui
import requests
import csv
from bs4 import BeautifulSoup


# a basic csv row writer function, capability to select a specific row will be implemented later
def write(s):
    with open('test.csv', 'w') as f:
        # create the csv writer
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(s)
        # write a row to the csv file


# initialize an array of string values and labels for the csv data
def main():
    header = ['GenBank Accession', 'PrimerBankID', 'FPrimer', 'FPrimer length', 'FPrimer tm', 'FPrimer location',
              'RPrimer', 'RPrimer length', 'FPrimer tm', 'RPrimer location', 'Coding Sequence', 'Validation Results']
    s = ["https://pga.mgh.harvard.edu/cgi-bin/primerbank/new_displayDetail2.cgi?primerID=6671509a1",
         "https://pga.mgh.harvard.edu/cgi-bin/primerbank/new_displayDetail2.cgi?primerID=6671509a2"]
    big_array = [header]
    for x in s:
        # data = \
        data = scrape(x)
        big_array.append(data)
    write(big_array)


def parse_coding_sequence(html_text, i):
    data = ''
    while len(html_text[i]) != 0:
        for n in range(len(html_text[i].split())):
            if n > 0 & n < len(html_text[i].split()) - 1:
                data += html_text[i].split()[n]
        i += 1

    print(data)
    return data


    # this is the final piece to finish, I need to parse the html file and make sure I only get the strings of nucleotides
    # this should also remove all spaces in the strings so that they are one large continuous stream of nucleotide bases


# scrape will eventually use beautiful soup to extract all text from the html and parse the html for a row of values.
# the values will be returned as an array of strings which will be written by the write function



def scrape(s):
    soup = BeautifulSoup(requests.get(s).content, 'html.parser')
    all_html = soup.get_text().splitlines()
    y = soup.get_text()
    # print(all_html)
    data = []
    i = 0
    for x in all_html:
        if x == 'PrimerBank ID':
            data.append(all_html[i + 1])
        elif x == 'GenBank Accession':
            data.append(all_html[i + 1])
        elif x == 'Forward Primer':
            data.append(all_html[i + 1])
            data.append(all_html[i + 2])
            data.append(all_html[i + 3])
            data.append(all_html[i + 4])
        elif x == 'Reverse Primer':
            data.append(all_html[i + 1])
            data.append(all_html[i + 2])
            data.append(all_html[i + 3])
            data.append(all_html[i + 4])
        elif x == 'Location in Coding Sequence (primers and amplicon highlighted)':
            x = parse_coding_sequence(all_html, i + 4)
            data.append(x)
        i += 1

    if 'Validation Results' in y:
        data.append('YES')
    else:
        data.append('NO')

    return data


main()
